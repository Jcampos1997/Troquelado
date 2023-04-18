
import psycopg2

from hdbcli import dbapi

cond = psycopg2.connect(
    host="192.168.2.100",
    database="appPeso",
    user="postgres",
    password="qq",
    options="-c search_path=dbo,produccion")
'''
cond = psycopg2.connect(
        host = "192.168.1.18",
        database = "appPesoPruebas",
        user = "postgres",
        password = "qq",
        options="-c search_path=dbo,produccion")
'''


cnsap = dbapi.connect(address='10.254.254.254', port=30015,
                      user='SVAGRT_DBREADER', password='dPtWhDwV2aRHR5bA')
