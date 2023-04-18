import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="qq",
                                  host="localhost",
                                  port="5432",
                                  database="appsenior",
                                  options="-c search_path=dbo,produccion")
                                  
    cur = connection.cursor()
        #contar cantidad de rollos pesados
    consulta = "SELECT id FROM maquina where nombre='102' and estado='activo' "
    cur.execute(consulta)
    cd = cur.fetchone()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cur.close()
        connection.close()
        print("PostgreSQL connection is closed")