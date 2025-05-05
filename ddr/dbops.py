#!/usr/bin/env python3

from personal import database_connection, write_table_as_csv, write_query_as_csv
import pandas as pd
import sys

connection = database_connection('hixacceptatie')
if connection is None:
    sys.exit(0)

#write_table_as_csv('vrlijst_controls')
#write_table_as_csv('vrlijst_lijstdef')
#write_table_as_csv('vrlijst_treelay')
#write_table_as_csv('vrlijst_vragen')
#write_table_as_csv('vrlijst_vrlcat')

query = "select lijstid from [hix_acc].[dbo].[vrlijst_lijstdef]"
lijsten = pd.read_sql(sql=query, con=connection)
print(lijsten.head(10))

# query = "select vraagid from [hix_acc].[dbo].[vrlijst_vragen]"
# vragen = pd.read_sql(sql=query, con=connection)
#
# query = "select distinct lijstid from [hix_acc].[dbo].[vrlijst_lstopslg]"
# beantwoorde_vragenlijsten = pd.read_sql(sql=query, con=connection)
# print(beantwoorde_vragenlijsten.head(10))

connection.close()