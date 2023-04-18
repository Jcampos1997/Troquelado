#import pyhdb
#import hana_ml
import hana_ml.dataframe as dataframe
conn = dataframe.ConnectionContext("10.254.254.254", 30015, "SVAGRT_DBREADER", "dPtWhDwV2aRHR5bA")

#Query para validar si of es de rollo
#sql='SELECT b."ItemName"  FROM "DB_SUPRALIVE_PRUEBAS"."OWOR" a INNER JOIN "DB_SUPRALIVE_PRUEBAS"."OITM" b ON a."ItemCode" = b."ItemCode" WHERE a."DocNum" = 223353 and b."ItemName" LIKE \'%ROLLO%\' '

#Query para ver colaboradores
#sql='SELECT a."firstName", a."lastName", a."jobTitle", a."workStreet" FROM "DB_SUPRALIVE_PRUEBAS"."OHEM" a'
#sql='SELECT a."firstName", a."lastName", a."jobTitle", a."workStreet" FROM "DB_SUPRALIVE_PRUEBAS"."OHEM" a where a."jobTitle"=\'SUPERVISOR EXPANDIDO\' '

sql='SELECT a."workStreet",a."StreetNoW" FROM "DB_SUPRALIVE_PRUEBAS"."OHEM" a where a."jobTitle"=\'SUPERVISOR EXPANDIDO\' '

df_pushdown = conn.sql(sql)
print(df_pushdown.collect())

# Close connection
conn.close()

