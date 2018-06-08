from configparser import ConfigParser
from datetime import datetime
from psycopg2.extras import DictCursor
import logging
import psycopg2
import requests

logger = logging.getLogger('foliolibrary')

class FolioContext:
    def __init__(self):
        cp = ConfigParser()
        cp.read('foliolibrary.ini')
        s = cp['FolioContext']
        self.connection = psycopg2.connect(host=s['host'], port=s['port'], user=s['user'], password=s['password'], database=s['database'])
        self.cursor = self.connection.cursor()

    def any_address_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_users.addresstype', take=1)) is not None

    def truncate_address_types(self):
        self.execute('TRUNCATE TABLE diku_mod_users.addresstype')
        self.commit()

    def find_address_type(self, id):
        return next(self.address_types(where='id = %s', params=(id,)))

    def address_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for at in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_users.addresstype{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield AddressType(id=at[0], content=at[1], creation_time=at[2], creation_user_id=at[3])

    def insert_address_type(self, address_type):
        self.execute('INSERT INTO diku_mod_users.addresstype (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (address_type.id, address_type.content, address_type.creation_time, address_type.creation_user_id))

    def update_address_type(self, address_type):
        self.execute('UPDATE diku_mod_users.addresstype SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (address_type.id, address_type.content, address_type.creation_time, address_type.creation_user_id, address_type.id))

    def delete_address_type(self, address_type):
        self.execute('DELETE FROM diku_mod_users.addresstype WHERE id = %s)', (address_type.id,))

    def any_audit_configurations(self):
        return next(self.query('SELECT 1 FROM diku_mod_configuration.audit_config_data', take=1)) is not None

    def truncate_audit_configurations(self):
        self.execute('TRUNCATE TABLE diku_mod_configuration.audit_config_data')
        self.commit()

    def find_audit_configuration(self, id):
        return next(self.audit_configurations(where='id = %s', params=(id,)))

    def audit_configurations(self, where=None, params=None, order_by=None, skip=None, take=None):
        for ac in self.query(f"SELECT id, orig_id, operation, jsonb AS content, created_date AS creation_time FROM diku_mod_configuration.audit_config_data{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield AuditConfiguration(id=ac[0], orig_id=ac[1], operation=ac[2], content=ac[3], creation_time=ac[4])

    def insert_audit_configuration(self, audit_configuration):
        self.execute('INSERT INTO diku_mod_configuration.audit_config_data (id, orig_id, operation, jsonb, created_date) VALUES (%s, %s, %s, %s, %s)', (audit_configuration.id, audit_configuration.orig_id, audit_configuration.operation, audit_configuration.content, audit_configuration.creation_time))

    def update_audit_configuration(self, audit_configuration):
        self.execute('UPDATE diku_mod_configuration.audit_config_data SET orig_id = %s, operation = %s, jsonb = %s, created_date = %s WHERE id = %s)', (audit_configuration.id, audit_configuration.orig_id, audit_configuration.operation, audit_configuration.content, audit_configuration.creation_time, audit_configuration.id))

    def delete_audit_configuration(self, audit_configuration):
        self.execute('DELETE FROM diku_mod_configuration.audit_config_data WHERE id = %s)', (audit_configuration.id,))

    def any_classification_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.classification_type', take=1)) is not None

    def truncate_classification_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.classification_type')
        self.commit()

    def find_classification_type(self, id):
        return next(self.classification_types(where='id = %s', params=(id,)))

    def classification_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for ct in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.classification_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield ClassificationType(id=ct[0], content=ct[1])

    def insert_classification_type(self, classification_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.classification_type (_id, jsonb) VALUES (%s, %s)', (classification_type.id, classification_type.content))

    def update_classification_type(self, classification_type):
        self.execute('UPDATE diku_mod_inventory_storage.classification_type SET jsonb = %s WHERE _id = %s)', (classification_type.id, classification_type.content, classification_type.id))

    def delete_classification_type(self, classification_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.classification_type WHERE _id = %s)', (classification_type.id,))

    def any_configurations(self):
        return next(self.query('SELECT 1 FROM diku_mod_configuration.config_data', take=1)) is not None

    def truncate_configurations(self):
        self.execute('TRUNCATE TABLE diku_mod_configuration.config_data')
        self.commit()

    def find_configuration(self, id):
        return next(self.configurations(where='id = %s', params=(id,)))

    def configurations(self, where=None, params=None, order_by=None, skip=None, take=None):
        for c in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_configuration.config_data{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Configuration(id=c[0], content=c[1], creation_time=c[2], creation_user_id=c[3])

    def insert_configuration(self, configuration):
        self.execute('INSERT INTO diku_mod_configuration.config_data (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (configuration.id, configuration.content, configuration.creation_time, configuration.creation_user_id))

    def update_configuration(self, configuration):
        self.execute('UPDATE diku_mod_configuration.config_data SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (configuration.id, configuration.content, configuration.creation_time, configuration.creation_user_id, configuration.id))

    def delete_configuration(self, configuration):
        self.execute('DELETE FROM diku_mod_configuration.config_data WHERE id = %s)', (configuration.id,))

    def any_contributor_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.contributor_type', take=1)) is not None

    def truncate_contributor_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.contributor_type')
        self.commit()

    def find_contributor_type(self, id):
        return next(self.contributor_types(where='id = %s', params=(id,)))

    def contributor_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for ct in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.contributor_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield ContributorType(id=ct[0], content=ct[1])

    def insert_contributor_type(self, contributor_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.contributor_type (_id, jsonb) VALUES (%s, %s)', (contributor_type.id, contributor_type.content))

    def update_contributor_type(self, contributor_type):
        self.execute('UPDATE diku_mod_inventory_storage.contributor_type SET jsonb = %s WHERE _id = %s)', (contributor_type.id, contributor_type.content, contributor_type.id))

    def delete_contributor_type(self, contributor_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.contributor_type WHERE _id = %s)', (contributor_type.id,))

    def any_creator_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.creator_type', take=1)) is not None

    def truncate_creator_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.creator_type')
        self.commit()

    def find_creator_type(self, id):
        return next(self.creator_types(where='id = %s', params=(id,)))

    def creator_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for ct in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.creator_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield CreatorType(id=ct[0], content=ct[1])

    def insert_creator_type(self, creator_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.creator_type (_id, jsonb) VALUES (%s, %s)', (creator_type.id, creator_type.content))

    def update_creator_type(self, creator_type):
        self.execute('UPDATE diku_mod_inventory_storage.creator_type SET jsonb = %s WHERE _id = %s)', (creator_type.id, creator_type.content, creator_type.id))

    def delete_creator_type(self, creator_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.creator_type WHERE _id = %s)', (creator_type.id,))

    def any_fixed_due_date_schedules(self):
        return next(self.query('SELECT 1 FROM diku_mod_circulation_storage.fixed_due_date_schedule', take=1)) is not None

    def truncate_fixed_due_date_schedules(self):
        self.execute('TRUNCATE TABLE diku_mod_circulation_storage.fixed_due_date_schedule')
        self.commit()

    def find_fixed_due_date_schedule(self, id):
        return next(self.fixed_due_date_schedules(where='id = %s', params=(id,)))

    def fixed_due_date_schedules(self, where=None, params=None, order_by=None, skip=None, take=None):
        for fdds in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_circulation_storage.fixed_due_date_schedule{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield FixedDueDateSchedule(id=fdds[0], content=fdds[1])

    def insert_fixed_due_date_schedule(self, fixed_due_date_schedule):
        self.execute('INSERT INTO diku_mod_circulation_storage.fixed_due_date_schedule (_id, jsonb) VALUES (%s, %s)', (fixed_due_date_schedule.id, fixed_due_date_schedule.content))

    def update_fixed_due_date_schedule(self, fixed_due_date_schedule):
        self.execute('UPDATE diku_mod_circulation_storage.fixed_due_date_schedule SET jsonb = %s WHERE _id = %s)', (fixed_due_date_schedule.id, fixed_due_date_schedule.content, fixed_due_date_schedule.id))

    def delete_fixed_due_date_schedule(self, fixed_due_date_schedule):
        self.execute('DELETE FROM diku_mod_circulation_storage.fixed_due_date_schedule WHERE _id = %s)', (fixed_due_date_schedule.id,))

    def any_groups(self):
        return next(self.query('SELECT 1 FROM diku_mod_users.groups', take=1)) is not None

    def truncate_groups(self):
        self.execute('TRUNCATE TABLE diku_mod_users.groups')
        self.commit()

    def find_group(self, id):
        return next(self.groups(where='id = %s', params=(id,)))

    def groups(self, where=None, params=None, order_by=None, skip=None, take=None):
        for g in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_users.groups{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Group(id=g[0], content=g[1], creation_time=g[2], creation_user_id=g[3])

    def insert_group(self, group):
        self.execute('INSERT INTO diku_mod_users.groups (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (group.id, group.content, group.creation_time, group.creation_user_id))

    def update_group(self, group):
        self.execute('UPDATE diku_mod_users.groups SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (group.id, group.content, group.creation_time, group.creation_user_id, group.id))

    def delete_group(self, group):
        self.execute('DELETE FROM diku_mod_users.groups WHERE id = %s)', (group.id,))

    def any_holdings(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.holdings_record', take=1)) is not None

    def truncate_holdings(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.holdings_record')
        self.commit()

    def find_holding(self, id):
        return next(self.holdings(where='id = %s', params=(id,)))

    def holdings(self, where=None, params=None, order_by=None, skip=None, take=None):
        for h in self.query(f"SELECT _id AS id, jsonb AS content, permanentlocationid FROM diku_mod_inventory_storage.holdings_record{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Holding(id=h[0], content=h[1], permanentlocationid=h[2])

    def insert_holding(self, holding):
        self.execute('INSERT INTO diku_mod_inventory_storage.holdings_record (_id, jsonb, permanentlocationid) VALUES (%s, %s, %s)', (holding.id, holding.content, holding.permanentlocationid))

    def update_holding(self, holding):
        self.execute('UPDATE diku_mod_inventory_storage.holdings_record SET jsonb = %s, permanentlocationid = %s WHERE _id = %s)', (holding.id, holding.content, holding.permanentlocationid, holding.id))

    def delete_holding(self, holding):
        self.execute('DELETE FROM diku_mod_inventory_storage.holdings_record WHERE _id = %s)', (holding.id,))

    def any_id_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.identifier_type', take=1)) is not None

    def truncate_id_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.identifier_type')
        self.commit()

    def find_id_type(self, id):
        return next(self.id_types(where='id = %s', params=(id,)))

    def id_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for it in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.identifier_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield IdType(id=it[0], content=it[1])

    def insert_id_type(self, id_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.identifier_type (_id, jsonb) VALUES (%s, %s)', (id_type.id, id_type.content))

    def update_id_type(self, id_type):
        self.execute('UPDATE diku_mod_inventory_storage.identifier_type SET jsonb = %s WHERE _id = %s)', (id_type.id, id_type.content, id_type.id))

    def delete_id_type(self, id_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.identifier_type WHERE _id = %s)', (id_type.id,))

    def any_instances(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.instance', take=1)) is not None

    def truncate_instances(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.instance')
        self.commit()

    def find_instance(self, id):
        return next(self.instances(where='id = %s', params=(id,)))

    def instances(self, where=None, params=None, order_by=None, skip=None, take=None):
        for i in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.instance{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Instance(id=i[0], content=i[1])

    def insert_instance(self, instance):
        self.execute('INSERT INTO diku_mod_inventory_storage.instance (_id, jsonb) VALUES (%s, %s)', (instance.id, instance.content))

    def update_instance(self, instance):
        self.execute('UPDATE diku_mod_inventory_storage.instance SET jsonb = %s WHERE _id = %s)', (instance.id, instance.content, instance.id))

    def delete_instance(self, instance):
        self.execute('DELETE FROM diku_mod_inventory_storage.instance WHERE _id = %s)', (instance.id,))

    def any_instance_formats(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.instance_format', take=1)) is not None

    def truncate_instance_formats(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.instance_format')
        self.commit()

    def find_instance_format(self, id):
        return next(self.instance_formats(where='id = %s', params=(id,)))

    def instance_formats(self, where=None, params=None, order_by=None, skip=None, take=None):
        for _if in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.instance_format{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield InstanceFormat(id=_if[0], content=_if[1])

    def insert_instance_format(self, instance_format):
        self.execute('INSERT INTO diku_mod_inventory_storage.instance_format (_id, jsonb) VALUES (%s, %s)', (instance_format.id, instance_format.content))

    def update_instance_format(self, instance_format):
        self.execute('UPDATE diku_mod_inventory_storage.instance_format SET jsonb = %s WHERE _id = %s)', (instance_format.id, instance_format.content, instance_format.id))

    def delete_instance_format(self, instance_format):
        self.execute('DELETE FROM diku_mod_inventory_storage.instance_format WHERE _id = %s)', (instance_format.id,))

    def any_instance_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.instance_type', take=1)) is not None

    def truncate_instance_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.instance_type')
        self.commit()

    def find_instance_type(self, id):
        return next(self.instance_types(where='id = %s', params=(id,)))

    def instance_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for it in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.instance_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield InstanceType(id=it[0], content=it[1])

    def insert_instance_type(self, instance_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.instance_type (_id, jsonb) VALUES (%s, %s)', (instance_type.id, instance_type.content))

    def update_instance_type(self, instance_type):
        self.execute('UPDATE diku_mod_inventory_storage.instance_type SET jsonb = %s WHERE _id = %s)', (instance_type.id, instance_type.content, instance_type.id))

    def delete_instance_type(self, instance_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.instance_type WHERE _id = %s)', (instance_type.id,))

    def any_items(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.item', take=1)) is not None

    def truncate_items(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.item')
        self.commit()

    def find_item(self, id):
        return next(self.items(where='id = %s', params=(id,)))

    def items(self, where=None, params=None, order_by=None, skip=None, take=None):
        for i in self.query(f"SELECT _id AS id, jsonb AS content, permanentloantypeid, temporaryloantypeid, materialtypeid FROM diku_mod_inventory_storage.item{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Item(id=i[0], content=i[1], permanentloantypeid=i[2], temporaryloantypeid=i[3], materialtypeid=i[4])

    def insert_item(self, item):
        self.execute('INSERT INTO diku_mod_inventory_storage.item (_id, jsonb, permanentloantypeid, temporaryloantypeid, materialtypeid) VALUES (%s, %s, %s, %s, %s)', (item.id, item.content, item.permanentloantypeid, item.temporaryloantypeid, item.materialtypeid))

    def update_item(self, item):
        self.execute('UPDATE diku_mod_inventory_storage.item SET jsonb = %s, permanentloantypeid = %s, temporaryloantypeid = %s, materialtypeid = %s WHERE _id = %s)', (item.id, item.content, item.permanentloantypeid, item.temporaryloantypeid, item.materialtypeid, item.id))

    def delete_item(self, item):
        self.execute('DELETE FROM diku_mod_inventory_storage.item WHERE _id = %s)', (item.id,))

    def any_loans(self):
        return next(self.query('SELECT 1 FROM diku_mod_circulation_storage.loan', take=1)) is not None

    def truncate_loans(self):
        self.execute('TRUNCATE TABLE diku_mod_circulation_storage.loan')
        self.commit()

    def find_loan(self, id):
        return next(self.loans(where='id = %s', params=(id,)))

    def loans(self, where=None, params=None, order_by=None, skip=None, take=None):
        for l in self.query(f"SELECT _id AS id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_circulation_storage.loan{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Loan(id=l[0], content=l[1], creation_time=l[2], creation_user_id=l[3])

    def insert_loan(self, loan):
        self.execute('INSERT INTO diku_mod_circulation_storage.loan (_id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (loan.id, loan.content, loan.creation_time, loan.creation_user_id))

    def update_loan(self, loan):
        self.execute('UPDATE diku_mod_circulation_storage.loan SET jsonb = %s, creation_date = %s, created_by = %s WHERE _id = %s)', (loan.id, loan.content, loan.creation_time, loan.creation_user_id, loan.id))

    def delete_loan(self, loan):
        self.execute('DELETE FROM diku_mod_circulation_storage.loan WHERE _id = %s)', (loan.id,))

    def any_loan_policies(self):
        return next(self.query('SELECT 1 FROM diku_mod_circulation_storage.loan_policy', take=1)) is not None

    def truncate_loan_policies(self):
        self.execute('TRUNCATE TABLE diku_mod_circulation_storage.loan_policy')
        self.commit()

    def find_loan_policy(self, id):
        return next(self.loan_policies(where='id = %s', params=(id,)))

    def loan_policies(self, where=None, params=None, order_by=None, skip=None, take=None):
        for lp in self.query(f"SELECT _id AS id, jsonb AS content, fixedduedatescheduleid, alternatefixedduedatescheduleid FROM diku_mod_circulation_storage.loan_policy{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield LoanPolicy(id=lp[0], content=lp[1], fixedduedatescheduleid=lp[2], alternatefixedduedatescheduleid=lp[3])

    def insert_loan_policy(self, loan_policy):
        self.execute('INSERT INTO diku_mod_circulation_storage.loan_policy (_id, jsonb, fixedduedatescheduleid, alternatefixedduedatescheduleid) VALUES (%s, %s, %s, %s)', (loan_policy.id, loan_policy.content, loan_policy.fixedduedatescheduleid, loan_policy.alternatefixedduedatescheduleid))

    def update_loan_policy(self, loan_policy):
        self.execute('UPDATE diku_mod_circulation_storage.loan_policy SET jsonb = %s, fixedduedatescheduleid = %s, alternatefixedduedatescheduleid = %s WHERE _id = %s)', (loan_policy.id, loan_policy.content, loan_policy.fixedduedatescheduleid, loan_policy.alternatefixedduedatescheduleid, loan_policy.id))

    def delete_loan_policy(self, loan_policy):
        self.execute('DELETE FROM diku_mod_circulation_storage.loan_policy WHERE _id = %s)', (loan_policy.id,))

    def any_loan_rules(self):
        return next(self.query('SELECT 1 FROM diku_mod_circulation_storage.loan_rules', take=1)) is not None

    def truncate_loan_rules(self):
        self.execute('TRUNCATE TABLE diku_mod_circulation_storage.loan_rules')
        self.commit()

    def find_loan_rule(self, id):
        return next(self.loan_rules(where='id = %s', params=(id,)))

    def loan_rules(self, where=None, params=None, order_by=None, skip=None, take=None):
        for lr in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_circulation_storage.loan_rules{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield LoanRule(id=lr[0], content=lr[1])

    def insert_loan_rule(self, loan_rule):
        self.execute('INSERT INTO diku_mod_circulation_storage.loan_rules (_id, jsonb) VALUES (%s, %s)', (loan_rule.id, loan_rule.content))

    def update_loan_rule(self, loan_rule):
        self.execute('UPDATE diku_mod_circulation_storage.loan_rules SET jsonb = %s WHERE _id = %s)', (loan_rule.id, loan_rule.content, loan_rule.id))

    def delete_loan_rule(self, loan_rule):
        self.execute('DELETE FROM diku_mod_circulation_storage.loan_rules WHERE _id = %s)', (loan_rule.id,))

    def any_loan_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.loan_type', take=1)) is not None

    def truncate_loan_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.loan_type')
        self.commit()

    def find_loan_type(self, id):
        return next(self.loan_types(where='id = %s', params=(id,)))

    def loan_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for lt in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.loan_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield LoanType(id=lt[0], content=lt[1])

    def insert_loan_type(self, loan_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.loan_type (_id, jsonb) VALUES (%s, %s)', (loan_type.id, loan_type.content))

    def update_loan_type(self, loan_type):
        self.execute('UPDATE diku_mod_inventory_storage.loan_type SET jsonb = %s WHERE _id = %s)', (loan_type.id, loan_type.content, loan_type.id))

    def delete_loan_type(self, loan_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.loan_type WHERE _id = %s)', (loan_type.id,))

    def any_locations(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.shelflocation', take=1)) is not None

    def truncate_locations(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.shelflocation')
        self.commit()

    def find_location(self, id):
        return next(self.locations(where='id = %s', params=(id,)))

    def locations(self, where=None, params=None, order_by=None, skip=None, take=None):
        for l in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.shelflocation{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Location(id=l[0], content=l[1])

    def insert_location(self, location):
        self.execute('INSERT INTO diku_mod_inventory_storage.shelflocation (_id, jsonb) VALUES (%s, %s)', (location.id, location.content))

    def update_location(self, location):
        self.execute('UPDATE diku_mod_inventory_storage.shelflocation SET jsonb = %s WHERE _id = %s)', (location.id, location.content, location.id))

    def delete_location(self, location):
        self.execute('DELETE FROM diku_mod_inventory_storage.shelflocation WHERE _id = %s)', (location.id,))

    def any_logins(self):
        return next(self.query('SELECT 1 FROM diku_mod_login.auth_credentials', take=1)) is not None

    def truncate_logins(self):
        self.execute('TRUNCATE TABLE diku_mod_login.auth_credentials')
        self.commit()

    def find_login(self, id):
        return next(self.logins(where='id = %s', params=(id,)))

    def logins(self, where=None, params=None, order_by=None, skip=None, take=None):
        for l in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_login.auth_credentials{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Login(id=l[0], content=l[1])

    def insert_login(self, login):
        self.execute('INSERT INTO diku_mod_login.auth_credentials (_id, jsonb) VALUES (%s, %s)', (login.id, login.content))

    def update_login(self, login):
        self.execute('UPDATE diku_mod_login.auth_credentials SET jsonb = %s WHERE _id = %s)', (login.id, login.content, login.id))

    def delete_login(self, login):
        self.execute('DELETE FROM diku_mod_login.auth_credentials WHERE _id = %s)', (login.id,))

    def any_material_types(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.material_type', take=1)) is not None

    def truncate_material_types(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.material_type')
        self.commit()

    def find_material_type(self, id):
        return next(self.material_types(where='id = %s', params=(id,)))

    def material_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for mt in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.material_type{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield MaterialType(id=mt[0], content=mt[1])

    def insert_material_type(self, material_type):
        self.execute('INSERT INTO diku_mod_inventory_storage.material_type (_id, jsonb) VALUES (%s, %s)', (material_type.id, material_type.content))

    def update_material_type(self, material_type):
        self.execute('UPDATE diku_mod_inventory_storage.material_type SET jsonb = %s WHERE _id = %s)', (material_type.id, material_type.content, material_type.id))

    def delete_material_type(self, material_type):
        self.execute('DELETE FROM diku_mod_inventory_storage.material_type WHERE _id = %s)', (material_type.id,))

    def any_notes(self):
        return next(self.query('SELECT 1 FROM diku_mod_notes.note_data', take=1)) is not None

    def truncate_notes(self):
        self.execute('TRUNCATE TABLE diku_mod_notes.note_data')
        self.commit()

    def find_note(self, id):
        return next(self.notes(where='id = %s', params=(id,)))

    def notes(self, where=None, params=None, order_by=None, skip=None, take=None):
        for n in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_notes.note_data{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Note(id=n[0], content=n[1], creation_time=n[2], creation_user_id=n[3])

    def insert_note(self, note):
        self.execute('INSERT INTO diku_mod_notes.note_data (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (note.id, note.content, note.creation_time, note.creation_user_id))

    def update_note(self, note):
        self.execute('UPDATE diku_mod_notes.note_data SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (note.id, note.content, note.creation_time, note.creation_user_id, note.id))

    def delete_note(self, note):
        self.execute('DELETE FROM diku_mod_notes.note_data WHERE id = %s)', (note.id,))

    def any_notifications(self):
        return next(self.query('SELECT 1 FROM diku_mod_notify.notify_data', take=1)) is not None

    def truncate_notifications(self):
        self.execute('TRUNCATE TABLE diku_mod_notify.notify_data')
        self.commit()

    def find_notification(self, id):
        return next(self.notifications(where='id = %s', params=(id,)))

    def notifications(self, where=None, params=None, order_by=None, skip=None, take=None):
        for n in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_notify.notify_data{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Notification(id=n[0], content=n[1], creation_time=n[2], creation_user_id=n[3])

    def insert_notification(self, notification):
        self.execute('INSERT INTO diku_mod_notify.notify_data (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (notification.id, notification.content, notification.creation_time, notification.creation_user_id))

    def update_notification(self, notification):
        self.execute('UPDATE diku_mod_notify.notify_data SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (notification.id, notification.content, notification.creation_time, notification.creation_user_id, notification.id))

    def delete_notification(self, notification):
        self.execute('DELETE FROM diku_mod_notify.notify_data WHERE id = %s)', (notification.id,))

    def any_past_loans(self):
        return next(self.query('SELECT 1 FROM diku_mod_circulation_storage.loan_history_table', take=1)) is not None

    def truncate_past_loans(self):
        self.execute('TRUNCATE TABLE diku_mod_circulation_storage.loan_history_table')
        self.commit()

    def find_past_loan(self, id):
        return next(self.past_loans(where='id = %s', params=(id,)))

    def past_loans(self, where=None, params=None, order_by=None, skip=None, take=None):
        for pl in self.query(f"SELECT _id AS id, orig_id, operation, jsonb AS content, created_date AS creation_time FROM diku_mod_circulation_storage.loan_history_table{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield PastLoan(id=pl[0], orig_id=pl[1], operation=pl[2], content=pl[3], creation_time=pl[4])

    def insert_past_loan(self, past_loan):
        self.execute('INSERT INTO diku_mod_circulation_storage.loan_history_table (_id, orig_id, operation, jsonb, created_date) VALUES (%s, %s, %s, %s, %s)', (past_loan.id, past_loan.orig_id, past_loan.operation, past_loan.content, past_loan.creation_time))

    def update_past_loan(self, past_loan):
        self.execute('UPDATE diku_mod_circulation_storage.loan_history_table SET orig_id = %s, operation = %s, jsonb = %s, created_date = %s WHERE _id = %s)', (past_loan.id, past_loan.orig_id, past_loan.operation, past_loan.content, past_loan.creation_time, past_loan.id))

    def delete_past_loan(self, past_loan):
        self.execute('DELETE FROM diku_mod_circulation_storage.loan_history_table WHERE _id = %s)', (past_loan.id,))

    def any_permissions(self):
        return next(self.query('SELECT 1 FROM diku_mod_permissions.permissions', take=1)) is not None

    def truncate_permissions(self):
        self.execute('TRUNCATE TABLE diku_mod_permissions.permissions')
        self.commit()

    def find_permission(self, id):
        return next(self.permissions(where='id = %s', params=(id,)))

    def permissions(self, where=None, params=None, order_by=None, skip=None, take=None):
        for p in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_permissions.permissions{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Permission(id=p[0], content=p[1])

    def insert_permission(self, permission):
        self.execute('INSERT INTO diku_mod_permissions.permissions (_id, jsonb) VALUES (%s, %s)', (permission.id, permission.content))

    def update_permission(self, permission):
        self.execute('UPDATE diku_mod_permissions.permissions SET jsonb = %s WHERE _id = %s)', (permission.id, permission.content, permission.id))

    def delete_permission(self, permission):
        self.execute('DELETE FROM diku_mod_permissions.permissions WHERE _id = %s)', (permission.id,))

    def any_permissions_users(self):
        return next(self.query('SELECT 1 FROM diku_mod_permissions.permissions_users', take=1)) is not None

    def truncate_permissions_users(self):
        self.execute('TRUNCATE TABLE diku_mod_permissions.permissions_users')
        self.commit()

    def find_permissions_user(self, id):
        return next(self.permissions_users(where='id = %s', params=(id,)))

    def permissions_users(self, where=None, params=None, order_by=None, skip=None, take=None):
        for pu in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_permissions.permissions_users{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield PermissionsUser(id=pu[0], content=pu[1])

    def insert_permissions_user(self, permissions_user):
        self.execute('INSERT INTO diku_mod_permissions.permissions_users (_id, jsonb) VALUES (%s, %s)', (permissions_user.id, permissions_user.content))

    def update_permissions_user(self, permissions_user):
        self.execute('UPDATE diku_mod_permissions.permissions_users SET jsonb = %s WHERE _id = %s)', (permissions_user.id, permissions_user.content, permissions_user.id))

    def delete_permissions_user(self, permissions_user):
        self.execute('DELETE FROM diku_mod_permissions.permissions_users WHERE _id = %s)', (permissions_user.id,))

    def any_platforms(self):
        return next(self.query('SELECT 1 FROM diku_mod_inventory_storage.platform', take=1)) is not None

    def truncate_platforms(self):
        self.execute('TRUNCATE TABLE diku_mod_inventory_storage.platform')
        self.commit()

    def find_platform(self, id):
        return next(self.platforms(where='id = %s', params=(id,)))

    def platforms(self, where=None, params=None, order_by=None, skip=None, take=None):
        for p in self.query(f"SELECT _id AS id, jsonb AS content FROM diku_mod_inventory_storage.platform{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Platform(id=p[0], content=p[1])

    def insert_platform(self, platform):
        self.execute('INSERT INTO diku_mod_inventory_storage.platform (_id, jsonb) VALUES (%s, %s)', (platform.id, platform.content))

    def update_platform(self, platform):
        self.execute('UPDATE diku_mod_inventory_storage.platform SET jsonb = %s WHERE _id = %s)', (platform.id, platform.content, platform.id))

    def delete_platform(self, platform):
        self.execute('DELETE FROM diku_mod_inventory_storage.platform WHERE _id = %s)', (platform.id,))

    def any_proxies(self):
        return next(self.query('SELECT 1 FROM diku_mod_users.proxyfor', take=1)) is not None

    def truncate_proxies(self):
        self.execute('TRUNCATE TABLE diku_mod_users.proxyfor')
        self.commit()

    def find_proxy(self, id):
        return next(self.proxies(where='id = %s', params=(id,)))

    def proxies(self, where=None, params=None, order_by=None, skip=None, take=None):
        for p in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_users.proxyfor{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Proxy(id=p[0], content=p[1], creation_time=p[2], creation_user_id=p[3])

    def insert_proxy(self, proxy):
        self.execute('INSERT INTO diku_mod_users.proxyfor (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (proxy.id, proxy.content, proxy.creation_time, proxy.creation_user_id))

    def update_proxy(self, proxy):
        self.execute('UPDATE diku_mod_users.proxyfor SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (proxy.id, proxy.content, proxy.creation_time, proxy.creation_user_id, proxy.id))

    def delete_proxy(self, proxy):
        self.execute('DELETE FROM diku_mod_users.proxyfor WHERE id = %s)', (proxy.id,))

    def any_requests(self):
        return next(self.query('SELECT 1 FROM diku_mod_circulation_storage.request', take=1)) is not None

    def truncate_requests(self):
        self.execute('TRUNCATE TABLE diku_mod_circulation_storage.request')
        self.commit()

    def find_request(self, id):
        return next(self.requests(where='id = %s', params=(id,)))

    def requests(self, where=None, params=None, order_by=None, skip=None, take=None):
        for r in self.query(f"SELECT _id AS id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_circulation_storage.request{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Request(id=r[0], content=r[1], creation_time=r[2], creation_user_id=r[3])

    def insert_request(self, request):
        self.execute('INSERT INTO diku_mod_circulation_storage.request (_id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (request.id, request.content, request.creation_time, request.creation_user_id))

    def update_request(self, request):
        self.execute('UPDATE diku_mod_circulation_storage.request SET jsonb = %s, creation_date = %s, created_by = %s WHERE _id = %s)', (request.id, request.content, request.creation_time, request.creation_user_id, request.id))

    def delete_request(self, request):
        self.execute('DELETE FROM diku_mod_circulation_storage.request WHERE _id = %s)', (request.id,))

    def any_users(self):
        return next(self.query('SELECT 1 FROM diku_mod_users.users', take=1)) is not None

    def truncate_users(self):
        self.execute('TRUNCATE TABLE diku_mod_users.users')
        self.commit()

    def find_user(self, id):
        return next(self.users(where='id = %s', params=(id,)))

    def users(self, where=None, params=None, order_by=None, skip=None, take=None):
        for u in self.query(f"SELECT id, jsonb AS content, creation_date AS creation_time, created_by AS creation_user_id FROM diku_mod_users.users{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield User(id=u[0], content=u[1], creation_time=u[2], creation_user_id=u[3])

    def insert_user(self, user):
        self.execute('INSERT INTO diku_mod_users.users (id, jsonb, creation_date, created_by) VALUES (%s, %s, %s, %s)', (user.id, user.content, user.creation_time, user.creation_user_id))

    def update_user(self, user):
        self.execute('UPDATE diku_mod_users.users SET jsonb = %s, creation_date = %s, created_by = %s WHERE id = %s)', (user.id, user.content, user.creation_time, user.creation_user_id, user.id))

    def delete_user(self, user):
        self.execute('DELETE FROM diku_mod_users.users WHERE id = %s)', (user.id,))

    def execute(self, sql, params=None):
        logger.debug(f'{sql} {params}')
        self.cursor.execute(sql, params)

    def query(self, sql, params=None, skip=None, take=None, dictionary=True):
        try:
            cursor = self.connection.cursor(cursor_factory=DictCursor) if dictionary else self.connection.cursor()
            sql = f"{sql}{'' if take is None else f' LIMIT {take}'}{'' if skip is None else f' OFFSET {skip}'}"
            logger.debug(f'{sql} {params}')
            cursor.execute(sql, params)
            for o in cursor:
                yield o
        finally:
            cursor.close()

    def commit(self):
        self.connection.commit()

    def dispose(self):
        if self.cursor is not None: self.cursor.close()
        if self.connection is not None: self.connection.close()

class AddressType:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'AddressType(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class AuditConfiguration:
    def __init__(self, id=None, orig_id=None, operation=None, content=None, creation_time=None):
        self.id = id
        self.orig_id = orig_id
        self.operation = operation
        self.content = content
        self.creation_time = creation_time

    def __str__(self):
        return f'AuditConfiguration(id = {self.id}, orig_id = {self.orig_id}, operation = {self.operation}, content = {self.content}, creation_time = {self.creation_time})'

class ClassificationType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'ClassificationType(id = {self.id}, content = {self.content})'

class Configuration:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Configuration(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class ContributorType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'ContributorType(id = {self.id}, content = {self.content})'

class CreatorType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'CreatorType(id = {self.id}, content = {self.content})'

class FixedDueDateSchedule:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'FixedDueDateSchedule(id = {self.id}, content = {self.content})'

class Group:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Group(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class Holding:
    def __init__(self, id=None, content=None, permanentlocationid=None):
        self.id = id
        self.content = content
        self.permanentlocationid = permanentlocationid

    def __str__(self):
        return f'Holding(id = {self.id}, content = {self.content}, permanentlocationid = {self.permanentlocationid})'

class IdType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'IdType(id = {self.id}, content = {self.content})'

class Instance:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'Instance(id = {self.id}, content = {self.content})'

class InstanceFormat:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'InstanceFormat(id = {self.id}, content = {self.content})'

class InstanceType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'InstanceType(id = {self.id}, content = {self.content})'

class Item:
    def __init__(self, id=None, content=None, permanentloantypeid=None, temporaryloantypeid=None, materialtypeid=None):
        self.id = id
        self.content = content
        self.permanentloantypeid = permanentloantypeid
        self.temporaryloantypeid = temporaryloantypeid
        self.materialtypeid = materialtypeid

    def __str__(self):
        return f'Item(id = {self.id}, content = {self.content}, permanentloantypeid = {self.permanentloantypeid}, temporaryloantypeid = {self.temporaryloantypeid}, materialtypeid = {self.materialtypeid})'

class Loan:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Loan(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class LoanPolicy:
    def __init__(self, id=None, content=None, fixedduedatescheduleid=None, alternatefixedduedatescheduleid=None):
        self.id = id
        self.content = content
        self.fixedduedatescheduleid = fixedduedatescheduleid
        self.alternatefixedduedatescheduleid = alternatefixedduedatescheduleid

    def __str__(self):
        return f'LoanPolicy(id = {self.id}, content = {self.content}, fixedduedatescheduleid = {self.fixedduedatescheduleid}, alternatefixedduedatescheduleid = {self.alternatefixedduedatescheduleid})'

class LoanRule:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'LoanRule(id = {self.id}, content = {self.content})'

class LoanType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'LoanType(id = {self.id}, content = {self.content})'

class Location:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'Location(id = {self.id}, content = {self.content})'

class Login:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'Login(id = {self.id}, content = {self.content})'

class MaterialType:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'MaterialType(id = {self.id}, content = {self.content})'

class Note:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Note(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class Notification:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Notification(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class PastLoan:
    def __init__(self, id=None, orig_id=None, operation=None, content=None, creation_time=None):
        self.id = id
        self.orig_id = orig_id
        self.operation = operation
        self.content = content
        self.creation_time = creation_time

    def __str__(self):
        return f'PastLoan(id = {self.id}, orig_id = {self.orig_id}, operation = {self.operation}, content = {self.content}, creation_time = {self.creation_time})'

class Permission:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'Permission(id = {self.id}, content = {self.content})'

class PermissionsUser:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'PermissionsUser(id = {self.id}, content = {self.content})'

class Platform:
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content

    def __str__(self):
        return f'Platform(id = {self.id}, content = {self.content})'

class Proxy:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Proxy(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class Request:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'Request(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class User:
    def __init__(self, id=None, content=None, creation_time=None, creation_user_id=None):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.creation_user_id = creation_user_id

    def __str__(self):
        return f'User(id = {self.id}, content = {self.content}, creation_time = {self.creation_time}, creation_user_id = {self.creation_user_id})'

class FolioServiceClient:
    def __init__(self):
        cp = ConfigParser()
        cp.read('foliolibrary.ini')
        s = cp['FolioServiceClient']
        self.url = s['url']
        self.tenant = s['tenant']
        self.access_token = s['access_token']
        self.username = s['username']
        self.password = s['password']
        self.headers = {'Accept': 'application/json, text/plain', 'x-okapi-tenant': self.tenant, 'Content-Type': 'application/json', 'x-okapi-token': self.access_token}

    def authenticate(self):
        dt = datetime.now()
        logger.debug('Authenticating')
        url = f'{self.url}/authn/login'
        logger.debug(url)
        s = json.dumps({'username': self.username, 'password' : self.password})
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        self.access_token = r.headers['x-okapi-token']
        self.headers['x-okapi-token'] = self.access_token
        logger.debug(f'{datetime.now() - dt} elapsed')

    def authenticate_if_necessary(self):
        if self.access_token is None: authenticate()

    def address_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding address types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/addresstypes', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['addressTypes']

    def insert_address_type(self, address_type):
        dt = datetime.now()
        logger.debug('Inserting address type')
        self.authenticate_if_necessary()
        url = f'{self.url}/addresstypes'
        logger.debug(url)
        if 'id' not in address_type: address_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_address_type(self, address_type):
        raise NotImplementedError

    def audit_configurations(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding audit configurations')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/configurations/audit', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['audits']

    def insert_audit_configuration(self, audit_configuration):
        dt = datetime.now()
        logger.debug('Inserting audit configuration')
        self.authenticate_if_necessary()
        url = f'{self.url}/configurations/audit'
        logger.debug(url)
        if 'id' not in audit_configuration: audit_configuration['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_audit_configuration(self, audit_configuration):
        raise NotImplementedError

    def classification_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding classification types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/classification-types', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['classificationTypes']

    def insert_classification_type(self, classification_type):
        dt = datetime.now()
        logger.debug('Inserting classification type')
        self.authenticate_if_necessary()
        url = f'{self.url}/classification-types'
        logger.debug(url)
        if 'id' not in classification_type: classification_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_classification_type(self, classification_type):
        raise NotImplementedError

    def configurations(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding configurations')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/configurations/entries', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['configs']

    def insert_configuration(self, configuration):
        dt = datetime.now()
        logger.debug('Inserting configuration')
        self.authenticate_if_necessary()
        url = f'{self.url}/configurations/entries'
        logger.debug(url)
        if 'id' not in configuration: configuration['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_configuration(self, configuration):
        raise NotImplementedError

    def contributor_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding contributor types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/contributor-types', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['contributorTypes']

    def insert_contributor_type(self, contributor_type):
        dt = datetime.now()
        logger.debug('Inserting contributor type')
        self.authenticate_if_necessary()
        url = f'{self.url}/contributor-types'
        logger.debug(url)
        if 'id' not in contributor_type: contributor_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_contributor_type(self, contributor_type):
        raise NotImplementedError

    def fixed_due_date_schedules(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding fixed due date schedules')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/fixed-due-date-schedule-storage/fixed-due-date-schedules', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['fixedDueDateSchedules']

    def insert_fixed_due_date_schedule(self, fixed_due_date_schedule):
        dt = datetime.now()
        logger.debug('Inserting fixed due date schedule')
        self.authenticate_if_necessary()
        url = f'{self.url}/fixed-due-date-schedule-storage/fixed-due-date-schedules'
        logger.debug(url)
        if 'id' not in fixed_due_date_schedule: fixed_due_date_schedule['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_fixed_due_date_schedule(self, fixed_due_date_schedule):
        raise NotImplementedError

    def groups(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding groups')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/groups', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['usergroups']

    def insert_group(self, group):
        dt = datetime.now()
        logger.debug('Inserting group')
        self.authenticate_if_necessary()
        url = f'{self.url}/groups'
        logger.debug(url)
        if 'id' not in group: group['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_group(self, group):
        raise NotImplementedError

    def holdings(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding holdings')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/holdings-storage/holdings', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['holdingsRecords']

    def insert_holding(self, holding):
        dt = datetime.now()
        logger.debug('Inserting holding')
        self.authenticate_if_necessary()
        url = f'{self.url}/holdings-storage/holdings'
        logger.debug(url)
        if 'id' not in holding: holding['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_holding(self, holding):
        raise NotImplementedError

    def id_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding id types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/identifier-types', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['identifierTypes']

    def insert_id_type(self, id_type):
        dt = datetime.now()
        logger.debug('Inserting id type')
        self.authenticate_if_necessary()
        url = f'{self.url}/identifier-types'
        logger.debug(url)
        if 'id' not in id_type: id_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_id_type(self, id_type):
        raise NotImplementedError

    def instances(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding instances')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/instance-storage/instances', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['instances']

    def insert_instance(self, instance):
        dt = datetime.now()
        logger.debug('Inserting instance')
        self.authenticate_if_necessary()
        url = f'{self.url}/instance-storage/instances'
        logger.debug(url)
        if 'id' not in instance: instance['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_instance(self, instance):
        raise NotImplementedError

    def instance_formats(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding instance formats')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/instance-formats', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['instanceFormats']

    def insert_instance_format(self, instance_format):
        dt = datetime.now()
        logger.debug('Inserting instance format')
        self.authenticate_if_necessary()
        url = f'{self.url}/instance-formats'
        logger.debug(url)
        if 'id' not in instance_format: instance_format['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_instance_format(self, instance_format):
        raise NotImplementedError

    def instance_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding instance types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/instance-types', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['instanceTypes']

    def insert_instance_type(self, instance_type):
        dt = datetime.now()
        logger.debug('Inserting instance type')
        self.authenticate_if_necessary()
        url = f'{self.url}/instance-types'
        logger.debug(url)
        if 'id' not in instance_type: instance_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_instance_type(self, instance_type):
        raise NotImplementedError

    def items(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding items')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/item-storage/items', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['items']

    def insert_item(self, item):
        dt = datetime.now()
        logger.debug('Inserting item')
        self.authenticate_if_necessary()
        url = f'{self.url}/item-storage/items'
        logger.debug(url)
        if 'id' not in item: item['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_item(self, item):
        raise NotImplementedError

    def loans(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding loans')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/loan-storage/loans', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['loans']

    def insert_loan(self, loan):
        dt = datetime.now()
        logger.debug('Inserting loan')
        self.authenticate_if_necessary()
        url = f'{self.url}/loan-storage/loans'
        logger.debug(url)
        if 'id' not in loan: loan['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_loan(self, loan):
        raise NotImplementedError

    def loan_policies(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding loan policies')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/loan-policy-storage/loan-policies', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['loanPolicies']

    def insert_loan_policy(self, loan_policy):
        dt = datetime.now()
        logger.debug('Inserting loan policy')
        self.authenticate_if_necessary()
        url = f'{self.url}/loan-policy-storage/loan-policies'
        logger.debug(url)
        if 'id' not in loan_policy: loan_policy['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_loan_policy(self, loan_policy):
        raise NotImplementedError

    def loan_rules(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding loan rules')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/loan-rules-storage', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def insert_loan_rule(self, loan_rule):
        dt = datetime.now()
        logger.debug('Inserting loan rule')
        self.authenticate_if_necessary()
        url = f'{self.url}/loan-rules-storage'
        logger.debug(url)
        if 'id' not in loan_rule: loan_rule['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_loan_rule(self, loan_rule):
        raise NotImplementedError

    def loan_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding loan types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/loan-types', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['loantypes']

    def insert_loan_type(self, loan_type):
        dt = datetime.now()
        logger.debug('Inserting loan type')
        self.authenticate_if_necessary()
        url = f'{self.url}/loan-types'
        logger.debug(url)
        if 'id' not in loan_type: loan_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_loan_type(self, loan_type):
        raise NotImplementedError

    def locations(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding locations')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/locations', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['locations']

    def insert_location(self, location):
        dt = datetime.now()
        logger.debug('Inserting location')
        self.authenticate_if_necessary()
        url = f'{self.url}/locations'
        logger.debug(url)
        if 'id' not in location: location['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_location(self, location):
        raise NotImplementedError

    def logins(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding logins')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/authn/credentials', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['credentials']

    def insert_login(self, login):
        dt = datetime.now()
        logger.debug('Inserting login')
        self.authenticate_if_necessary()
        url = f'{self.url}/authn/credentials'
        logger.debug(url)
        if 'id' not in login: login['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_login(self, login):
        raise NotImplementedError

    def material_types(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding material types')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/material-types', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['mtypes']

    def insert_material_type(self, material_type):
        dt = datetime.now()
        logger.debug('Inserting material type')
        self.authenticate_if_necessary()
        url = f'{self.url}/material-types'
        logger.debug(url)
        if 'id' not in material_type: material_type['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_material_type(self, material_type):
        raise NotImplementedError

    def notes(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding notes')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/notes', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['notes']

    def insert_note(self, note):
        dt = datetime.now()
        logger.debug('Inserting note')
        self.authenticate_if_necessary()
        url = f'{self.url}/notes'
        logger.debug(url)
        if 'id' not in note: note['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_note(self, note):
        raise NotImplementedError

    def notifications(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding notifications')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/notify', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['notifications']

    def insert_notification(self, notification):
        dt = datetime.now()
        logger.debug('Inserting notification')
        self.authenticate_if_necessary()
        url = f'{self.url}/notify'
        logger.debug(url)
        if 'id' not in notification: notification['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_notification(self, notification):
        raise NotImplementedError

    def past_loans(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding past loans')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/loan-storage/loan-history', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['loans']

    def insert_past_loan(self, past_loan):
        dt = datetime.now()
        logger.debug('Inserting past loan')
        self.authenticate_if_necessary()
        url = f'{self.url}/loan-storage/loan-history'
        logger.debug(url)
        if 'id' not in past_loan: past_loan['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_past_loan(self, past_loan):
        raise NotImplementedError

    def permissions(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding permissions')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/perms/permissions', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['permissions']

    def insert_permission(self, permission):
        dt = datetime.now()
        logger.debug('Inserting permission')
        self.authenticate_if_necessary()
        url = f'{self.url}/perms/permissions'
        logger.debug(url)
        if 'id' not in permission: permission['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_permission(self, permission):
        raise NotImplementedError

    def permissions_users(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding permissions users')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/perms/users', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['permissionUsers']

    def insert_permissions_user(self, permissions_user):
        dt = datetime.now()
        logger.debug('Inserting permissions user')
        self.authenticate_if_necessary()
        url = f'{self.url}/perms/users'
        logger.debug(url)
        if 'id' not in permissions_user: permissions_user['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_permissions_user(self, permissions_user):
        raise NotImplementedError

    def platforms(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding platforms')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/platforms', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['platforms']

    def insert_platform(self, platform):
        dt = datetime.now()
        logger.debug('Inserting platform')
        self.authenticate_if_necessary()
        url = f'{self.url}/platforms'
        logger.debug(url)
        if 'id' not in platform: platform['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_platform(self, platform):
        raise NotImplementedError

    def proxies(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding proxies')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/proxiesfor', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['proxiesFor']

    def insert_proxy(self, proxy):
        dt = datetime.now()
        logger.debug('Inserting proxy')
        self.authenticate_if_necessary()
        url = f'{self.url}/proxiesfor'
        logger.debug(url)
        if 'id' not in proxy: proxy['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_proxy(self, proxy):
        raise NotImplementedError

    def requests(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding requests')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/request-storage/requests', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['requests']

    def insert_request(self, request):
        dt = datetime.now()
        logger.debug('Inserting request')
        self.authenticate_if_necessary()
        url = f'{self.url}/request-storage/requests'
        logger.debug(url)
        if 'id' not in request: request['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_request(self, request):
        raise NotImplementedError

    def users(self, where=None, order_by=None, skip=None, take = 100):
        dt = datetime.now()
        logger.debug('Finding users')
        self.authenticate_if_necessary()
        r = requests.get(f'{self.url}/users', [('query', None if where is None and order_by is None else where + ('' if order_by is None else f' sortby {order_by}')), ('offset', skip), ('limit', take)], headers=self.headers)
        logger.debug(r.url)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()['users']

    def insert_user(self, user):
        dt = datetime.now()
        logger.debug('Inserting user')
        self.authenticate_if_necessary()
        url = f'{self.url}/users'
        logger.debug(url)
        if 'id' not in user: user['id'] = str(uuid.uuid4())
        s = json.dumps(user)
        logger.debug(s)
        r = requests.post(url, s, headers=self.headers)
        logger.debug(r)
        if not r.ok: raise Exception(f'{r.status_code} {r.reason} {r.text}')
        logger.debug(r.text)
        logger.debug(f'{datetime.now() - dt} elapsed')
        return r.json()

    def delete_user(self, user):
        raise NotImplementedError
