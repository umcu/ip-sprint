#!/usr/bin/env python3

from personal import *
import sys

connection = database_connection('hixacceptatie')
if connection is None:
    sys.exit(0)

query = f"select top (100) * from [hix_acc].[dbo].[config_instvars];"
iv = read_query_as_df(query, connection)
print(iv.head())

# write_table_as_csv('config_wcsegments')
# write_table_as_csv('config_workcontext')
# write_table_as_csv('config_instvars')

connection.close()
