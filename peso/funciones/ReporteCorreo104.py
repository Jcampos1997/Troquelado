
#REPORTE PARA LOS PESOS DE LA MAQUINA 102
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from funciones import ServerCorreo
from datetime import datetime
#import pdfkit
import configm 

luc = configm.cond
lio = configm.cnsap #PARA PODER REALIZAR CONSULTAS EN SAP
class ReporteCorreo104():

    def __init__(self, supervidor):
        self.supervisor = supervidor

    def imprimirReporte(self):   
        fila_y = 560 #iniciamos en la posicion 560 en y(plano cartesiano)
        fila_x_numero = 20
        fila_x_fecha = 50
        fila_x_peso = 200
        fila_x_kg = 230
        linea_horizontal = 555
        linea_vertical = 590
        contador = 0.0 #contador para controlar el numero de filas y realizar el salto de pagina
        contador_fila = 1 #contador para controlar el numero de filas realizar el salto de filas a lado  
        contador_fila2 = 1
        peso_total = 0.0 #sumara el peso para sacar el peso total
        peso_total_bueno = 0.0
        peso_total_desperdicio = 0.0  
        calculo_porcentaje_desperdicio = 0.0   
        ultima_consulta = luc.cursor() 
        reporte  = luc.cursor() 
        ultima_consulta2 = luc.cursor()
        #247150 246317
        #tomaremos la ultima orden de fabricacion 
        fecha_actual = datetime.today().strftime('%Y-%m-%d')
        ultima_orden_fabricacion = "SELECT ofab FROM peso_materia pm INNER JOIN maquina_of mo ON "\
                                   "pm.id_maquina_of = mo.id " \
                                   "WHERE to_char(pm.fecha_creacion,'YYYY-MM-DD') "\
                                   "LIKE '{}%' AND mo.maquina LIKE '%104%' ORDER BY id_peso_mat DESC limit 1 ".format(str(fecha_actual))
        
        ultima_consulta.execute(ultima_orden_fabricacion)
        ultima_consulta2.execute(ultima_orden_fabricacion)
        orden_fab = ultima_consulta.fetchone()
        orden = ultima_consulta2.fetchone()
        
        #CONSULTA QUE PRESENTARA LOS DATOS DE CABECERA DEL REPORTE
        consulta = "SELECT CONCAT(EXTRACT(year FROM pm.fecha_creacion),'-',"\
                   "EXTRACT(MONTH FROM pm.fecha_creacion),'-',"\
	               "EXTRACT(day FROM pm.fecha_creacion)) as Fecha,"\
	               "EXTRACT(HOUR FROM pm.fecha_creacion),"\
	               "pm.fecha_creacion, pm.ofab, mo.operador,"\
	               "sum(pm.peso) AS peso_bueno, "\
	               "(SELECT sum(peso) FROM peso_materia WHERE finca LIKE '%finca%' AND ofab LIKE '%{}%') AS peso_malo "\
                   "FROM peso_materia pm "\
                   "INNER JOIN maquina_of mo ON mo.id = pm.id_maquina_of "\
                   "WHERE pm.ofab LIKE '%{}%' AND pm.finca IS null AND  to_char(pm.fecha_creacion,'YYYY-MM-DD') LIKE '{}%' "\
                   "GROUP BY pm.fecha_creacion,mo.operador,pm.ofab, pm.id_peso_mat "\
	               "ORDER BY pm.id_peso_mat ASC ".format(str(orden[0]), str(orden[0]), str(fecha_actual))
        
        reporte.execute(consulta)
        orden_fab = reporte.fetchall()
        reporte.close()
        #CONSULTA QUE PRESENTARA LOS DATOS EN LA TABLA
        consulta_tabla = "SELECT pm.fecha_creacion, EXTRACT(HOUR FROM pm.fecha_creacion), CASE WHEN pm.finca LIKE '%finca%' THEN 1 "\
                         "ELSE 0 "\
                         "END AS Finca, "\
                         "SUM(pm.peso) AS peso_Kg "\
                         "FROM peso_materia pm "\
                         "INNER JOIN maquina_of mo ON mo.id = pm.id_maquina_of "\
                         "WHERE pm.ofab LIKE '%{}%' AND to_char(pm.fecha_creacion,'YYYY-MM-DD') LIKE '{}%' "\
                         "GROUP BY pm.fecha_creacion, pm.id_peso_mat "\
                         "ORDER BY pm.id_peso_mat ASC ".format(str(orden[0]), str(fecha_actual))
      
        #DATOS DE LA TABLA
        table = luc.cursor()
        table.execute(consulta_tabla)
        datos_tabla = table.fetchall()

        #DATOS DE PESO DESPERDICIADO
        peso_d = luc.cursor()
        consulta_peso_d = "SELECT sum(peso) FROM peso_desperdicio WHERE ofab LIKE '{}' ".format(str(orden[0]))
        peso_d.execute(consulta_peso_d)
        dato_peso_desperdiciado = peso_d.fetchone()
        print(dato_peso_desperdiciado)
    
        #CONSULTA PARA OBTENER EL CÓDIGO DEL PRODUCTO Y EL NOMBRE 
        consulta_sap = 'SELECT a."DocNum", a."ItemCode", a."ProdName",'\
                       'c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a  '\
                       'INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN '\
                       '"SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" '\
                       'where a."DocNum"={} '.format(str(orden[0]))
        sap = lio.cursor()
        sap.execute(consulta_sap)
        codigo_nombre_producto = sap.fetchone()
        sap.close()


        hora_inicio_fin = "(SELECT EXTRACT(HOUR FROM pm.fecha_creacion) AS hora "\
	                      "FROM peso_materia pm "\
	                      "INNER JOIN maquina_of mo ON mo.id = pm.id_maquina_of WHERE pm.ofab LIKE '%{}%'"\
                          "GROUP BY pm.fecha_creacion, pm.id_peso_mat "\
	                      "ORDER BY pm.id_peso_mat ASC LIMIT 1) "\
                          "UNION ALL  "\
                          "(SELECT EXTRACT(HOUR FROM pm.fecha_creacion) AS hora "\
	                      "FROM peso_materia pm "\
	                      "INNER JOIN maquina_of mo ON mo.id = pm.id_maquina_of "\
                          "WHERE pm.ofab LIKE '%{}%' "\
                          "GROUP BY pm.fecha_creacion, pm.id_peso_mat "\
	                      "ORDER BY pm.id_peso_mat DESC  LIMIT 1) ".format(str(orden[0]), str(orden[0]))


        hora = luc.cursor()
        hora.execute(hora_inicio_fin)
        h_inicio_fin = hora.fetchall()    
        hora.close()

        print(str(h_inicio_fin[1][0]))
        hora_inicio = str(h_inicio_fin[0][0])
        hora_fin = str(h_inicio_fin[1][0])

        resta = float(hora_fin) -float(hora_inicio)
       
        #especificamos el nombre del archivo
        canvas2 = canvas.Canvas("reportePesos.pdf", pagesize=letter)
        canvas2.setLineWidth(.3)    

        #realiza la suma de cada peso para obtener el total de pesos
        for fila in datos_tabla:
            peso_total += float(fila[3])

        #realiza la suma de cada peso para obtener el total de pesos en buen estado
        for fila in datos_tabla:
            if fila[2] != 1:
              peso_total_bueno += float(fila[3])

        for fila in datos_tabla:
            if fila[2] == 1:
                peso_total_desperdicio += float(fila[3])
                
        #calculamos el promedio en kilogramos/hora
        promedio_km_hora = float(peso_total) / (float(hora_fin) - float(hora_inicio))
      
        #tomo los datos de la consulta 
        peso_desperdicio = dato_peso_desperdiciado[0]
        peso_malo = orden_fab[0][6]
        
        #se toma en cuenta que la base de datos hay datos nulos,
        #entonces valido en caso de que sean None
        if peso_desperdicio == None:
            peso_desperdicio = 0.0
        if peso_malo == None:
            peso_malo = 0.0
        print("Peso desperdiciado: {}".format(peso_desperdicio))
        print("Peso total bueno {}".format(peso_total_bueno))
        print("Peso malo {}".format(peso_malo))
        #CALCULO EL PORCENTAJE DE DESPERDICIO
        calculo_porcentaje_desperdicio =  (float(peso_desperdicio) / (float(peso_total_bueno) + float(peso_malo))) * 100
        fecha = str(datos_tabla[0][0]) #esta fecha sale en la cabecera del reporte
        
        #DIBUJA LA CABECERA DEL REPORTE
        canvas2.setFont('Helvetica', 23)
        canvas2.line(10, 785, 10, 600) #LINEA VERTICAL DERECHA
        canvas2.line(600, 785, 600, 600) #LINEA VERTICAL IZQUIERDA
        canvas2.line(10, 785, 600, 785) #LINEA ORIZONTAL
        canvas2.drawString(150, 750, 'Orden de fabricación: ')
        canvas2.drawString(370, 750, str(orden_fab[0][3]))
        canvas2.line(10, 735, 600, 735) #LINEA ORIZONTAL
        canvas2.setFont('Helvetica', 12)
        canvas2.drawString(30, 720, 'Supervisor: ')
        canvas2.drawString(100, 720, self.supervisor)
        canvas2.line(10, 715, 600, 715) #LINEA ORIZONTAL
        canvas2.drawString(30, 700, 'Operador: ')
        canvas2.drawString(100, 700, str(orden_fab[0][4][0:10]))
        canvas2.line(10, 695, 600, 695) #LINEA ORIZONTAL
        canvas2.drawString(30, 680,'Código: ')
        canvas2.drawString(100, 680, str(codigo_nombre_producto[1]))
        canvas2.line(10, 675, 600, 675) #LINEA ORIZONTAL
        canvas2.line(10, 635, 600, 635) #LINEA ORIZONTAL
        canvas2.line(10, 615, 600, 615) #LINEA ORIZONTAL
        canvas2.drawString(30, 605,'Producto: ')
        canvas2.drawString(100, 605, str(codigo_nombre_producto[2]))
        canvas2.line(10, 655, 600, 655) #LINEA ORIZONTAL
        canvas2.drawString(380, 700, 'Peso total en kg: ')
        canvas2.drawString(535, 700, str(round(peso_total,2)))
        canvas2.drawString(578, 700, 'Kg' )
        canvas2.drawString(30, 660, 'Producción Kg. buen estado: ')
        canvas2.drawString(190, 660, str(round(peso_total_bueno,2)))
        canvas2.drawString(230, 660, 'Kg' )
        canvas2.drawString(30, 640, 'Fecha: ')
        canvas2.drawString(100, 640, fecha[0:11])
        canvas2.drawString(30, 621, 'Hora Inicio: ')
        canvas2.drawString(100, 621, hora_inicio[0:2])
        canvas2.drawString(380, 720, 'Producción Kg. mal estado: ')
        canvas2.drawString(535, 720, str(round(peso_total_desperdicio,2)))
        canvas2.drawString(578, 720, 'Kg' )

        canvas2.drawString(380, 680,'Desperdicio:')
        canvas2.drawString(535, 680, str(peso_desperdicio))
        canvas2.drawString(578, 680, 'Kg' )

        canvas2.drawString(380,660,'% Desperdicio:')
        canvas2.drawString(535,660,str(round(calculo_porcentaje_desperdicio, 2)))
        canvas2.drawString(578, 660, '%' )  
        canvas2.drawString(380 ,640, 'Promedio Kg/H: ')
        canvas2.drawString(525 ,640,  str(round(promedio_km_hora,2)))
        canvas2.drawString(568, 640, 'Kg/H' )

        canvas2.drawString(380, 621, 'Hora Fin: ')
        canvas2.drawString(430, 621, hora_fin[0:2])

        canvas2.line(10, 575, 600, 575) #LINEA ORIZONTAL ANTES DE LA FECHA Y HORA 
        canvas2.line(10, 590, 600, 590) #LINEA ORIZONTAL DESPUES DE LA FECHA Y HORA 
        canvas2.drawString(20,580,'#') 
        canvas2.drawString(60,580,'Fecha y hora')
        canvas2.drawString(210,580,'Peso')

        canvas2.drawString(350,580,'#') 
        canvas2.drawString(390,580,'Fecha y hora')
        canvas2.drawString(550,580,'Peso')

        peso_total = 0.0
        peso_total_bueno = 0.0

        contador = 1
        for fila in datos_tabla:
            if fila[2] == 1:

               #FECHA
               linea_horizontal_finca = linea_horizontal + 5
               canvas2.line(45, linea_horizontal_finca, 150, linea_horizontal_finca) #LINEA ORIZONTAL
               canvas2.line(45, linea_horizontal_finca, 150, linea_horizontal_finca) #LINEA ORIZONTAL
               canvas2.line(45, linea_horizontal_finca, 150, linea_horizontal_finca) #LINEA ORIZONTAL
               canvas2.line(45, linea_horizontal_finca, 150, linea_horizontal_finca) #LINEA ORIZONTAL
               
               #PESO
               canvas2.line(200, linea_horizontal_finca, 245, linea_horizontal_finca) #LINEA ORIZONTAL
               canvas2.line(200, linea_horizontal_finca, 245, linea_horizontal_finca) #LINEA ORIZONTAL
               canvas2.line(200, linea_horizontal_finca, 245, linea_horizontal_finca) #LINEA ORIZONTAL
               canvas2.line(200, linea_horizontal_finca, 245, linea_horizontal_finca) #LINEA ORIZONTAL
               linea_horizontal_finca = 0
            #cuando contador sea mayor o igual 29 las posiciones se cambian para que salgan los datos
            #en el lado derecho
            if contador >= 29:
                fila_x_numero = 350
                fila_x_fecha = 390
                fila_x_peso = 550
                fila_x_kg = 580
                fila_y = 560
                contador = 1

            #si el contador es igual a 57 de nuevo se cambian las posiciones ya que ahora
            #se realizara un salto de página
            if contador_fila2 == 57 :
                
                fila_y = 740 #iniciamos en la posicion 700 en y(plano cartesiano)
                fila_x_numero = 20
                fila_x_fecha = 50
                fila_x_peso = 200
                fila_x_kg = 230
                linea_vertical = 600
                linea_horizontal = 735
                contador_fila2 = 1
                fecha = str(fila[0])
                canvas2.showPage()#showPage() permite el salto de pagina
                canvas2.drawString(350,760,'#') 
                canvas2.drawString(390,760,'Fecha y hora')
                canvas2.drawString(550,760,'Peso')
                canvas2.drawString(20, 760,'#') 
                canvas2.drawString(60,760,'Fecha y hora')
                canvas2.drawString(210,760,'Peso')
                canvas2.drawString(fila_x_numero, fila_y,str(contador_fila))
                canvas2.drawString(fila_x_fecha, fila_y,fecha[0:16]) #[0:16] singnifica que va a seleccionar los primeros 15 caracteres
                canvas2.drawString(fila_x_peso, fila_y,str(fila[3]))
                canvas2.drawString(fila_x_kg, fila_y, 'Kg')
                
            if contador_fila <= 28:
                
                canvas2.line(10, 600, 600, 600) #LINEA ORIZONTAL ESTA DEBAJO DE PRODUCTO
                canvas2.line(10, linea_horizontal, 600, linea_horizontal) #LINEA ORIZONTAL
                canvas2.line(10, 30, 10, linea_vertical) #LINEA VERTICAL DERECHA 
                canvas2.line(340, 560, 340, linea_vertical) #LINEA VERTICAL IZQUIERDA
                canvas2.line(40, 560, 40, linea_vertical) #LINEA VERTICAL IZQUIERDA
                canvas2.line(180, 560, 180, linea_vertical) #LINEA VERTICAL IZQUIERDA
                canvas2.line(370, 560, 370, linea_vertical) #LINEA VERTICAL 
                canvas2.line(600, 560, 600, linea_vertical) #LINEA VERTICAL 
                canvas2.line(540, 560, 540, linea_vertical) #LINEA VERTICAL 
                linea_horizontal -= 20
                linea_vertical -= 21.7
            
            if contador_fila >= 57:  
                canvas2.line(10, 780, 600, 780) #LINEA ORIZONTAL
                canvas2.line(10, 755, 600, 755) #LINEA ORIZONTAL
                canvas2.line(10, linea_horizontal, 600, linea_horizontal) #LINEA ORIZONTAL
                canvas2.line(10, 780, 10, linea_vertical) #LINEA VERTICAL DERECHA
                canvas2.line(40, 780, 40, linea_vertical) #LINEA VERTICAL IZQUIERDA
                canvas2.line(180, 780, 180, linea_vertical) #LINEA VERTICAL IZQUIERDA
                canvas2.line(340, 780, 340, linea_vertical) #LINEA VERTICAL IZQUIERDA
                canvas2.line(370, 780, 370, linea_vertical) #LINEA VERTICAL 
                canvas2.line(540, 780, 540, linea_vertical) #LINEA VERTICAL 
                canvas2.line(600, 780, 600, linea_vertical) #LINEA VERTICAL 
                linea_horizontal -= 20    
                linea_vertical -= 12

            fecha = str(fila[0]) 
            canvas2.drawString(fila_x_numero, fila_y,str(contador_fila))
            canvas2.drawString(fila_x_fecha, fila_y,fecha[0:16]) #[0:16] singnifica que va a seleccionar los primeros 15 caracteres
            canvas2.drawString(fila_x_peso, fila_y,str(fila[3]))
            canvas2.drawString(fila_x_kg, fila_y, 'Kg')
                
            fila_y -=  20
            contador += 1 
            
            peso_total += float(fila[3])
            contador_fila += 1
            contador_fila2 += 1
         
        #revalua si el conteo de la fila es menor a 85 para dibujar
        #los campos de OPERADOR Y SUPERVISOR 
        if contador_fila < 85:
            canvas2.line(170, fila_y - 340, 240, fila_y - 340) #LINEA ORIZONTAL
            canvas2.line(370, fila_y - 340, 440, fila_y - 340) #LINEA ORIZONTAL
            canvas2.drawString(180,fila_y - 350,'Operador')
            canvas2.drawString(380,fila_y - 350,'Supervisor')
        peso_total = 0.0
        canvas2.save()
        ServerCorreo.ServerCorreo.enviarCorreoReporte(self)