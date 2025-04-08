#!/usr/bin/env python

from urllib.parse import quote
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint

# retrieve data from database and put this in a dataframe
sql_query = 'SELECT moment_brief_aangemaakt, ontslagdatum FROM datakwaliteit.Opname_Procesinfo_Ontslagbericht WHERE YEAR(ontslagdatum) = 2021'
passwd_quoted = quote('K3&l#ZYp@xiiq&TM')
sql_connection_string = f'mssql+pymssql://pub_s_datakwaliteit:{passwd_quoted}@voxdb-dpdb01.ds.umcutrecht.nl/?charset=utf8'
df_ontslagdatum = pd.DataFrame(pd.read_sql_query(sql_query, sql_connection_string))

# show first lines of output, plus list of column names
print(df_ontslagdatum.iloc[range(0, 2)])
# print(sorted(df_ontslagdatum.columns))
"""
['brief_binnen_14_dagen', 'brief_of_bericht_op_tijd', 'duur_aanmaken_brief',
'duur_akkoord_brief', 'duur_doorloop_brief', 'duur_versturen_bericht',
'duur_versturen_brief', 'klinisch_ontslagbericht_kpi_indicator', 'leeftijd_bij_ontslag',
'moment_bericht_verstuurd', 'moment_brief_aangemaakt', 'moment_brief_akkoord',
'moment_brief_gewijzigd', 'moment_brief_verstuurd', 'ontslagafdeling_afdeling_id',
'ontslagafdeling_afdeling_identifier_system', 'ontslagafdeling_afdeling_identifier_value',
'ontslagbericht_aanwezig', 'ontslagbrief_aanwezig', 'ontslagdatum', 'ontslagmoment',
'ontslagspecialisme_specialisme_id', 'ontslagspecialisme_specialisme_identifier_system',
'ontslagspecialisme_specialisme_identifier_value', 'opnamemoment', 'opnametype_id',
'opnametype_identifier_system', 'opnametype_identifier_value', 'organisatie-eenheid_id',
'organisatie-eenheid_identifier_system', 'organisatie-eenheid_identifier_value']
"""
# check that date was read as date
# print(df_ontslagdatum['ontslagdatum'][0])

# construct GX data source and asset from this dataframe
context = gx.get_context()
source = context.sources.add_pandas(name='ontslagdatum_source')
data_asset = source.add_dataframe_asset(name='dataframe_ontslagdatum', dataframe=df_ontslagdatum)

# create batch request based on data asset 'dataframe_ontslagdatum'
batch_asset = context.datasources['ontslagdatum_source'].get_asset('dataframe_ontslagdatum')
batch_request = batch_asset.build_batch_request()

# create a GX expectation suite
expectation_suite_name = 'test_suite'
expectation_suite = context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)

# add expectations to expectations suite
expectation_1 = ExpectationConfiguration(
expectation_type="expect_column_values_to_be_between",
kwargs={
    "column": "moment_brief_aangemaakt",
    "max_value": 240.0, "min_value": -48.0, "mostly": 0.7,
    "strict_max": False, "strict_min": False
})
expectation_suite.add_expectation(expectation_configuration=expectation_1)

"""
"expectation_type": "expect_column_median_to_be_between",
"kwargs": {
    "column": "moment_brief_aangemaakt",
    "max_value": 16.0,
    "min_value": -16.0,
    "strict_max": false,
    "strict_min": false
},

"expectation_type": "expect_column_values_to_be_between",
"kwargs": {
    "column": "moment_brief_verstuurd",
    "max_value": 480.0,
    "min_value": -2.0,
    "mostly": 0.7,
    "strict_max": false,
    "strict_min": false
},

"expectation_type": "expect_column_median_to_be_between",
"kwargs": {
    "column": "moment_brief_verstuurd",
    "max_value": 36.0,
    "min_value": 12.0,
    "strict_max": false,
    "strict_min": false},

expectation_2 = ExpectationConfiguration(
    expectation_type='expect_column_values_to_not_be_null',
    kwargs={'column': 'ontslagdatum', 'mostly': 1.0},
)
suite.add_expectation(expectation_configuration=expectation_2)
"""

# add expectation_suite to context
context.add_or_update_expectation_suite(expectation_suite=expectation_suite)

# run expectation suite on batch request via a simple checkpoint
checkpoint_config = {
    'class_name': 'SimpleCheckpoint',
    'validations': [
        {'batch_request': batch_request,
         'expectation_suite_name': expectation_suite_name,
        }
    ],
}
checkpoint = SimpleCheckpoint('ontslagdatum_test', context, **checkpoint_config)
checkpoint_result = checkpoint.run()

# build and open Data Docs with the latest checkpoint run result included:
context.build_data_docs()
context.open_data_docs()
