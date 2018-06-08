from configparser import ConfigParser
from datetime import datetime
import logging
import mysql.connector
import requests

logger = logging.getLogger('olelibrary')

class OleContext:
    def __init__(self):
        cp = ConfigParser()
        cp.read('olelibrary.ini')
        s = cp['OleContext']
        self.connection = mysql.connector.connect(host=s['host'], port=s['port'], user=s['user'], password=s['password'], database=s['database'])

    def any_address_types(self):
        return next(self.query('SELECT 1 FROM krim_addr_typ_t', take=1)) is not None

    def find_address_type(self, code):
        return next(self.address_types(where='code = %s', params=(code,)))

    def address_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for at in self.query(f"SELECT addr_typ_cd AS code, obj_id AS guid, ver_nbr AS version, nm AS name, actv_ind AS active, display_sort_cd AS `order`, last_updt_dt AS last_write_time FROM krim_addr_typ_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield AddressType(code=at[0], guid=at[1], version=at[2], name=at[3], active=at[4], order=at[5], last_write_time=at[6])

    def any_bibs(self):
        return next(self.query('SELECT 1 FROM ole_ds_bib_t', take=1)) is not None

    def find_bib(self, id):
        return next(self.bibs(where='id = %s', params=(id,)))

    def bibs(self, where=None, params=None, order_by=None, skip=None, take=None):
        for b in self.query(f"SELECT bib_id AS id, former_id, fast_add, staff_only, created_by AS creation_user_name, date_created AS creation_time, updated_by AS last_write_user_name, date_updated AS last_write_time, status, status_updated_by AS status_last_write_user_name, status_updated_date AS status_last_write_time, unique_id_prefix AS id_prefix, content FROM ole_ds_bib_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Bib(id=b[0], former_id=b[1], fast_add=b[2], staff_only=b[3], creation_user_name=b[4], creation_time=b[5], last_write_user_name=b[6], last_write_time=b[7], status=b[8], status_last_write_user_name=b[9], status_last_write_time=b[10], id_prefix=b[11], content=b[12])

    def any_email_addresses(self):
        return next(self.query('SELECT 1 FROM krim_entity_email_t', take=1)) is not None

    def find_email_address(self, id):
        return next(self.email_addresses(where='id = %s', params=(id,)))

    def email_addresses(self, where=None, params=None, order_by=None, skip=None, take=None):
        for ea in self.query(f"SELECT entity_email_id AS id, obj_id AS guid, ver_nbr AS version, ent_typ_cd AS person_type_code, entity_id AS person_id, email_typ_cd AS email_address_type_code, email_addr AS address, dflt_ind AS _default, actv_ind AS active, last_updt_dt AS last_write_time FROM krim_entity_email_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield EmailAddress(id=ea[0], guid=ea[1], version=ea[2], person_type_code=ea[3], person_id=ea[4], email_address_type_code=ea[5], address=ea[6], _default=ea[7], active=ea[8], last_write_time=ea[9])

    def any_holdings(self):
        return next(self.query('SELECT 1 FROM ole_ds_holdings_t', take=1)) is not None

    def find_holding(self, id):
        return next(self.holdings(where='id = %s', params=(id,)))

    def holdings(self, where=None, params=None, order_by=None, skip=None, take=None):
        for h in self.query(f"SELECT holdings_id AS id, bib_id, holdings_type AS type, former_holdings_id AS former_id, staff_only, location_id, location AS location_path, location_level, call_number_type_id, call_number_prefix, call_number, shelving_order, copy_number, receipt_status_id, publisher, access_status, access_status_date_updated AS access_status_last_write_time, subscription_status, platform, imprint, local_persistent_uri, allow_ill, authentication_type_id, proxied_resource, number_simult_users AS max_users, e_resource_id, admin_url, admin_username AS admin_user_name, admin_password, access_username AS access_user_name, access_password, unique_id_prefix AS id_prefix, source_holdings_content AS content, initial_sbrcptn_start_dt AS first_subscription_start_date, current_sbrcptn_start_dt AS current_subscription_start_date, current_sbrcptn_end_dt AS current_subscription_end_date, cancellation_decision_dt AS cancellation_decision_date, cancellation_effective_dt AS cancellation_date, cancellation_reason AS cancellation_notes, gokb_identifier AS gokb_id, cancellation_candidate AS is_cancellation_candidate, materials_specified, first_indicator, second_indicator, created_by AS creation_user_name, date_created AS creation_time, updated_by AS last_write_user_name, date_updated AS last_write_time FROM ole_ds_holdings_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Holding(id=h[0], bib_id=h[1], type=h[2], former_id=h[3], staff_only=h[4], location_id=h[5], location_path=h[6], location_level=h[7], call_number_type_id=h[8], call_number_prefix=h[9], call_number=h[10], shelving_order=h[11], copy_number=h[12], receipt_status_id=h[13], publisher=h[14], access_status=h[15], access_status_last_write_time=h[16], subscription_status=h[17], platform=h[18], imprint=h[19], local_persistent_uri=h[20], allow_ill=h[21], authentication_type_id=h[22], proxied_resource=h[23], max_users=h[24], e_resource_id=h[25], admin_url=h[26], admin_user_name=h[27], admin_password=h[28], access_user_name=h[29], access_password=h[30], id_prefix=h[31], content=h[32], first_subscription_start_date=h[33], current_subscription_start_date=h[34], current_subscription_end_date=h[35], cancellation_decision_date=h[36], cancellation_date=h[37], cancellation_notes=h[38], gokb_id=h[39], is_cancellation_candidate=h[40], materials_specified=h[41], first_indicator=h[42], second_indicator=h[43], creation_user_name=h[44], creation_time=h[45], last_write_user_name=h[46], last_write_time=h[47])

    def any_items(self):
        return next(self.query('SELECT 1 FROM ole_ds_item_t', take=1)) is not None

    def find_item(self, id):
        return next(self.items(where='id = %s', params=(id,)))

    def items(self, where=None, params=None, order_by=None, skip=None, take=None):
        for i in self.query(f"SELECT item_id AS id, holdings_id AS holding_id, barcode, fast_add, staff_only, uri, item_type_id, temp_item_type_id, item_status_id, item_status_date_updated AS item_status_last_write_time, location_id, location AS location_path, location_level, call_number_type_id, call_number_prefix, call_number, shelving_order, enumeration, chronology, copy_number, num_pieces AS piece_count, desc_of_pieces AS pieces_description, purchase_order_line_item_id AS order_number, vendor_line_item_id AS vendor_item_id, fund, price, claims_returned, claims_returned_date_created AS claims_returned_time, claims_returned_note AS claims_returned_notes, current_borrower AS patron_id, proxy_borrower AS proxy_patron_id, check_out_date_time AS check_out_time, due_date_time AS due_time, check_in_note AS check_in_notes, item_damaged_status AS is_damaged, item_damaged_note AS damaged_notes, missing_pieces AS is_missing_pieces, missing_pieces_effective_date AS missing_pieces_date, missing_pieces_count, missing_pieces_note AS missing_pieces_notes, barcode_arsl AS arsl_barcode, high_density_storage_id, num_of_renew AS renewal_count, created_by AS creation_user_name, date_created AS creation_time, updated_by AS last_write_user_name, date_updated AS last_write_time, unique_id_prefix AS id_prefix, org_due_date_time AS original_due_time, volume_number FROM ole_ds_item_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Item(id=i[0], holding_id=i[1], barcode=i[2], fast_add=i[3], staff_only=i[4], uri=i[5], item_type_id=i[6], temp_item_type_id=i[7], item_status_id=i[8], item_status_last_write_time=i[9], location_id=i[10], location_path=i[11], location_level=i[12], call_number_type_id=i[13], call_number_prefix=i[14], call_number=i[15], shelving_order=i[16], enumeration=i[17], chronology=i[18], copy_number=i[19], piece_count=i[20], pieces_description=i[21], order_number=i[22], vendor_item_id=i[23], fund=i[24], price=i[25], claims_returned=i[26], claims_returned_time=i[27], claims_returned_notes=i[28], patron_id=i[29], proxy_patron_id=i[30], check_out_time=i[31], due_time=i[32], check_in_notes=i[33], is_damaged=i[34], damaged_notes=i[35], is_missing_pieces=i[36], missing_pieces_date=i[37], missing_pieces_count=i[38], missing_pieces_notes=i[39], arsl_barcode=i[40], high_density_storage_id=i[41], renewal_count=i[42], creation_user_name=i[43], creation_time=i[44], last_write_user_name=i[45], last_write_time=i[46], id_prefix=i[47], original_due_time=i[48], volume_number=i[49])

    def any_names(self):
        return next(self.query('SELECT 1 FROM krim_entity_nm_t', take=1)) is not None

    def find_name(self, id):
        return next(self.names(where='id = %s', params=(id,)))

    def names(self, where=None, params=None, order_by=None, skip=None, take=None):
        for n in self.query(f"SELECT entity_nm_id AS id, obj_id AS guid, ver_nbr AS version, entity_id AS person_id, nm_typ_cd AS name_type_code, first_nm AS first_name, middle_nm AS middle_name, last_nm AS last_name, suffix_nm AS suffix, prefix_nm AS prefix, dflt_ind AS _default, actv_ind AS active, last_updt_dt AS last_write_time, title_nm AS title, note_msg AS notes, nm_chng_dt AS changed_date FROM krim_entity_nm_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Name(id=n[0], guid=n[1], version=n[2], person_id=n[3], name_type_code=n[4], first_name=n[5], middle_name=n[6], last_name=n[7], suffix=n[8], prefix=n[9], _default=n[10], active=n[11], last_write_time=n[12], title=n[13], notes=n[14], changed_date=n[15])

    def any_patrons(self):
        return next(self.query('SELECT 1 FROM ole_ptrn_t', take=1)) is not None

    def find_patron(self, id):
        return next(self.patrons(where='id = %s', params=(id,)))

    def patrons(self, where=None, params=None, order_by=None, skip=None, take=None):
        for p in self.query(f"SELECT ole_ptrn_id AS id, obj_id AS guid, ver_nbr AS version, barcode AS library_id, borr_typ AS patron_type_id, actv_ind AS active, general_block, paging_privilege, courtesy_notice, delivery_privilege, expiration_date AS end_date, activation_date AS start_date, general_block_nt AS general_block_notes, inv_barcode_num AS invalid_barcode, inv_barcode_num_eff_date AS invalid_barcode_start_date, ole_src AS source_id, ole_stat_cat AS patron_category_id, photograph FROM ole_ptrn_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Patron(id=p[0], guid=p[1], version=p[2], library_id=p[3], patron_type_id=p[4], active=p[5], general_block=p[6], paging_privilege=p[7], courtesy_notice=p[8], delivery_privilege=p[9], end_date=p[10], start_date=p[11], general_block_notes=p[12], invalid_barcode=p[13], invalid_barcode_start_date=p[14], source_id=p[15], patron_category_id=p[16], photograph=p[17])

    def any_patron_id1s(self):
        return next(self.query('SELECT 1 FROM ole_ptrn_local_id_t', take=1)) is not None

    def find_patron_id1(self, id):
        return next(self.patron_id1s(where='id = %s', params=(id,)))

    def patron_id1s(self, where=None, params=None, order_by=None, skip=None, take=None):
        for pi1 in self.query(f"SELECT ole_ptrn_local_seq_id AS id, obj_id AS guid, ver_nbr AS version, ole_ptrn_id AS patron_id, local_id AS value FROM ole_ptrn_local_id_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield PatronId1(id=pi1[0], guid=pi1[1], version=pi1[2], patron_id=pi1[3], value=pi1[4])

    def any_patron_types(self):
        return next(self.query('SELECT 1 FROM ole_dlvr_borr_typ_t', take=1)) is not None

    def find_patron_type(self, id):
        return next(self.patron_types(where='id = %s', params=(id,)))

    def patron_types(self, where=None, params=None, order_by=None, skip=None, take=None):
        for pt in self.query(f"SELECT dlvr_borr_typ_id AS id, dlvr_borr_typ_cd AS code, dlvr_borr_typ_desc AS description, dlvr_borr_typ_nm AS name, obj_id AS guid, ver_nbr AS version, row_act_ind AS active FROM ole_dlvr_borr_typ_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield PatronType(id=pt[0], code=pt[1], description=pt[2], name=pt[3], guid=pt[4], version=pt[5], active=pt[6])

    def any_people(self):
        return next(self.query('SELECT 1 FROM krim_entity_t', take=1)) is not None

    def find_person(self, id):
        return next(self.people(where='id = %s', params=(id,)))

    def people(self, where=None, params=None, order_by=None, skip=None, take=None):
        for p in self.query(f"SELECT entity_id AS id, obj_id AS guid, ver_nbr AS version, actv_ind AS active, last_updt_dt AS last_write_time FROM krim_entity_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield Person(id=p[0], guid=p[1], version=p[2], active=p[3], last_write_time=p[4])

    def any_users(self):
        return next(self.query('SELECT 1 FROM krim_prncpl_t', take=1)) is not None

    def find_user(self, id):
        return next(self.users(where='id = %s', params=(id,)))

    def users(self, where=None, params=None, order_by=None, skip=None, take=None):
        for u in self.query(f"SELECT prncpl_id AS id, obj_id AS guid, ver_nbr AS version, prncpl_nm AS user_name, entity_id AS person_id, prncpl_pswd AS password, actv_ind AS active, last_updt_dt AS last_write_time FROM krim_prncpl_t{'' if where is None else f' WHERE {where}'}{'' if order_by is None else f' ORDER BY {order_by}'}", params, skip, take, False):
            yield User(id=u[0], guid=u[1], version=u[2], user_name=u[3], person_id=u[4], password=u[5], active=u[6], last_write_time=u[7])

    def query(self, sql, params=None, skip=None, take=None, dictionary=True):
        try:
            cursor = self.connection.cursor(dictionary=dictionary)
            sql = f"{sql}{'' if skip is None and take is None else f' LIMIT {take}' if skip is None else f' LIMIT {skip}, {take or 2147483648}'}"
            logger.debug(f'{sql} {params}')
            cursor.execute(sql, params)
            for o in cursor:
                yield o
        finally:
            cursor.close()

    def dispose(self):
        if self.connection is not None: self.connection.close()

class AddressType:
    def __init__(self, code=None, guid=None, version=None, name=None, active=None, order=None, last_write_time=None):
        self.code = code
        self.guid = guid
        self.version = version
        self.name = name
        self.active = active
        self.order = order
        self.last_write_time = last_write_time

    def __str__(self):
        return f'AddressType(code = {self.code}, guid = {self.guid}, version = {self.version}, name = {self.name}, active = {self.active}, order = {self.order}, last_write_time = {self.last_write_time})'

class Bib:
    def __init__(self, id=None, former_id=None, fast_add=None, staff_only=None, creation_user_name=None, creation_time=None, last_write_user_name=None, last_write_time=None, status=None, status_last_write_user_name=None, status_last_write_time=None, id_prefix=None, content=None):
        self.id = id
        self.former_id = former_id
        self.fast_add = fast_add
        self.staff_only = staff_only
        self.creation_user_name = creation_user_name
        self.creation_time = creation_time
        self.last_write_user_name = last_write_user_name
        self.last_write_time = last_write_time
        self.status = status
        self.status_last_write_user_name = status_last_write_user_name
        self.status_last_write_time = status_last_write_time
        self.id_prefix = id_prefix
        self.content = content

    def __str__(self):
        return f'Bib(id = {self.id}, former_id = {self.former_id}, fast_add = {self.fast_add}, staff_only = {self.staff_only}, creation_user_name = {self.creation_user_name}, creation_time = {self.creation_time}, last_write_user_name = {self.last_write_user_name}, last_write_time = {self.last_write_time}, status = {self.status}, status_last_write_user_name = {self.status_last_write_user_name}, status_last_write_time = {self.status_last_write_time}, id_prefix = {self.id_prefix}, content = {self.content})'

class EmailAddress:
    def __init__(self, id=None, guid=None, version=None, person_type_code=None, person_id=None, email_address_type_code=None, address=None, _default=None, active=None, last_write_time=None):
        self.id = id
        self.guid = guid
        self.version = version
        self.person_type_code = person_type_code
        self.person_id = person_id
        self.email_address_type_code = email_address_type_code
        self.address = address
        self._default = _default
        self.active = active
        self.last_write_time = last_write_time

    def __str__(self):
        return f'EmailAddress(id = {self.id}, guid = {self.guid}, version = {self.version}, person_type_code = {self.person_type_code}, person_id = {self.person_id}, email_address_type_code = {self.email_address_type_code}, address = {self.address}, _default = {self._default}, active = {self.active}, last_write_time = {self.last_write_time})'

class Holding:
    def __init__(self, id=None, bib_id=None, type=None, former_id=None, staff_only=None, location_id=None, location_path=None, location_level=None, call_number_type_id=None, call_number_prefix=None, call_number=None, shelving_order=None, copy_number=None, receipt_status_id=None, publisher=None, access_status=None, access_status_last_write_time=None, subscription_status=None, platform=None, imprint=None, local_persistent_uri=None, allow_ill=None, authentication_type_id=None, proxied_resource=None, max_users=None, e_resource_id=None, admin_url=None, admin_user_name=None, admin_password=None, access_user_name=None, access_password=None, id_prefix=None, content=None, first_subscription_start_date=None, current_subscription_start_date=None, current_subscription_end_date=None, cancellation_decision_date=None, cancellation_date=None, cancellation_notes=None, gokb_id=None, is_cancellation_candidate=None, materials_specified=None, first_indicator=None, second_indicator=None, creation_user_name=None, creation_time=None, last_write_user_name=None, last_write_time=None):
        self.id = id
        self.bib_id = bib_id
        self.type = type
        self.former_id = former_id
        self.staff_only = staff_only
        self.location_id = location_id
        self.location_path = location_path
        self.location_level = location_level
        self.call_number_type_id = call_number_type_id
        self.call_number_prefix = call_number_prefix
        self.call_number = call_number
        self.shelving_order = shelving_order
        self.copy_number = copy_number
        self.receipt_status_id = receipt_status_id
        self.publisher = publisher
        self.access_status = access_status
        self.access_status_last_write_time = access_status_last_write_time
        self.subscription_status = subscription_status
        self.platform = platform
        self.imprint = imprint
        self.local_persistent_uri = local_persistent_uri
        self.allow_ill = allow_ill
        self.authentication_type_id = authentication_type_id
        self.proxied_resource = proxied_resource
        self.max_users = max_users
        self.e_resource_id = e_resource_id
        self.admin_url = admin_url
        self.admin_user_name = admin_user_name
        self.admin_password = admin_password
        self.access_user_name = access_user_name
        self.access_password = access_password
        self.id_prefix = id_prefix
        self.content = content
        self.first_subscription_start_date = first_subscription_start_date
        self.current_subscription_start_date = current_subscription_start_date
        self.current_subscription_end_date = current_subscription_end_date
        self.cancellation_decision_date = cancellation_decision_date
        self.cancellation_date = cancellation_date
        self.cancellation_notes = cancellation_notes
        self.gokb_id = gokb_id
        self.is_cancellation_candidate = is_cancellation_candidate
        self.materials_specified = materials_specified
        self.first_indicator = first_indicator
        self.second_indicator = second_indicator
        self.creation_user_name = creation_user_name
        self.creation_time = creation_time
        self.last_write_user_name = last_write_user_name
        self.last_write_time = last_write_time

    def __str__(self):
        return f'Holding(id = {self.id}, bib_id = {self.bib_id}, type = {self.type}, former_id = {self.former_id}, staff_only = {self.staff_only}, location_id = {self.location_id}, location_path = {self.location_path}, location_level = {self.location_level}, call_number_type_id = {self.call_number_type_id}, call_number_prefix = {self.call_number_prefix}, call_number = {self.call_number}, shelving_order = {self.shelving_order}, copy_number = {self.copy_number}, receipt_status_id = {self.receipt_status_id}, publisher = {self.publisher}, access_status = {self.access_status}, access_status_last_write_time = {self.access_status_last_write_time}, subscription_status = {self.subscription_status}, platform = {self.platform}, imprint = {self.imprint}, local_persistent_uri = {self.local_persistent_uri}, allow_ill = {self.allow_ill}, authentication_type_id = {self.authentication_type_id}, proxied_resource = {self.proxied_resource}, max_users = {self.max_users}, e_resource_id = {self.e_resource_id}, admin_url = {self.admin_url}, admin_user_name = {self.admin_user_name}, admin_password = {self.admin_password}, access_user_name = {self.access_user_name}, access_password = {self.access_password}, id_prefix = {self.id_prefix}, content = {self.content}, first_subscription_start_date = {self.first_subscription_start_date}, current_subscription_start_date = {self.current_subscription_start_date}, current_subscription_end_date = {self.current_subscription_end_date}, cancellation_decision_date = {self.cancellation_decision_date}, cancellation_date = {self.cancellation_date}, cancellation_notes = {self.cancellation_notes}, gokb_id = {self.gokb_id}, is_cancellation_candidate = {self.is_cancellation_candidate}, materials_specified = {self.materials_specified}, first_indicator = {self.first_indicator}, second_indicator = {self.second_indicator}, creation_user_name = {self.creation_user_name}, creation_time = {self.creation_time}, last_write_user_name = {self.last_write_user_name}, last_write_time = {self.last_write_time})'

class Item:
    def __init__(self, id=None, holding_id=None, barcode=None, fast_add=None, staff_only=None, uri=None, item_type_id=None, temp_item_type_id=None, item_status_id=None, item_status_last_write_time=None, location_id=None, location_path=None, location_level=None, call_number_type_id=None, call_number_prefix=None, call_number=None, shelving_order=None, enumeration=None, chronology=None, copy_number=None, piece_count=None, pieces_description=None, order_number=None, vendor_item_id=None, fund=None, price=None, claims_returned=None, claims_returned_time=None, claims_returned_notes=None, patron_id=None, proxy_patron_id=None, check_out_time=None, due_time=None, check_in_notes=None, is_damaged=None, damaged_notes=None, is_missing_pieces=None, missing_pieces_date=None, missing_pieces_count=None, missing_pieces_notes=None, arsl_barcode=None, high_density_storage_id=None, renewal_count=None, creation_user_name=None, creation_time=None, last_write_user_name=None, last_write_time=None, id_prefix=None, original_due_time=None, volume_number=None):
        self.id = id
        self.holding_id = holding_id
        self.barcode = barcode
        self.fast_add = fast_add
        self.staff_only = staff_only
        self.uri = uri
        self.item_type_id = item_type_id
        self.temp_item_type_id = temp_item_type_id
        self.item_status_id = item_status_id
        self.item_status_last_write_time = item_status_last_write_time
        self.location_id = location_id
        self.location_path = location_path
        self.location_level = location_level
        self.call_number_type_id = call_number_type_id
        self.call_number_prefix = call_number_prefix
        self.call_number = call_number
        self.shelving_order = shelving_order
        self.enumeration = enumeration
        self.chronology = chronology
        self.copy_number = copy_number
        self.piece_count = piece_count
        self.pieces_description = pieces_description
        self.order_number = order_number
        self.vendor_item_id = vendor_item_id
        self.fund = fund
        self.price = price
        self.claims_returned = claims_returned
        self.claims_returned_time = claims_returned_time
        self.claims_returned_notes = claims_returned_notes
        self.patron_id = patron_id
        self.proxy_patron_id = proxy_patron_id
        self.check_out_time = check_out_time
        self.due_time = due_time
        self.check_in_notes = check_in_notes
        self.is_damaged = is_damaged
        self.damaged_notes = damaged_notes
        self.is_missing_pieces = is_missing_pieces
        self.missing_pieces_date = missing_pieces_date
        self.missing_pieces_count = missing_pieces_count
        self.missing_pieces_notes = missing_pieces_notes
        self.arsl_barcode = arsl_barcode
        self.high_density_storage_id = high_density_storage_id
        self.renewal_count = renewal_count
        self.creation_user_name = creation_user_name
        self.creation_time = creation_time
        self.last_write_user_name = last_write_user_name
        self.last_write_time = last_write_time
        self.id_prefix = id_prefix
        self.original_due_time = original_due_time
        self.volume_number = volume_number

    def __str__(self):
        return f'Item(id = {self.id}, holding_id = {self.holding_id}, barcode = {self.barcode}, fast_add = {self.fast_add}, staff_only = {self.staff_only}, uri = {self.uri}, item_type_id = {self.item_type_id}, temp_item_type_id = {self.temp_item_type_id}, item_status_id = {self.item_status_id}, item_status_last_write_time = {self.item_status_last_write_time}, location_id = {self.location_id}, location_path = {self.location_path}, location_level = {self.location_level}, call_number_type_id = {self.call_number_type_id}, call_number_prefix = {self.call_number_prefix}, call_number = {self.call_number}, shelving_order = {self.shelving_order}, enumeration = {self.enumeration}, chronology = {self.chronology}, copy_number = {self.copy_number}, piece_count = {self.piece_count}, pieces_description = {self.pieces_description}, order_number = {self.order_number}, vendor_item_id = {self.vendor_item_id}, fund = {self.fund}, price = {self.price}, claims_returned = {self.claims_returned}, claims_returned_time = {self.claims_returned_time}, claims_returned_notes = {self.claims_returned_notes}, patron_id = {self.patron_id}, proxy_patron_id = {self.proxy_patron_id}, check_out_time = {self.check_out_time}, due_time = {self.due_time}, check_in_notes = {self.check_in_notes}, is_damaged = {self.is_damaged}, damaged_notes = {self.damaged_notes}, is_missing_pieces = {self.is_missing_pieces}, missing_pieces_date = {self.missing_pieces_date}, missing_pieces_count = {self.missing_pieces_count}, missing_pieces_notes = {self.missing_pieces_notes}, arsl_barcode = {self.arsl_barcode}, high_density_storage_id = {self.high_density_storage_id}, renewal_count = {self.renewal_count}, creation_user_name = {self.creation_user_name}, creation_time = {self.creation_time}, last_write_user_name = {self.last_write_user_name}, last_write_time = {self.last_write_time}, id_prefix = {self.id_prefix}, original_due_time = {self.original_due_time}, volume_number = {self.volume_number})'

class Name:
    def __init__(self, id=None, guid=None, version=None, person_id=None, name_type_code=None, first_name=None, middle_name=None, last_name=None, suffix=None, prefix=None, _default=None, active=None, last_write_time=None, title=None, notes=None, changed_date=None):
        self.id = id
        self.guid = guid
        self.version = version
        self.person_id = person_id
        self.name_type_code = name_type_code
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix
        self.prefix = prefix
        self._default = _default
        self.active = active
        self.last_write_time = last_write_time
        self.title = title
        self.notes = notes
        self.changed_date = changed_date

    def __str__(self):
        return f'Name(id = {self.id}, guid = {self.guid}, version = {self.version}, person_id = {self.person_id}, name_type_code = {self.name_type_code}, first_name = {self.first_name}, middle_name = {self.middle_name}, last_name = {self.last_name}, suffix = {self.suffix}, prefix = {self.prefix}, _default = {self._default}, active = {self.active}, last_write_time = {self.last_write_time}, title = {self.title}, notes = {self.notes}, changed_date = {self.changed_date})'

class Patron:
    def __init__(self, id=None, guid=None, version=None, library_id=None, patron_type_id=None, active=None, general_block=None, paging_privilege=None, courtesy_notice=None, delivery_privilege=None, end_date=None, start_date=None, general_block_notes=None, invalid_barcode=None, invalid_barcode_start_date=None, source_id=None, patron_category_id=None, photograph=None):
        self.id = id
        self.guid = guid
        self.version = version
        self.library_id = library_id
        self.patron_type_id = patron_type_id
        self.active = active
        self.general_block = general_block
        self.paging_privilege = paging_privilege
        self.courtesy_notice = courtesy_notice
        self.delivery_privilege = delivery_privilege
        self.end_date = end_date
        self.start_date = start_date
        self.general_block_notes = general_block_notes
        self.invalid_barcode = invalid_barcode
        self.invalid_barcode_start_date = invalid_barcode_start_date
        self.source_id = source_id
        self.patron_category_id = patron_category_id
        self.photograph = photograph

    def __str__(self):
        return f'Patron(id = {self.id}, guid = {self.guid}, version = {self.version}, library_id = {self.library_id}, patron_type_id = {self.patron_type_id}, active = {self.active}, general_block = {self.general_block}, paging_privilege = {self.paging_privilege}, courtesy_notice = {self.courtesy_notice}, delivery_privilege = {self.delivery_privilege}, end_date = {self.end_date}, start_date = {self.start_date}, general_block_notes = {self.general_block_notes}, invalid_barcode = {self.invalid_barcode}, invalid_barcode_start_date = {self.invalid_barcode_start_date}, source_id = {self.source_id}, patron_category_id = {self.patron_category_id}, photograph = {self.photograph})'

class PatronId1:
    def __init__(self, id=None, guid=None, version=None, patron_id=None, value=None):
        self.id = id
        self.guid = guid
        self.version = version
        self.patron_id = patron_id
        self.value = value

    def __str__(self):
        return f'PatronId1(id = {self.id}, guid = {self.guid}, version = {self.version}, patron_id = {self.patron_id}, value = {self.value})'

class PatronType:
    def __init__(self, id=None, code=None, description=None, name=None, guid=None, version=None, active=None):
        self.id = id
        self.code = code
        self.description = description
        self.name = name
        self.guid = guid
        self.version = version
        self.active = active

    def __str__(self):
        return f'PatronType(id = {self.id}, code = {self.code}, description = {self.description}, name = {self.name}, guid = {self.guid}, version = {self.version}, active = {self.active})'

class Person:
    def __init__(self, id=None, guid=None, version=None, active=None, last_write_time=None):
        self.id = id
        self.guid = guid
        self.version = version
        self.active = active
        self.last_write_time = last_write_time

    def __str__(self):
        return f'Person(id = {self.id}, guid = {self.guid}, version = {self.version}, active = {self.active}, last_write_time = {self.last_write_time})'

class User:
    def __init__(self, id=None, guid=None, version=None, user_name=None, person_id=None, password=None, active=None, last_write_time=None):
        self.id = id
        self.guid = guid
        self.version = version
        self.user_name = user_name
        self.person_id = person_id
        self.password = password
        self.active = active
        self.last_write_time = last_write_time

    def __str__(self):
        return f'User(id = {self.id}, guid = {self.guid}, version = {self.version}, user_name = {self.user_name}, person_id = {self.person_id}, password = {self.password}, active = {self.active}, last_write_time = {self.last_write_time})'
