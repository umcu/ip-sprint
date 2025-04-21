#!/usr/bin/env python3

from personal import database_connection, write_query_as_csv, write_table_as_csv
import sys

connection = database_connection('hixacceptatie')
if connection is None:
    sys.exit(0)

#write_table_as_csv('config_wcsegments')
#write_table_as_csv('config_workcontext')
write_table_as_csv('config_instvars')

connection.close()
