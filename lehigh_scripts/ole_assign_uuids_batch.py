import MySQLdb
import uuid
from datetime import datetime

fields_update_queries = {
    "bib_uuid" : "update ole_ds_bib_t "
    }

tables_fields_queries = {
    "ole_ds_bib_t" : { "bib_id" : { "new_field" : "bib_uuid", "query" : "update ole_ds_bib_t set bib_uuid = %s where bib_id = %s", "data" : list() } },
    "ole_ds_holdings_t" : { "holdings_id" : { "new_field" : "holdings_uuid", "query" : "update ole_ds_holdings_t set holdings_uuid = %s where holdings_id = %s", "data" : list() },
                            "bib_id" : { "new_field" : "bib_uuid", "query" : "update ole_ds_holdings_t set bib_uuid = %s where bib_id = %s", "data" : list() } },
    "ole_ds_item_t" : { "item_id" : { "new_field" : "item_uuid", "query" : "update ole_ds_item_t set item_uuid = %s where item_id = %s", "data" : list() },
                        "holdings_id" : { "new_field" : "holdings_uuid", "query" : "update ole_ds_item_t set holdings_uuid = %s where holdings_id = %s", "data" : list() } },
    "ole_dlvr_loan_t" : { "item_uuid" : { "new_field" : "item_actual_uuid", "query" : "update ole_dlvr_loan_t set item_actual_uuid = %s where item_uuid = %s", "data" : list() },
                          "loan_tran_id" : { "new_field": "loan_uuid", "query" : "update_ole_dlvr_loan_t set loan_uuid = %s where loan_tran_id = %s", "data" : list() } },
    "ole_dlvr_circ_record" : { "item_uuid" : { "new_field" : "item_actual_uuid", "query" : "update ole_dlvr_circ_record set item_actual_uuid = %s where item_uuid = %s", "data" : list() },
                               "loan_tran_id" : { "new_field" : "loan_uuid", "query" : "update ole_dlvr_circ_record set loan_uuid = %s where loan_tran_id = %s", "data" : list() } }
    }

id_fields_tables = {
    "bib_id" : [ "ole_ds_bib_t", "ole_ds_holdings_t" ],
    "holdings_id" : [ "ole_ds_holdings_t", "ole_ds_item_t" ],
    "item_id" : [ "ole_ds_item_t" ],
    "item_uuid" : [ "ole_dlvr_loan_t", "ole_dlvr_circ_record" ]
}

remove_prefix_fields = {
    "ole_dlvr_loan_t" : { "item_uuid" : "wio-" },
    "ole_dlvr_circ_record" : { "item_uuid" : "wio-" }
    }

dbhost = "localhost"
dbuser = "root"
dbpasswd = "MySQLRootPWGoesHere"
ole_dbname = "ole"
migration_dbname = "ole_folio_migration"

ole_db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpasswd, db=ole_dbname)

update_count = 0
batch_size = 100

def updateDBBatch(db, query, batch, uuid_val, id_val):
    batch.append((uuid_val, id_val))
    print "Adding to batch for query:\"",query,"\", with values:",str(uuid_val),",",str(id_val)
    if len(batch) == batch_size:
        print "Executing query:\"",query,"\", with batch size of",batch_size,", time is:",str(datetime.now())
        cursor = db.cursor()
        try:
            cursor.executemany(query, batch)
            db.commit()
            #batch.clear()
            batch[:] = []
        except MySQLdb.Error, e:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            db.rollback()        

def updateDB(db, query, now=False):
    global update_count, batch_size
    print "    updateDB query: " + query
    if ( update_count % batch_size == 0 or now ):
        try:
            print "Reached update",update_count,", committing, time is:",str(datetime.now())
            db.commit()
        except MySQLdb.Error, e:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            db.rollback()            
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(query)
        update_count = update_count + 1
    #    db.commit()
    except MySQLdb.Error, e:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        db.rollback()

def queryDB(db, query):
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    db.commit()
    return cursor.fetchall()

def init_migration_db():
    query = "drop database if exists ole_folio_migration"
    updateDB(ole_db, query, True)
    query = "create database ole_folio_migration"
    updateDB(ole_db, query, True)
    migration_db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpasswd, db=migration_dbname)    
    # Add UUID columns to all tables
    for table in tables_fields_queries:
        print "Processing table",table
        print "Adding all rows from",ole_dbname,".",table,"to",migration_dbname,".",table
        query = "create table " + migration_dbname + "." + table + " like " + ole_dbname + "." + table
        updateDB(migration_db, query, True)
        query = "insert into " + migration_dbname + "." + table + " select * from " + ole_dbname + "." + table
        updateDB(migration_db, query, True)
        for old_field in tables_fields_queries[table]:
            print "Creating ",tables_fields_queries[table][old_field]["new_field"]," linked to",old_field,"in table",table
            query = "alter table " + table + " add column " + tables_fields_queries[table][old_field]["new_field"] + " varchar(36) default null after " + old_field
            updateDB(migration_db, query, True)

def process_bib(db, bib_row):
    bib_uuid = uuid.uuid4()
    # This should put the bib UUID in the all tables where the bib ID appears, in the appropriate fields
    for table in id_fields_tables["bib_id"]:
        fields_queries = tables_fields_queries[table]
        for field in fields_queries:
            updateDBBatch(db, fields_queries[field]["query"], fields_queries[field]["data"], str(bib_uuid), bib_row["bib_id"])
        
def process_holdings(db, holdings_row):
    holdings_uuid = uuid.uuid4()
    for table in id_fields_tables["holdings_id"]:
        fields_queries = tables_fields_queries[table]
        for field in fields_queries:
            updateDBBatch(db, fields_queries[field]["query"], fields_queries[field]["data"], str(holdings_uuid), holdings_row["holdings_id"])

def process_item(db, item_row):
    item_uuid = uuid.uuid4()
    for table in id_fields_tables["item_id"]:
        fields_queries = tables_fields_queries[table]
        for field in fields_queries:
            updateDBBatch(db, fields_queries[field]["query"], fields_queries[field]["data"], str(item_uuid), item_row["item_id"])

def process_data(db, data_row, id_field):
    new_uuid = uuid.uuid4()
    for table in id_fields_tables[id_field]:
        fields_queries = tables_fields_queries[table]
        updateDBBatch(db, fields_queries[id_field]["query"], fields_queries[id_field]["data"], str(new_uuid), data_row[id_field])                      
        #for field in fields_queries:
        #    updateDBBatch(db, fields_queries[field]["query"], fields_queries[field]["data"], new_uuid, data_row[id_field])

init_migration_db()

migration_db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpasswd, db=migration_dbname)    

print "Processing bibs:"
query = "select bib_id from ole_ds_bib_t"
bib_rows = queryDB(ole_db, query)
print "Got back",len(bib_rows),"rows"
for bib_row in bib_rows:
    process_data(migration_db, bib_row, "bib_id")

print "Processing holdings:"
query = "select holdings_id from ole_ds_holdings_t"
holdings_rows = queryDB(ole_db, query)
print "Got back",len(holdings_rows),"rows"
for holdings_row in holdings_rows:
    process_data(migration_db, holdings_row, "holdings_id")

print "Processing items:"
query = "select item_id from ole_ds_item_t"
item_rows = queryDB(ole_db, query)
print "Got back",len(item_rows),"rows"
for item_row in item_rows:
    process_data(migration_db, item_row, "item_id")
