import numpy as np

class Columns():
    def __init__(self):
        self.act = 'act'
        self.age_at_incident = 'age_at_incident'
        self.aoic = 'aoic'
        self.arraignment_date = 'arraignment_date'
        self.arrest_date = 'arrest_date'
        self.bond_amount_current = 'bond_amount_current'
        self.bond_amount_initial = 'bond_amount_initial'
        self.bond_date_current = 'bond_date_current'
        self.bond_date_initial = 'bond_date_initial'
        self.bond_electroinic_monitor_flag_current = 'bond_electroinic_monitor_flag_current'
        self.bond_electronic_monitor_flag_initial = 'bond_electronic_monitor_flag_initial'
        self.bond_type_current = 'bond_type_current'
        self.bond_type_initial = 'bond_type_initial'
        self.case_id = 'case_id'
        self.case_length = 'case_length'
        self.case_participant_id = 'case_participant_id'
        self.chapter = 'chapter'
        self.charge_count = 'charge_count'
        self.charge_disposition = 'charge_disposition'
        self.charge_disposition_cat = 'charge_disposition_cat'
        self.charge_disposition_reason = 'charge_disposition_reason'
        self.charge_id = 'charge_id'
        self.charge_offense_title = 'charge_offense_title'
        self.charge_version_id = 'charge_version_id'
        self.charged_class_difference = 'charged_class_difference'
        self.charge_class = 'class'
        self.commitment_days = 'commitment_days'
        self.commitment_dollars = 'commitment_dollars'
        self.commitment_type = 'commitment_type'
        self.commitment_unit = 'commitment_unit'
        self.commitment_weight = 'commitment_weight'
        self.current_sentence_flag = 'current_sentence_flag'
        self.disposition_charged_act = 'disposition_charged_act'
        self.disposition_charged_aoic = 'disposition_charged_aoic'
        self.disposition_charged_chapter = 'disposition_charged_chapter'
        self.disposition_charged_class = 'disposition_charged_class'
        self.disposition_charged_offense_title = 'disposition_charged_offense_title'
        self.disposition_charged_section = 'disposition_charged_section'
        self.disposition_court_facility = 'disposition_court_facility'
        self.disposition_court_name = 'disposition_court_name'
        self.disposition_date = 'disposition_date'
        self.disposition_date_days_pending = 'disposition_date_days_pending'
        self.event = 'event'
        self.event_date = 'event_date'
        self.felony_review_date = 'felony_review_date'
        self.felony_review_result = 'felony_review_result'
        self.finding_no_probable_cause = 'finding_no_probable_cause'
        self.gender = 'gender'
        self.incident_begin_date = 'incident_begin_date'
        self.incident_city = 'incident_city'
        self.incident_end_date = 'incident_end_date'
        self.initial_charged_class = 'initial_charged_class'
        self.judge = 'judge'
        self.law_enforcement_agency = 'law_enforcement_agency'
        self.law_enforcement_unit = 'law_enforcement_unit'
        self.life_term = 'life_term'
        self.offense_category = 'offense_category'
        self.primary_charge_flag = 'primary_charge_flag'
        self.primary_charge_flag_init = 'primary_charge_flag_init'
        self.race = 'race'
        self.received_date = 'received_date'
        self.section = 'section'
        self.sentence_court_facility = 'sentence_court_facility'
        self.sentence_court_name = 'sentence_court_name'
        self.sentence_date = 'sentence_date'
        self.sentence_judge = 'sentence_judge'
        self.sentence_phase = 'sentence_phase'
        self.sentence_type = 'sentence_type'
        self.updated_offense_category = 'updated_offense_category'

        self.key_district = {
              1: 'District 1 - Chicago'
            , 2: 'District 2 - Skokie'
            , 3: 'District 3 - Rolling Meadows'
            , 4: 'District 4 - Maywood'
            , 5: 'District 5 - Bridgeview'
            , 6: 'District 6 - Markham'
        }

        self.fac_name = 'Fac_Name'

        self.key_facname = {
            '26Th Street': 'Criminal Courts (26th/California)'
            , 'Markham Courthouse': 'Markham Courthouse (6th District)'
            , 'Skokie Courthouse': 'Skokie Courthouse (2nd District)'
            , 'Rolling Meadows Courthouse': 'Rolling Meadows Courthouse (3rd District)'
            , np.nan: np.nan
            , 'Maywood Courthouse': 'Maywood Courthouse (4th District)'
            , 'Bridgeview Courthouse': 'Bridgeview Courthouse (5th District)'
            , 'Dv Courthouse': 'Domestic Violence Courthouse'
            , 'Dnu_3605 W. Fillmore St (Rjcc)': 'RJCC'
            , 'Daley Center': 'Daley Center'
            , '3605 W. Fillmore (Rjcc)': 'RJCC'
            , 'Grand & Central (Area 5)': 'Circuit Court Branch 23/50'
            , 'Harrison & Kedzie (Area 4)': 'Circuit Court Branch 43/44'
            , '51St & Wentworth (Area 1)': 'Circuit Court Branch 34/38'
            , 'Belmont & Western (Area 3)': 'Circuit Court Branch 29/42'
            , '727 E. 111Th Street (Area 2)': 'Circuit Court Branch 35/38'
                            }

    def names(self):
        initiation_table = [
            'case_id'
            , 'case_participant_id'
            , 'received_date'
            , 'offense_category'
            , 'primary_charge_flag'
            , 'charge_id'
            , 'charge_version_id'
            , 'charge_offense_title'
            , 'charge_count'
            , 'chapter'
            , 'act'
            , 'section'
            , 'class'
            , 'aoic'
            , 'event'
            , 'event_date'
            , 'finding_no_probable_cause'
            , 'arraignment_date'
            , 'bond_date_initial'
            , 'bond_date_current'
            , 'bond_type_initial'
            , 'bond_type_current'
            , 'bond_amount_initial'
            , 'bond_amount_current'
            , 'bond_electronic_monitor_flag_initial'
            , 'bond_electroinic_monitor_flag_current'
            , 'age_at_incident'
            , 'race'
            , 'gender'
            , 'incident_city'
            , 'incident_begin_date'
            , 'incident_end_date'
            , 'law_enforcement_agency'
            , 'law_enforcement_unit'
            , 'arrest_date'
            , 'felony_review_date'
            , 'felony_review_result'
            , 'updated_offense_category'
        ]

        disposition_table = [
            'case_id'
            , 'case_participant_id'
            , 'received_date'
            , 'offense_category'
            , 'primary_charge_flag'
            , 'charge_id'
            , 'charge_version_id'
            , 'disposition_charged_offense_title'
            , 'charge_count'
            , 'disposition_date'
            , 'disposition_charged_chapter'
            , 'disposition_charged_act'
            , 'disposition_charged_section'
            , 'disposition_charged_class'
            , 'disposition_charged_aoic'
            , 'charge_disposition'
            , 'charge_disposition_reason'
            , 'judge'
            , 'disposition_court_name'
            , 'disposition_court_facility'
            , 'age_at_incident'
            , 'race'
            , 'gender'
            , 'incident_city'
            , 'incident_begin_date'
            , 'incident_end_date'
            , 'law_enforcement_agency'
            , 'law_enforcement_unit'
            , 'arrest_date'
            , 'felony_review_date'
            , 'felony_review_result'
            , 'arraignment_date'
            , 'updated_offense_category'
        ]

        derived_table = ['case_id'
                             , 'case_participant_id'
                             , 'primary_charge_flag_init'
                             , 'class'
                             , 'received_date'
                             , 'event'
                             , 'judge'
                             , 'disposition_court_name'
                             , 'disposition_court_facility'
                             , 'charge_disposition'
                             , 'case_length'
                             , 'disposition_date'
                             , 'disposition_date_days_pending']

        initiation_modified = ['case_id', 'case_participant_id', 'received_date', 'offense_category', 'primary_charge_flag', 'charge_id', 'charge_version_id', 'charge_offense_title', 'charge_count', 'chapter', 'act', 'section', 'class', 'aoic', 'event', 'event_date', 'finding_no_probable_cause', 'arraignment_date', 'bond_date_initial', 'bond_date_current', 'bond_type_initial', 'bond_type_current', 'bond_amount_initial', 'bond_amount_current', 'bond_electronic_monitor_flag_initial', 'bond_electroinic_monitor_flag_current', 'age_at_incident', 'race', 'gender', 'incident_city', 'incident_begin_date', 'incident_end_date', 'law_enforcement_agency', 'law_enforcement_unit', 'arrest_date', 'felony_review_date', 'felony_review_result', 'updated_offense_category', 'disposition_date_days_pending']
        disposition_modified = ['case_id', 'case_participant_id', 'received_date', 'offense_category', 'primary_charge_flag', 'charge_id', 'charge_version_id', 'disposition_charged_offense_title', 'charge_count', 'disposition_date', 'disposition_charged_chapter', 'disposition_charged_act', 'disposition_charged_section', 'disposition_charged_class', 'disposition_charged_aoic', 'charge_disposition', 'charge_disposition_reason', 'judge', 'disposition_court_name', 'disposition_court_facility', 'age_at_incident', 'race', 'gender', 'incident_city', 'incident_begin_date', 'incident_end_date', 'law_enforcement_agency', 'law_enforcement_unit', 'arrest_date', 'felony_review_date', 'felony_review_result', 'arraignment_date', 'updated_offense_category', 'charge_disposition_cat', 'case_length', 'initial_charged_class', 'charged_class_difference']
        sentencing_modified = ['case_id', 'case_participant_id', 'received_date', 'offense_category', 'primary_charge_flag', 'charge_id', 'charge_version_id', 'disposition_charged_offense_title', 'charge_count', 'disposition_date', 'disposition_charged_chapter', 'disposition_charged_act', 'disposition_charged_section', 'disposition_charged_class', 'disposition_charged_aoic', 'charge_disposition', 'charge_disposition_reason', 'sentence_judge', 'sentence_court_name', 'sentence_court_facility', 'sentence_phase', 'sentence_date', 'sentence_type', 'current_sentence_flag', 'commitment_type', 'commitment_unit', 'age_at_incident', 'race', 'gender', 'incident_city', 'incident_begin_date', 'incident_end_date', 'law_enforcement_agency', 'law_enforcement_unit', 'arrest_date', 'felony_review_date', 'felony_review_result', 'arraignment_date', 'updated_offense_category', 'commitment_days', 'commitment_dollars', 'commitment_weight', 'life_term', 'case_length', 'charge_disposition_cat']

        all_cols = list(set(initiation_table + disposition_table + derived_table + sentencing_modified + disposition_modified + initiation_modified))

        all_cols.sort()

        self_list = [(str('self.'+x+'='+"\'"+x+"\'")) for x in all_cols]
        self_list = [x if 'self.class=' not in x else x.replace('self.class=', 'self.charge_class=') for x in self_list ]
        # https://www.geeksforgeeks.org/python-ways-to-print-list-without-quotes/
        # return a list to create class variables
        print('[%s]' % ' '.join(map(str, self_list)))


# Columns().names()








