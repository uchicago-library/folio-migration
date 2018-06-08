from argparse import ArgumentParser
from datetime import datetime
from foliolibrary import *
from olelibrary import OleContext
import json
import logging
import foliolibrary
import sys
import uuid

def main():
    global logger
    logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    f = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(f)
    logger.addHandler(sh)
    fh = logging.FileHandler('trace.log')
    fh.setFormatter(f)
    logger.addHandler(fh)
    logger = logging.getLogger('olefolioapplication')
    dt = datetime.now()
    logger.info('Starting')
    ap = ArgumentParser()
    ap.add_argument('--load', action='store_true')
    ap.add_argument('--load-address-types', action='store_true')
    ap.add_argument('--load-groups', action='store_true')
    ap.add_argument('--load-permissions', action='store_true')
    ap.add_argument('--load-permissions-users', action='store_true')
    ap.add_argument('--load-proxies', action='store_true')
    ap.add_argument('--load-users', action='store_true')
    args = ap.parse_args()
    if args.load or args.load_address_types: load_address_types()
    if args.load or args.load_groups: load_groups()
    #if args.load_permissions: load_permissions()
    #if args.load_permissions_users: load_permissions_users()
    #if args.load_proxies: load_proxies()
    if args.load or args.load_users: load_users()
    logger.info('Ending')
    logger.info(f'{datetime.now() - dt} elapsed')
    sys.exit(0)

def load_address_types():
    logger.info('Loading address types')
    dt = datetime.now()
    dt2 = datetime.now()
    oc = OleContext()
    fc = FolioContext()
    fc.truncate_address_types()
    i = 0
    for at in oc.address_types():
        fc.insert_address_type(AddressType(id=at.guid, content=json.dumps({'id': at.guid, 'desc': None, 'addressType': at.name })))
        i = i + 1
        if i % 1000 == 0:
            fc.commit()
            if i % 10000 == 0:
                logger.info(f'{i} {datetime.now() - dt2} {datetime.now() - dt}')
                dt2 = datetime.now()
    fc.commit()
    logger.info(f'{i} {datetime.now() - dt2} {datetime.now() - dt}')
    logger.info(f'Added {i} address types')
    logger.info(f'{datetime.now() - dt} elapsed')

def load_groups():
    logger.info('Loading groups')
    dt = datetime.now()
    dt2 = datetime.now()
    oc = OleContext()
    fc = FolioContext()
    fc.truncate_groups()
    i = 0
    #{"id": "1c6fe965-f0a9-414c-93bf-13b34fc1ae73", "desc": "Graduate Student", "group": "graduate", "metadata": {"createdDate": "2017-12-14T17:38:24.681+0000", "updatedDate": "2017-12-14T17:38:24.681+0000", "createdByUserId": "1ad737b0-d847-11e6-bf26-cec0c932ce01", "updatedByUserId": "1ad737b0-d847-11e6-bf26-cec0c932ce01"}}
    for pt in oc.patron_types():
        fc.insert_group(Group(id=pt.guid, content=json.dumps({'id': pt.guid, 'desc': None, 'group': pt.name, 'metadata': { 'createdDate': None, 'updatedDate': None, 'createdByUserId': None, 'updatedByUserId': None}}), creation_time=dt, creation_user_id=None))
        i = i + 1
        if i % 1000 == 0:
            fc.commit()
            if i % 10000 == 0:
                logger.info(f'{i} {datetime.now() - dt2} {datetime.now() - dt}')
                dt2 = datetime.now()
    fc.commit()
    logger.info(f'{i} {datetime.now() - dt2} {datetime.now() - dt}')
    logger.info(f'Added {i} groups')
    logger.info(f'{datetime.now() - dt} elapsed')

def load_users():
    logger.info('Loading users')
    dt = datetime.now()
    dt2 = datetime.now()
    oc = OleContext()
    fc = FolioContext()
    fc.truncate_users()
    fc.truncate_permissions_users()
    fc.truncate_logins()
    l = ['arnt', 'byrne', 'cmalmbor', 'elong', 'jemiller', 'seanf', 'tod', 'clthomas', 'cueker', 'dbottorff', 'ecboettcher', 'emerkel', 'gatt', 'kefeeney', 'kzadrozny', 'lar1', 'mouw', 'natascha', 'stp0']
    i = 0
    for a in oc.query("SELECT p.entity_id AS id, p.obj_id AS guid, p.actv_ind AS active, p2.barcode, (SELECT prncpl_nm FROM krim_prncpl_t u WHERE u.entity_id = p.entity_id LIMIT 1) AS user_name, (SELECT local_id FROM ole_ptrn_local_id_t i WHERE i.ole_ptrn_id = p2.ole_ptrn_id LIMIT 1) AS external_system_id, n.first_nm AS first_name, n.middle_nm AS middle_name, n.last_nm AS last_name, e.email_addr AS email_address FROM krim_entity_t p LEFT JOIN ole_ptrn_t p2 ON p2.ole_ptrn_id = p.entity_id LEFT JOIN krim_entity_nm_t n ON n.entity_id = p.entity_id LEFT JOIN krim_entity_email_t e ON e.entity_id = p.entity_id WHERE n.dflt_ind = 'Y' AND (e.dflt_ind IS NULL OR e.dflt_ind = 'Y')", take=100000):
    #for a in oc.query("SELECT * FROM (SELECT p.entity_id AS id, p.obj_id AS guid, p.actv_ind AS active, p2.barcode, (SELECT prncpl_nm FROM krim_prncpl_t u WHERE u.entity_id = p.entity_id LIMIT 1) AS user_name, (SELECT local_id FROM ole_ptrn_local_id_t i WHERE i.ole_ptrn_id = p2.ole_ptrn_id LIMIT 1) AS external_system_id, n.first_nm AS first_name, n.middle_nm AS middle_name, n.last_nm AS last_name, e.email_addr AS email_address FROM krim_entity_t p LEFT JOIN ole_ptrn_t p2 ON p2.ole_ptrn_id = p.entity_id LEFT JOIN krim_entity_nm_t n ON n.entity_id = p.entity_id LEFT JOIN krim_entity_email_t e ON e.entity_id = p.entity_id WHERE n.dflt_ind = 'Y' AND (e.dflt_ind IS NULL OR e.dflt_ind = 'Y')) a WHERE a.user_name = 'jemiller'", take=1):
        fc.insert_user(User(id=a['guid'], content=json.dumps({'id': a['guid'], 'active': a['active'] == 'Y', 'barcode': a['barcode'], 'personal': {'email': None if a['email_address'] is None else 'nospam.' + a['email_address'], 'lastName': a['last_name'], 'firstName': a['first_name'], 'middleName': a['middle_name']}, 'username': a['user_name'], 'externalSystemId': a['external_system_id']}), creation_time=None, creation_user_id=None))
        fc.insert_permissions_user(PermissionsUser(id=str(uuid.uuid4()), content=json.dumps({'id': a['guid'], 'userId': a['guid'], 'permissions': ['perms.all', 'login.all', 'users.all', 'module.trivial.enabled', 'module.users.enabled', 'module.items.enabled', 'module.instances.enabled', 'module.inventory.enabled', 'module.checkin.enabled', 'module.checkout.enabled', 'module.scan.enabled', 'module.requests.enabled', 'module.organization.enabled', 'module.notes.enabled', 'module.search.enabled', 'settings.enabled', 'settings.checkout.enabled', 'settings.developer.enabled', 'settings.loan-rules.all', 'settings.loan-policies.all', 'settings.loan-types.all', 'settings.material-types.all', 'settings.usergroups.all', 'settings.addresstypes.all', 'stripes-util-notes.all', 'ui-circulation.settings.loan-policies', 'ui-circulation.settings.loan-rules', 'ui-items.settings.material-types', 'ui-items.settings.loan-types', 'ui-organization.settings.key-bindings', 'ui-organization.settings.locale', 'ui-organization.settings.plugins', 'ui-organization.settings.sso', 'ui-users.editpermsets', 'ui-users.settings.usergroups', 'ui-users.settings.addresstypes', 'ui-users.settings.permsets', 'configuration.all', 'users-bl.all', 'inventory-storage.all', 'inventory.all', 'circulation-storage.all', 'circulation.all', 'notify.all', 'notes.all'] if a['user_name'] is not None and any(a['user_name'] in s for s in l) else []})))
        if any(a['user_name'] is not None and a['user_name'] in s for s in l):
            fc.insert_login(Login(id=str(uuid.uuid4()), content=json.dumps({'id': a['guid'], 'hash': '52DCA1934B2B32BEA274900A496DF162EC172C1E', 'salt': '483A7C864569B90C24A0A6151139FF0B95005B16', 'userId': a['guid']})))
        i = i + 1
        if i % 1000 == 0:
            fc.commit()
            if i % 10000 == 0:
                logger.info(f'{i} {datetime.now() - dt2} {datetime.now() - dt}')
                dt2 = datetime.now()
    fc.commit()
    logger.info(f'{i} {datetime.now() - dt2} {datetime.now() - dt}')
    logger.info(f'Added {i} users')
    logger.info(f'{datetime.now() - dt} elapsed')

if __name__ == '__main__': main()
