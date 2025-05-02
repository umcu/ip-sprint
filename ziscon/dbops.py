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

# Casus: value bevat 1 GUID
# C" 0,{2B9293AF-E862-11D3-A60F-00A024C504A3},F,"" """"PSY  """",""""PSO  """",""""GGZ  """",""""KJP  """" "" "
#    0,{2B9293AF-E862-11D3-A60F-00A024C504A3},F," ""PSY  "",""PSO  "",""GGZ  "",""KJP  "" "
#                                                  "PSY  ","PSO  ","GGZ  ","KJP  "
#
# Casus: value bevat >1 GUID's
# C"6,{49C47C86-D97F-11D3-9ED4-0008C70D94E3},F,""""""ARCHIEF """""","
#   ,
#  "6,{C8D8830E-882E-4C04-B056-7DB9F50DC3A6},F,CS00000006,"
#   ,
#  "6,{C0BF0AD1-43D8-475A-8840-68EEB9341A47},F,""CS00000271,CS00000224,CS00000218"","
#
# level 1: open=2780, close=2776
# level 2: open=2781, close=2777
# level 3: open=2782, close=2778