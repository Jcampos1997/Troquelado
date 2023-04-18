from hdbcli import dbapi

con = dbapi.connect(address='10.254.254.254',port=30015,user='SVAGRT_DBREADER',password='dPtWhDwV2aRHR5bA')

cur = con.cursor()
ofs='231509'
sql='SELECT a."DocNum", a."ItemCode", a."ProdName", c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN "SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" where a."DocNum"='+ofs+' '
cur.execute(sql)
result = cur.fetchall()
for l in result:
     print (l)