#!/bin/bash

tenant_id="lu"
tenant_name="Lehigh University"
tenant_desc="Lehigh University"
# This is the FOLIO admin user password, which must match
# the one set in the sql file loaded into the database
# for the users module.
admin_user="${tenant_id}_admin"
admin_user_pw="PASSWORDGOESHERE"
hostname=`hostname --fqdn`
# Set this to the name of the network interface with the
# machine's "public" IP address -- whatever will be used
# by docker containers to talk to the host,
# e. g. eth0 or ens192
network_iface="NETWORK_INTERFACE_GOES_HERE"
primary_ip_addr=`ip addr show dev $network_iface | grep "inet " | awk '{$1=$1;print}' | cut -f 2 -d" " | cut -f 1 -d'/'`
node_id="$hostname"
# This could also be going through a reverse proxy, e. g.
# okapi_url="https://${hostname}/okapi"
okapi_url="http://${hostname}:9130"
# The postgres_host will be used by docker containers, so it has
# to be an IP address in case name resolution isn't working, and
# it can't be localhost since each container has its own localhost
# that doesn't refer to the host machine but the container itself.
postgres_host="$primary_ip_addr"
postgres_port="5432"
postgres_folio_db="folio"
postgres_folio_user="folio"
postgres_folio_pw="PG_FOLIO_PW"
postgres_okapi_pw="PG_OKAPI_PW"
is_cluster="N"
builddir=`pwd`
# If we're building for a cluster, then we want
# node IDs from the cluster
# Otherwise, just use the IP address here
#node_id=`hostname -I | cut -f 1 -d " "`
stripes_path="/var/www/folio-testing-platform/folio-stripes-platform"

# This deletes the schemas created by the modules, so we have a clean slate
./clear_roles.sh

# Assume okapi and postgres are installed, but remove existing databases and reset them
su postgres bash -c "psql postgres postgres -c 'create role okapi with password \'$postgres_okapi_pw\' login createdb'"
su postgres bash -c "psql postgres postgres -c 'create role folio with password \'$postgres_okapi_pw\' login superuser'"
su postgres bash -c "psql postgres postgres -c 'create database okapi with owner okapi'"
su postgres bash -c "psql postgres postgres -c 'create database folio with owner folio'"

/usr/share/folio/okapi/bin/okapi.sh --initdb
systemctl restart okapi
sleep 10
if [ -d folio-install ]; then
    rm -rf folio-install
fi
git clone https://github.com/folio-org/folio-install
# Pull module descriptors from repository specified in okapi-pull.json
curl -w '\n' -D - -X POST -H "Content-type: application/json" -d @./folio-install/okapi-pull.json ${okapi_url}/_/proxy/pull/modules
cat >./tenant.json <<EOF
{
  "id" : "$tenant_id",
  "name" : "$tenant_name",
  "description" : "$tenant_desc"
}
EOF
# Create tenant in Okapi
curl -w '\n' -D - -X POST -H "Content-type: application/json" -d @./tenant.json ${okapi_url}/_/proxy/tenants
# Enable okapi internal module for tenant
curl -w '\n' -D - -X POST -H "Content-type: application/json" -d '{"id":"okapi"}' ${okapi_url}/_/proxy/tenants/${tenant_id}/modules
n lts
if [ -d folio-testing-platform ]; then
    rm -rf folio-testing-platform
fi
git clone https://github.com/folio-org/folio-testing-platform
cp lu-favicon.ico folio-testing-platform/tenant-assets/
cp lu-logo.gif folio-testing-platform/tenant-assets/
cd $builddir/folio-testing-platform
sed -i "s@http://localhost:9130@$okapi_url@g" stripes.config.js
sed -i 's/diku/'"$tenant_id"'/g' stripes.config.js
sed -i "s/opentown-libraries-logo.png/lu-logo.gif/g" stripes.config.js
sed -i "s/opentown-libraries-favicon.png/lu-favicon.ico/g" stripes.config.js
sed -i "s/Opentown Libraries/Lehigh University Library/g" stripes.config.js
# Build stripes platform
yarn install
yarn build output --sourcemap
# Then copy the output folder to where the webserver looks for it
if [ -d $stripes_path ]; then
	mkdir -p $stripes_path
    rmdir $stripes_path
fi
mv output $stripes_path
chown -R www-data:www-data $stripes_path
cd $builddir
echo "Deploying FOLIO backend for modules specified in stripes platform"
perl folio-install/gen-module-list.pl folio-testing-platform/ModuleDescriptors > enable.json
curl -w '\n' -X POST -D - -H "Content-type: application/json" -d @enable.json -o full-install.json ${okapi_url}/_/proxy/tenants/${tenant_id}/install?simulate=true
#Setup Okapi environment variables so modules know where the database can be found
curl -w '\n' -D - -X POST -H "Content-Type: application/json" -d "{\"name\":\"db.host\",\"value\":\"$postgres_host\"}" ${okapi_url}/_/env
curl -w '\n' -D - -X POST -H "Content-Type: application/json" -d "{\"name\":\"db.port\",\"value\":\"$postgres_port\"}" ${okapi_url}/_/env
curl -w '\n' -D - -X POST -H "Content-Type: application/json" -d "{\"name\":\"db.database\",\"value\":\"$postgres_folio_db\"}" ${okapi_url}/_/env
curl -w '\n' -D - -X POST -H "Content-Type: application/json" -d "{\"name\":\"db.username\",\"value\":\"$postgres_folio_user\"}" ${okapi_url}/_/env
curl -w '\n' -D - -X POST -H "Content-Type: application/json" -d "{\"name\":\"db.password\",\"value\":\"$postgres_folio_pw\"}" ${okapi_url}/_/env

if [ "$is_cluster" == "Y" ]; then
    echo "Get the node IDs from the cluster, then loop over them and generate deployment descriptors for each one, distributing the descriptors across the cluster nodes evenly probably, or perhaps putting all modules on every node, whichever"
else
    # Create deployment descriptors for the backend modules Okapi told us we need earlier
    cd $builddir
    if [ -d deployment-descriptors ]; then
	rm -rf deployment-descriptors
    fi
    perl folio-install/gen-deploy-descrs.pl --node $node_id full-install.json folio-install/deployment-descriptor-templates
    echo "Pulling docker images for modules"
    perl folio-install/docker-pull.pl ./deployment-descriptors
    sleep 10
    echo "Deploying the modules"
    cd $builddir/deployment-descriptors
    for i in *; do curl -w '\n' -D - -X POST -H "Content-type: application/json" -d @${i} ${okapi_url}/_/discovery/modules; done
    cd $builddir
    sleep 180 # Wait a while for okapi and docker to catch up -- 3 minutes is arbitrary, but will probably be long enough
    echo "Enabling modules for tenant $tenant_id"
    curl -w '\n' -X POST -D - -H "Content-type: application/json" -d @full-install.json ${okapi_url}/_/proxy/tenants/${tenant_id}/install
    echo "Creating FOLIO superuser"
    PGPASSWORD="$postgres_folio_pw"
    psql -h $primary_ip_addr -U folio -1 -f ./${tenant_id}_admin.sql folio
    echo "Loading permissions for superuser"
    perl folio-install/load-permissions.pl --tenant ${tenant_id} --user $admin_user --password $admin_user_pw --okapi "$okapi_url"
    echo "Load reference data"
    perl folio-install/load-reference-data.pl folio-install/reference-data --tenant ${tenant_id} --user $admin_user --password $admin_user_pw --okapi "$okapi_url"
fi


