from distutils.command.config import config
from email.mime import image
from imp import reload
from itertools import count
from logging import root
from select import select
import kivy
import transaction

from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import time
import serial
from kivy.clock import Clock
from datetime import datetime, timezone
from kivy.uix.image import Image
from kivy.properties import StringProperty
from inicio import Inicio
from kivy.core.window import Window
import random
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import os, errno
import psycopg2
import configm
from funciones import ReporteCorreo
luc = configm.cond
lio = configm.cnsap

Window.clearcolor = (0.5, 0.5, 0.5, 1)

Window.maximize()

class P(FloatLayout):
    pass

class Px(FloatLayout):
    pass
    def derribo(self):
        self.parent.current = 'rollo'

#CLASE PARA ABRIR UN POPUP Y PESAR EL PRIMER CANUTO
#AL MOMENTO QUE SE PESA, SE CIERRA EL POPUP
class PopupNuevoCanuto2(Popup):
    def cerrar_canuto_primero(self):
        print("Pesar primer canuto")
        print('click')
         
        ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout=1,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
        ser.isOpen()  
        
        while 1 :
            bytesToRead = ser.inWaiting()
            data = ser.read(bytesToRead)
            time.sleep(1)
            if not data:
                print('sin data')
            else:
                x = str(data).replace("b'", "")
                #y = x[:-1]
                y = x[-6:-1]
                
                #open mensaje
                
                print(y) 
                dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                #insertamos registro de peso
                re6 = luc.cursor()
                id_maquina = luc.cursor()

                #cargo of a guardar en canuto
                consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' and estado='nuevo' order by id desc limit 1 "
                re6.execute(consulta2)
                rowse = re6.fetchall()
                re6.close()

                #extraigo el id de la máquina
                consulta_id = "SELECT id FROM maquina_of where maquina='103' and estado='nuevo' order by id desc limit 1 "
                id_maquina.execute(consulta_id)
                id = id_maquina.fetchone()
                id_maquina_of = id[0]
                id_maquina.close()

                yytt2=0
                for row in rowse:
                    yytt2 = str(row[0])
                    n = random.randint(100,99999)
                    codi="CAN"+yytt2+"_"+str(n)
                    #quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"
                    
                    re7 = luc.cursor()
                    peso = float(y)
                    consulta = "INSERT into peso_canuto(fecha_creacion, ofab,codigo,id_maquina_of,peso)values ('"+dt+"','"+yytt2+"','"+codi+"','"+str(id_maquina_of)+"','"+str(peso)+"')"
                    
                    re7.execute(consulta)
                    
                    re7.close()
                    print("Peso canuto grabado") 
                print('Canuto pesado.')
                ser.close()
                Popup.dismiss(self)
                break

#CLASE PARA ABRIR UN POPUP Y PESAR EL PRIMER CANUTO
#AL MOMENTO QUE SE PESA, SE CIERRA EL POPUP
class PopupUltimoRollo2(Popup):
    def cerrar_rollo_ultimo(self):
        print("Pesar ultimo  rollo")
        print('click')
        
        ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout=1,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
        ser.isOpen()  
        
        while 1 :
            bytesToRead = ser.inWaiting()
            data = ser.read(bytesToRead)
            time.sleep(1)
            if not data:
                print('sin data')
            else:
                x = str(data).replace("b'", "")
                #y = x[:-1]
                y = x[-6:-1]
                peso = float(y)
                #open mensaje
                
                print(y) 
                dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                #insertamos registro de peso
                re21 = luc.cursor()
                #cargo of a guardar en canuto
                consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' order by id desc limit 1 "
                re21.execute(consulta2)
                rowse = re21.fetchall()
                re21.close()
                yytt2=0 

                #obtenemos el id de maquina_of
                codigo_id = luc.cursor()
                consulta_id = "SELECT id FROM maquina_of where maquina='103' order by id desc limit 1 "
                codigo_id.execute(consulta_id)
                id = codigo_id.fetchone()
                id_maquina_of = id[0]
                codigo_id.close()

                for row in rowse:
                    yytt2 = str(row[0])
                    n = random.randint(100,99999)
                    codif=yytt2+"_"+str(n)
                    quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"
                    cur = luc.cursor()
                    consulta = "INSERT into peso_materia(fecha_creacion, peso,ofab,codcanuto,codrollo,estado, id_maquina_of)values ('"+dt+"','"+str(peso)+"','"+yytt2+"',"'('+quy+')'",'"+codif+"','habilitado', '"+str(id_maquina_of)+"')"
                    cur.execute(consulta)
                    luc.commit()
                    count = cur.rowcount
                    cur.close()
                    print("Peso rollo grabado") 
                 
                    re23 = luc.cursor() 
                    #impresion
                    consulta = "select a.id_peso_mat,b.of_rollos, b.maquina, b.operador, a.codrollo,a.peso from peso_materia a, maquina_of b where a.ofab=b.of_rollos and b.estado='nuevo' and b.maquina='103' order by id_peso_mat desc limit 1"
                    re23.execute(consulta)
                    cd = re23.fetchone()
                    ofs=cd[1]
                    re23.close()
                    sp1 = lio.cursor()
                    qrysp1='SELECT a."DocNum", a."ItemCode", a."ProdName", c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN "SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" where a."DocNum"='+ofs+' '
                    sp1.execute(qrysp1)
                    cds = sp1.fetchone()
                    pp=cds[1]
                    sp1.close()
                    
                    #toma el ultimo peso del canuto
                    can = luc.cursor()   
                    canuto = 'SELECT peso FROM peso_canuto WHERE id_peso_canuto = (SELECT max(id_peso_canuto) FROM peso_canuto) '
                    can.execute(canuto)
                    ultimo_canuto = can.fetchone()
                    peso_canuto = ultimo_canuto[0]
                    can.close()
                    #SE TOMA EL PESO DEL ROLLO MENOS EL PESO DEL CANUTO
                    peso_fin = float(cd[5]) - float(peso_canuto) 
                    fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')
                    
                    #DISEÑO DEL TICKET 
                    fline1="\nÓRDEN DE FAB: "+cd[1]+"     MÁQUINA:150\n\n"
                    fline1a="CÓDIGO PRODUCTO: "+cds[1]+"\n"
                    fline1b="PRODUCTO: "+cds[2]+"\n"
                    fline1c="GRUPO: "+cds[3]+"\n\n"
                    fline1d="PESO: "+str(peso_fin)+"\n\n"
                    fline2="            CÓDIGO ROLLO \n"
                    fline3="          "+cd[4]+"\n\n"
                    fline5= "FECHA: " + fecha_actual+"\n"
                    fline4="OPERADOR: "+cd[3]

                    ftotal=fline1+fline1a+fline1b+fline1c+fline1d+fline2+fline3+fline5+fline4
                    os.remove("maquina2.txt")
                    f = open("maquina2.txt", "a+")
                    f.write(ftotal)
                    f.close()
                    os.system('lpr "maquina2.txt"')
                ser.close()
                break
        

        Popup.dismiss(self)
  
class Rollod(Screen):
    def __init__(self, **kwargs):
        self.peso_canuto = 0.0
        self.contador = 0
        super(Rollod, self).__init__(**kwargs)
        print('inicie')

    def cerrar_canuto_primero(self):
        print("Pesar primer canuto")
        print('click')
         
        ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout=1,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
        ser.isOpen()  
        
        while 1 :
            bytesToRead = ser.inWaiting()
            data = ser.read(bytesToRead)
            time.sleep(1)
            if not data:
                print('sin data')
            else:
                x = str(data).replace("b'", "")
                #y = x[:-1]
                y = x[-6:-1]
                
              
                #open mensaje
                
                print(y) 
                dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                #insertamos registro de peso
                re6 = luc.cursor()
                id_maquina = luc.cursor()

                #cargo of a guardar en canuto
                consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' and estado='nuevo' order by id desc limit 1 "
                re6.execute(consulta2)
                rowse = re6.fetchall()
                re6.close()

                #extraigo el id de la máquina
                consulta_id = "SELECT id FROM maquina_of where maquina='103' and estado='nuevo' order by id desc limit 1 "
                id_maquina.execute(consulta_id)
                id = id_maquina.fetchone()
                id_maquina_of = id[0]
                id_maquina.close()

                yytt2=0
                for row in rowse:
                    yytt2 = str(row[0])
                    n = random.randint(100,99999)
                    codi="CAN"+yytt2+"_"+str(n)
                    #quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"
                    
                    re7 = luc.cursor()
                    peso = float(y)
                    consulta = "INSERT into peso_canuto(fecha_creacion, ofab,codigo,id_maquina_of,peso)values ('"+dt+"','"+yytt2+"','"+codi+"','"+str(id_maquina_of)+"','"+str(peso)+"')"
                    
                    re7.execute(consulta)
                    
                    re7.close()
                    print("Peso canuto grabado") 
                print('Canuto pesado.')
                ser.close()
                break

    def cerrar_rollo_ultimo(self):
        print("Pesar ultimo  rollo")
        print('click')
        
        ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout=1,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
        ser.isOpen()  
        
        while 1 :
            bytesToRead = ser.inWaiting()
            data = ser.read(bytesToRead)
            time.sleep(1)
            if not data:
                print('sin data')
            else:
                x = str(data).replace("b'", "")
                #y = x[:-1]
                y = x[-6:-1]
                peso = float(y)
                #open mensaje
                
                print(y) 
                dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                #insertamos registro de peso
                re21 = luc.cursor()
                #cargo of a guardar en canuto
                consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' order by id desc limit 1 "
                re21.execute(consulta2)
                rowse = re21.fetchall()
                re21.close()
                yytt2=0 

                #obtenemos el id de maquina_of
                codigo_id = luc.cursor()
                consulta_id = "SELECT id FROM maquina_of where maquina='103' order by id desc limit 1 "
                codigo_id.execute(consulta_id)
                id = codigo_id.fetchone()
                id_maquina_of = id[0]
                codigo_id.close()

                for row in rowse:
                    yytt2 = str(row[0])
                    n = random.randint(100,99999)
                    codif=yytt2+"_"+str(n)
                    quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"
                    cur = luc.cursor()
                    consulta = "INSERT into peso_materia(fecha_creacion, peso,ofab,codcanuto,codrollo,estado, id_maquina_of)values ('"+dt+"','"+str(peso)+"','"+yytt2+"',"'('+quy+')'",'"+codif+"','habilitado', '"+str(id_maquina_of)+"')"
                    cur.execute(consulta)
                    luc.commit()
                    count = cur.rowcount
                    cur.close()
                    print("Peso rollo grabado") 
                 
                    re23 = luc.cursor() 
                    #impresion
                    consulta = "select a.id_peso_mat,b.of_rollos, b.maquina, b.operador, a.codrollo,a.peso from peso_materia a, maquina_of b where a.ofab=b.of_rollos and b.estado='nuevo' and b.maquina='103' order by id_peso_mat desc limit 1"
                    re23.execute(consulta)
                    cd = re23.fetchone()
                    ofs=cd[1]
                    re23.close()
                    sp1 = lio.cursor()
                    qrysp1='SELECT a."DocNum", a."ItemCode", a."ProdName", c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN "SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" where a."DocNum"='+ofs+' '
                    sp1.execute(qrysp1)
                    cds = sp1.fetchone()
                    pp=cds[1]
                    sp1.close()
                    
                    #toma el ultimo peso del canuto
                    can = luc.cursor()   
                    canuto = 'SELECT peso FROM peso_canuto WHERE id_peso_canuto = (SELECT max(id_peso_canuto) FROM peso_canuto) '
                    can.execute(canuto)
                    ultimo_canuto = can.fetchone()
                    peso_canuto = ultimo_canuto[0]
                    can.close()
                    #SE TOMA EL PESO DEL ROLLO MENOS EL PESO DEL CANUTO
                    peso_fin = float(cd[5]) - float(peso_canuto) 
                    fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')
                    
                    #DISEÑO DEL TICKET 
                    fline1="\nÓRDEN DE FAB: "+cd[1]+"     MÁQUINA:150\n\n"
                    fline1a="CÓDIGO PRODUCTO: "+cds[1]+"\n"
                    fline1b="PRODUCTO: "+cds[2]+"\n"
                    fline1c="GRUPO: "+cds[3]+"\n\n"
                    fline1d="PESO: "+str(peso_fin)+"\n\n"
                    fline2="            CÓDIGO ROLLO \n"
                    fline3="          "+cd[4]+"\n\n"
                    fline5= "FECHA: " + fecha_actual+"\n"
                    fline4="OPERADOR: "+cd[3]

                    ftotal=fline1+fline1a+fline1b+fline1c+fline1d+fline2+fline3+fline5+fline4
                    os.remove("maquina2.txt")
                    f = open("maquina2.txt", "a+")
                    f.write(ftotal)
                    f.close()
                    os.system('lpr "maquina2.txt"')
                ser.close()
                break

    def tomar_peso_canuto(self, peso):
        return peso

    def iniciomaq1(self):
        print("") #enviar a 

    def comenzar(self):
        btncapturar = self.ids.btncapturar
        btncapturar.disabled=False

    def maquinauno(self):
            
        cur = luc.cursor()
        #extraigo ultima of no finalizada de la maquina 102, pregunto si existo
        consulta = "SELECT of_rollos FROM maquina_of where maquina='102' and estado not in ('finalizado') order by id desc limit 1 "
        cur.execute(consulta)
        cd = cur.fetchone()
        #ofrollo=cd[0]
        #con.close ()

        if cd == None:
            self.parent.current = 'maquinadatos'
        else:
            self.parent.current = 'rollo'
        
   
    def maquinatres(self):
        cur = luc.cursor()
        #extraigo ultima of no finalizada de la maquina 102, pregunto si existo
        consulta = "SELECT of_rollos FROM maquina_of where maquina='104' and estado not in ('finalizado') order by id desc limit 1 "
        cur.execute(consulta)
        cd = cur.fetchone()
        #ofrollo=cd[0]

        if cd == None:
            self.parent.current = 'maquinadatos3'
        else:
            self.parent.current = 'rollot'

    def finalizo(self):
            #reporte = ReporteCorreo.ReporteCorreo('Samuel Valero')
            #reporte.imprimirReporte()
            print('Reporte enviado')
            self.parent.current = 'finalizary'

    def continuar(self):
        btncap2 = self.ids.btncap2
        btncapturar = self.ids.btncapturar
        btnpesodesperdicio = self.ids.btnpesodesperdicio
        btncapturarf = self.ids.btncapturarf
        copiado = self.ids.copiado
        btn_cerrart = self.ids.btn_cerrart
       
        btncanuto = self.ids.btncanuto
        btnpesorollo = self.ids.btnpesorollo
        operador = self.ids.operador
        btnpesodesperdicio = self.ids.btnpesodesperdicio
        maq1 = self.ids.maq1
        maq2 = self.ids.maq2
        maq3 = self.ids.maq3
        chkfinca = self.ids.chkfinca

        btncapturar.disabled = False
        btncapturar.size_hint_y='.4'
        btncapturar.size_hint_x='.4'
        btncapturar.width='200'
        btncapturar.opacity='1'
        btncapturarf.disabled = True
        btncapturarf.size_hint_y=None
        btncapturarf.size_hint_x=None
        btncapturarf.width='0'
        btncapturarf.opacity='0' 
        btncapturarf.text='' 
        
        copiado.text=''

        re1 = luc.cursor()

        #BOTONES DE MAQUINAS
        #extraigo ultima of no finalizada de la maquina 102, pregunto si existo
        consulta = "SELECT of_rollos FROM maquina_of where maquina='102' and estado not in ('finalizado') order by id desc limit 1 "
        re1.execute(consulta)
        cd = re1.fetchone()
        
        if cd==None:
            maq1.background_color=(0.5, 0.5, 0.5, 0.2)
            ofrollo='Libre'
        else:
            ofrollo=cd[0]

        re1.close()

        re2 = luc.cursor()

        conx = "SELECT of_rollos FROM maquina_of where maquina='103' and estado not in ('finalizado') order by id desc limit 1 "
        re2.execute(conx)
        cd = re2.fetchone()
        if cd==None:
            maq2.background_color=(0.5, 0.5, 0.5, 0.2)
            ofrollo2='Libre'
        else:
            ofrollo2=cd[0]

        re2.close()

        re3 = luc.cursor()
        
        cony = "SELECT of_rollos FROM maquina_of where maquina='104' and estado not in ('finalizado') order by id desc limit 1 "
        re3.execute(cony)
        cd = re3.fetchone()
        if cd==None:
            maq3.background_color=(0.5, 0.5, 0.5, 0.2)
            ofrollo3='Libre'
        else:
            ofrollo3=cd[0]

        maq1.text='MÁQUINA #1\n'+ofrollo
        maq2.text='MÁQUINA #2\n'+ofrollo2
        maq3.text='MÁQUINA #3\n'+ofrollo3

        re3.close()
        #FIN BOTONES DE MAQUINAS

        re4 = luc.cursor()

        consultaop = "SELECT operador FROM maquina_of where maquina='103' order by id desc limit 1"
        re4.execute(consultaop)
        cd = re4.fetchone()
        operador.text='OPERADOR: '+cd[0]

        re4.close()
        
        if cd == None:
            print('no hay ordenes activas')
            #show_popup()
        else:
            print('es nueva?')
        
            re5 = luc.cursor()

            consulta = "SELECT canuto,rollo FROM auditoria where of='"+ofrollo2+"' "
            print(consulta)
            re5.execute(consulta)
            cd = re5.fetchone()
            ofrollocan=cd[0]
            print(ofrollocan)
            if ofrollocan == 1:
                print('ahora peso rollo')
                chkfinca.opacity=1
                chkfinca.disabled=False
                btnpesorollo.disabled=False
                btncanuto.disabled=True
                btncap2.disabled=True
                btncapturar.disabled=True
                #btncapturarc.disable=True 
                btn_cerrart.disable=True
                btnpesodesperdicio.disabled=False
                #show_popup()
            else:
                print('ahora peso canuto') 
                chkfinca.opacity=0
                chkfinca.disabled=True
                #btncapturarc.disable=True 
                btncapturar.disabled=True  
                btnpesorollo.disabled=True
                btncanuto.disabled=False
                btncap2.disabled=True
                btn_cerrart.disable=True
                btnpesodesperdicio.disabled=False

            re5.close()

    def comenzart(self):
        btncapturar = self.ids.btncapturar
        btncapturar.disabled=False
        
    #FUNCIÓN PARA PESAR EL PRIMER CANUTO
    def pesar_canuto_primero(self):
        print('CANUTO PRIMERO')
        try:
            self.cerrar_canuto_primero()
            popup = Popup(title='Canuto primero',
                    content=Label(text='Canuto pesado correctamente!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
        except:
            popup = Popup(title='Alerta',
                    content=Label(text='Error de conexión'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()


        #popup = PopupNuevoCanuto2()
        #popup.open()

        #btnprimercanuto = self.ids.btncanutoprimero
        #btnprimercanuto.disabled = False

    #FUNCION PARA PESAR EL ÚLTIMO ROLLO   
    def pesar_rollo_ultimo(self):
        print('ROLLO ULTIMO')
        try:
            self.cerrar_rollo_ultimo()
            popup = Popup(title='Rollo último',
                    content=Label(text='Útimo rollo pesado correctamente!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
        except:
            popup = Popup(title='Alerta!',
                    content=Label(text='Errorm pese el rollo de nuevo!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()

        #popup = PopupUltimoRollo2()
        #popup.open()
    
#Extraigo peso CANUTO -------------------------------------------
    def extraer_pesorc(self): #SE LLAMA EN LA FUNCION accion()
        try:
            btncap2 = self.ids.btncap2
            btncapturar = self.ids.btncapturar
            #btncapturarc = self.ids.btncapturarc        
            btn_cerrart = self.ids.btn_cerrart
            btn_fin = self.ids.btn_fin
            btn_printer = self.ids.btn_printer
            btncanuto = self.ids.btncanuto
            btnpesorollo = self.ids.btnpesorollo
            btnpesodesperdicio = self.ids.btnpesodesperdicio
            copiado = self.ids.copiado
            mensaje = self.ids.lblcorrecto
            ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
            ser.isOpen()  
            
            while 1 :
                bytesToRead = ser.inWaiting()
                data = ser.read(bytesToRead)
                time.sleep(1)
                if not data:
                    print('sin data')
                else:
                    x = str(data).replace("b'", "")
                    #y = x[:-1]
                    y = x[-6:-1]
                    peso = float(y)
                    self.peso_canuto = self.tomar_peso_canuto(y)
                    #open mensaje
                    
                    print(y) 
                    dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                    #insertamos registro de peso
                    re6 = luc.cursor()
                    id_maquina = luc.cursor()

                    #cargo of a guardar en canuto
                    consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' and estado='nuevo' order by id desc limit 1 "
                    re6.execute(consulta2)
                    rowse = re6.fetchall()
                    re6.close()

                    #extraigo el id de la máquina
                    consulta_id = "SELECT id FROM maquina_of where maquina='103' and estado='nuevo' order by id desc limit 1 "
                    id_maquina.execute(consulta_id)
                    id = id_maquina.fetchone()
                    id_maquina_of = id[0]
                    id_maquina.close()

                    yytt2=0
                    for row in rowse:
                        yytt2 = str(row[0])
                        n = random.randint(100,99999)
                        codi="CAN"+yytt2+"_"+str(n)
                        #quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"
                        
                        re7 = luc.cursor()
                    
                        consulta = "INSERT into peso_canuto(fecha_creacion, ofab,codigo,id_maquina_of,peso)values ('"+dt+"','"+yytt2+"','"+codi+"','"+str(id_maquina_of)+"','"+str(peso)+"')"
                        
                        re7.execute(consulta)

                        re7.close()

                        re8 = luc.cursor()

                        actaudito = "UPDATE auditoria SET canuto='1',rollo='0' where of='"+yytt2+"' "
                        print(actaudito)
                        re8.execute(actaudito)
                    
                        luc.commit()

                        re8.close()

                        count = re8.rowcount
                        print("Peso canuto grabado") 
                        copiado.text='PESO GRABADO CORRECTAMENTE'
                        btncap2.disabled=False
                        btncanuto.disabled=True
                        btnpesorollo.disabled=True
                        btn_cerrart.disabled=False
                        btn_fin.disabled=True
                        btn_printer.disabled=True
                        btncapturar.disabled=True
                        #btncapturarc.disabled=True
                    ser.close()
                    break
        except:
            popup = Popup(title='Alerta!',
                    content=Label(text='Error, pese el canuto de nuevo!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
        
                
#Extraigo peso ROLLO -------------------------------------------
    #ESTE FUNCION SE EJECUTA AL PRECIONAR EL BOTON CAPTURAR AL MOMENTO
    #DE PESAR, CANUTO, ROLLO O DESPERDICIO
    def accion(self):
        try:
            re9 = luc.cursor()
            #REALIZA UNA CONSULTA DONDE LA MÁQUINA NO ESTE FINALIZADA
            consulta = "SELECT of_rollos FROM maquina_of where maquina='103' and estado not in ('finalizado') order by id desc limit 1 "
            re9.execute(consulta)
            cd = re9.fetchone()
            ofrollo=cd[0] #TOMO EL NUMERO DE ROLLO 
            re9.close()

            #REALIZA UNA CONSULTA A AUDITORIA PARA TOMAR VALOR 1 O 0 
            #DEPENDIENDO DE ELLO SE EJECUTARA UNA ACCION PARA IMPRIMIR UN TICKET
            re10 = luc.cursor()
            consultax = "SELECT canuto,rollo,desperdicio FROM auditoria where of='"+ofrollo+"' "
            print(consultax)
            re10.execute(consultax)
            cd = re10.fetchone()
            ofrollocan=cd[0] #TOMA EL VALOR DE CANUTO 0 O 1
            ofrollo=cd[1]    #TOMA EL VALOR DE ROLLO 0 O 1 
            ofdesp=cd[2]     #TOMA EL VALOR DE DESPERDICIO 0 O 1

            re10.close()

            print(ofrollocan)
            if ofdesp == 1: #SI DESPERDICIO ES 1 TOMA EL PESO DE DESPERDICIO
                print("me fui a desp")
                self.extraer_pesord()
            elif ofrollocan == 1:  #SI ROLLO ES 0 TOMA EL PESO DE ROLLO
                print("me fui a pes rol")
                self.extraer_pesor()
            else:
                print("me fui a pes can") #TOMA EL PESO DEL CANUTO
                self.extraer_pesorc()
            transaction.commit()
        except:
            transaction.abort()
            popup = Popup(title='Alerta!',
                    content=Label(text='Error, por favor, pese de nuevo!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
     
       

#Extraigo peso ROLLO FINCA -------------------------------------------
       
    def on_checkbox_active(self, checkbox, value):
        btncapturarf = self.ids.btncapturarf
        btncapturar = self.ids.btncapturar

        if value:
            print('The checkbox is active')
            btncapturarf.disabled = False
            btncapturarf.size_hint_y=.4
            btncapturarf.size_hint_x=.4
            btncapturarf.width=700
            btncapturarf.opacity=1 
            btncapturarf.text='CAPTURAR P. FINCA'  

            btncapturar.disabled = True
            btncapturar.size_hint_y=None
            btncapturar.size_hint_x=None
            btncapturar.width=0
            btncapturar.opacity=0

        else:
            print('The checkbox is inactive')
            btncapturar.disabled = False
            btncapturar.size_hint_y='.4'
            btncapturar.size_hint_x='.4'
            btncapturar.width='200'
            btncapturar.opacity='1'

            btncapturarf.disabled = True
            btncapturarf.size_hint_y=None
            btncapturarf.size_hint_x=None
            btncapturarf.width='0'
            btncapturarf.opacity='0' 
            btncapturarf.text='' 

    def accionf(self): 
        try:
                print('calidad finca')
                btncap2 = self.ids.btncap2
                btncapturar = self.ids.btncapturar
                btn_cerrart = self.ids.btn_cerrart
                btn_fin = self.ids.btn_fin
                btn_printer = self.ids.btn_printer
                btncanuto = self.ids.btncanuto
                btnpesorollo = self.ids.btnpesorollo
                btnpesodesperdicio = self.ids.btnpesodesperdicio
                copiado = self.ids.copiado
                mensaje = self.ids.lblcorrecto
                ser = serial.Serial(
                port='/dev/ttyUSB0', #PUERTO USB DE DE IMPERESORA
                baudrate=9600,
                timeout=1,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.SEVENBITS
            )
                ser.isOpen()  
                
                while 1 :
                    bytesToRead = ser.inWaiting()
                    data = ser.read(bytesToRead)
                    time.sleep(1)
                    if not data:
                        print('sin data')
                    else:
                        x = str(data).replace("b'", "")
                        #y = x[:-1]
                        y = x[-6:-1]
                        peso = float(y)
                        #open mensaje
                        
                        print(y) 
                        dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                        #insertamos registro de peso
                        #cargo of a guardar en canuto
                        re11 = luc.cursor()
                        maquina = luc.cursor()

                        consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' order by id desc limit 1 "
                        re11.execute(consulta2)
                        rowse = re11.fetchall()
                        re11.close()

                        #consulta para extraer el id de la maquina
                        consulta_id= "SELECT id FROM maquina_of where nombre='102' order by id desc limit 1 "
                        maquina.execute(consulta_id)
                        id_maquina = maquina.fetchone()
                        id_maquina_of = id_maquina[0]
                        id_maquina.close()

                        yytt2=0
                        for row in rowse:
                            yytt2 = str(row[0])
                            n = random.randint(100,99999)
                            codif=yytt2+"_"+str(n)

                            re12 = luc.cursor()

                            quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"

                            re12.close()

                            re13 = luc.cursor()

                            consulta = "INSERT into peso_materia(fecha_creacion, peso,ofab,codcanuto,codrollo,estado,finca, id_maquina_of)values ('"+dt+"','"+str(peso)+"','"+yytt2+"',"'('+quy+')'",'"+codif+"','habilitado','finca','"+str(id_maquina_of)+"')"
                            re13.execute(consulta)

                            re13.close()

                            re14 = luc.cursor()

                            actaudito = "UPDATE auditoria SET canuto='0',rollo='1' where of='"+yytt2+"' "
                            print(actaudito)
                            re14.execute(actaudito)
                            luc.commit()
                            re14.close()
                            count = re14.rowcount
                            print("Peso rollo finca grabado") 
                            copiado.text='PESO GRABADO CORRECTAMENTE'
                            btncap2.disabled=False
                            btnpesorollo.disabled=True
                            btn_cerrart.disabled=False
                            btn_fin.disabled=False
                            btn_printer.disabled=False
                            btncapturar.disabled=True

                            #impresion
                            re15 = luc.cursor()
                            consulta = "select a.id_peso_mat,b.of_rollos, b.maquina, b.operador, a.codrollo,a.peso from peso_materia a, maquina_of b where a.ofab=b.of_rollos and b.estado='nuevo' and b.maquina='103' and a.finca='finca' order by id_peso_mat desc limit 1"
                            re15.execute(consulta)
                            cd = re15.fetchone()
                            ofs=cd[1]
                            re15.close()
                            sp1 = lio.cursor()
                            qrysp1='SELECT a."DocNum", a."ItemCode", a."ProdName", c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN "SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" where a."DocNum"='+ofs+' '
                            sp1.execute(qrysp1)
                            cds = sp1.fetchone()
                            pp=cds[1]
                            sp1.close()

                            peso_fin = float(cd[5]) - float(self.peso_canuto)
                            fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')

                            fline1="\nÓRDEN DE FAB: "+cd[1]+"     MÁQUINA:150\n\n"
                            fline1a="CÓDIGO PRODUCTO: "+cds[1]+"\n"
                            fline1b="PRODUCTO: "+cds[2]+"\n"
                            fline1c="GRUPO: "+cds[3]+"\n\n"
                            fline1d="PESO: "+str(peso_fin)+"\n\n"
                            fline2="     CÓDIGO ROLLO FINCA \n"
                            fline3="          "+cd[4]+"\n\n"
                            fline5 ="FECHA: " +fecha_actual+"\n"
                            fline4="OPERADOR: "+cd[3]
                            ftotal=fline1+fline1a+fline1b+fline1c+fline1d+fline2+fline3+fline5+fline4
                            os.remove("maquina2.txt")
                            f = open("maquina2.txt", "a+")
                            f.write(ftotal)
                            f.close()
                            os.system('lpr "maquina2.txt"')
                        ser.close()
                        break
        except:
            popup = Popup(title='Alerta!',
                    content=Label(text='Error, pese finca de nuevo!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
        



#Extraigo peso ROLLO FINCA -------------------------------------------

    def cambio_turno(self):
        self.parent.current = 'cambiotx2'

    def desperdicio(self):
        btncap2 = self.ids.btncap2
        btncapturar = self.ids.btncapturar
        btncapturar.disabled=False
        btncanuto = self.ids.btncanuto
        btnpesorollo = self.ids.btnpesorollo
        btncanuto.disabled=True
        btnpesorollo.disabled=True
        btncap2.disabled=True

        re16 = luc.cursor()

        consulta = "SELECT of_rollos FROM maquina_of where maquina='103' and estado not in ('finalizado') order by id desc limit 1 "
        re16.execute(consulta)
        cd = re16.fetchone()

        re16.close()

        of=cd[0]    

        re17 = luc.cursor()    
        consultax = "UPDATE auditoria set desperdicio=1 where of='"+of+"'"
        print (consultax)
        re17.execute(consultax)         
        luc.commit()
        re17.close()

    def extraer_pesord(self): #ESTA FUNCION SE LLAMA EN LA FUNCION acccion() 
        try:                      #SE ENCARGA DE TOMAR EL PESO DE DESPERDICIO
            btncap2 = self.ids.btncap2
            btncapturar = self.ids.btncapturar
            btn_cerrart = self.ids.btn_cerrart
            btn_fin = self.ids.btn_fin
            btn_printer = self.ids.btn_printer
            btncanuto = self.ids.btncanuto
            btnpesorollo = self.ids.btnpesorollo
            btnpesodesperdicio = self.ids.btnpesodesperdicio
            copiado = self.ids.copiado
            mensaje = self.ids.lblcorrecto
            ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
            ser.isOpen()  
            
            while 1 :
                bytesToRead = ser.inWaiting()
                data = ser.read(bytesToRead)
                time.sleep(1)
                if not data:
                    print('sin data')
                else:
                    x = str(data).replace("b'", "")
                    #y = x[:-1]
                    y = x[-6:-1]
                    peso = float(y)
                    #open mensaje
                    
                    print(y) 
                    dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                    #insertamos registro de peso
                    re18 = luc.cursor() 
                    #cargo of a guardar en canuto
                    consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' order by id desc limit 1 "
                    re18.execute(consulta2)
                    rowse = re18.fetchall()
                    re18.close()
                    yytt2=0

                    #obtenemos el id de maquina_of
                    codigo_id = luc.cursor()
                    consulta_id = "SELECT id FROM maquina_of where maquina='103' order by id desc limit 1 "
                    codigo_id.execute(consulta_id)
                    id = codigo_id.fetchone()
                    id_maquina_of = id[0]
                    codigo_id.close()


                    for row in rowse:
                        yytt2 = str(row[0])
                        n = random.randint(100,99999)
                        codi="ROL"+yytt2+"_"+str(n)
                        re19 = luc.cursor()
                        consulta = "INSERT into peso_desperdicio(fecha,ofab,peso, id_maquina_of)values ('"+dt+"','"+yytt2+"','"+str(peso)+"', '"+str(id_maquina_of)+"')"
                        re19.execute(consulta)
                        re19.close()
                        re20 = luc.cursor()
                        actaudito = "UPDATE auditoria SET desperdicio='0' where of='"+yytt2+"' "
                        print(actaudito)
                        re20.execute(actaudito)
                        luc.commit()
                        count = re20.rowcount
                        re20.close()
                        print("Peso desperdicio grabado") 
                        copiado.text='PESO GRABADO CORRECTAMENTE'
                        btncap2.disabled=False
                        btnpesorollo.disabled=True
                        btn_cerrart.disabled=False
                        btn_fin.disabled=False
                        btn_printer.disabled=False
                        btncapturar.disabled=True
                    ser.close()
                    break
        except:
            popup = Popup(title='Alerta!',
                    content=Label(text='Error, pese desperdicio de nuevo!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()

#peso rollo
    def extraer_pesor(self): #ESTA FUNCION SE LLAMA EN LA FUNCION accion()
        try:                 #ES LA ENCARGADA DE GENERAR EL TICKET DEL PESO DEL ROLLO
            btncap2 = self.ids.btncap2
            btncapturar = self.ids.btncapturar
            btn_cerrart = self.ids.btn_cerrart
            btn_fin = self.ids.btn_fin
            btn_printer = self.ids.btn_printer
            btncanuto = self.ids.btncanuto
            btnpesorollo = self.ids.btnpesorollo
            btnpesodesperdicio = self.ids.btnpesodesperdicio
            copiado = self.ids.copiado
            mensaje = self.ids.lblcorrecto
            ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
            ser.isOpen()  
            
            while 1 :
                bytesToRead = ser.inWaiting()
                data = ser.read(bytesToRead)
                time.sleep(1)
                if not data:
                    print('sin data')
                else:
                    x = str(data).replace("b'", "")
                    #y = x[:-1]
                    y = x[-6:-1]
                    peso = float(y)
                    #open mensaje
                    
                    print(y) 
                    dt = datetime.today().strftime('%Y-%m-%d %H:%M')
                    #insertamos registro de peso
                    re21 = luc.cursor()
                    #cargo of a guardar en canuto
                    consulta2 = "SELECT of_rollos FROM maquina_of where maquina='103' order by id desc limit 1 "
                    re21.execute(consulta2)
                    rowse = re21.fetchall()
                    re21.close()
                    yytt2=0 

                    #obtenemos el id de maquina_of
                    codigo_id = luc.cursor()
                    consulta_id = "SELECT id FROM maquina_of where maquina='103' order by id desc limit 1 "
                    codigo_id.execute(consulta_id)
                    id = codigo_id.fetchone()
                    id_maquina_of = id[0]
                    codigo_id.close()

                    for row in rowse:
                        yytt2 = str(row[0])
                        n = random.randint(100,99999)
                        codif=yytt2+"_"+str(n)
                        quy="select codigo from peso_canuto where ofab='"+yytt2+"' order by id_peso_canuto DESC limit 1"
                        cur = luc.cursor()
                        consulta = "INSERT into peso_materia(fecha_creacion, peso,ofab,codcanuto,codrollo,estado, id_maquina_of)values ('"+dt+"','"+str(peso)+"','"+yytt2+"',"'('+quy+')'",'"+codif+"','habilitado', '"+str(id_maquina_of)+"')"
                        cur.execute(consulta)
                        actaudito = "UPDATE auditoria SET canuto='0',rollo='1' where of='"+yytt2+"' "
                        print(actaudito)
                        cur.execute(actaudito)
                        luc.commit()
                        count = cur.rowcount
                        cur.close()
                        print("Peso rollo grabado") 
                        copiado.text='PESO GRABADO CORRECTAMENTE'
                        btncap2.disabled=False
                        btnpesorollo.disabled=True
                        btn_cerrart.disabled=False
                        btn_fin.disabled=False
                        btn_printer.disabled=False
                        btncapturar.disabled=True
                        re23 = luc.cursor() 
                        #impresion
                        consulta = "select a.id_peso_mat,b.of_rollos, b.maquina, b.operador, a.codrollo,a.peso from peso_materia a, maquina_of b where a.ofab=b.of_rollos and b.estado='nuevo' and b.maquina='103' order by id_peso_mat desc limit 1"
                        re23.execute(consulta)
                        cd = re23.fetchone()
                        ofs=cd[1]
                        re23.close()
                        sp1 = lio.cursor()
                        qrysp1='SELECT a."DocNum", a."ItemCode", a."ProdName", c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN "SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" where a."DocNum"='+ofs+' '
                        sp1.execute(qrysp1)
                        cds = sp1.fetchone()
                        pp=cds[1]
                        sp1.close()

                        #SE TOMA EL PESO DEL ROLLO MENOS EL PESO DEL CANUTO
                        peso_fin = float(cd[5]) - float(self.peso_canuto) 
                        fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')

                        #DISEÑO DEL TICKET 
                        fline1="\nÓRDEN DE FAB: "+cd[1]+"     MÁQUINA:150\n\n"
                        fline1a="CÓDIGO PRODUCTO: "+cds[1]+"\n"
                        fline1b="PRODUCTO: "+cds[2]+"\n"
                        fline1c="GRUPO: "+cds[3]+"\n\n"
                        fline1d="PESO: "+str(peso_fin)+"\n\n"
                        fline2="            CÓDIGO ROLLO \n"
                        fline3="          "+cd[4]+"\n\n"
                        fline5= "FECHA: " + fecha_actual+"\n"
                        fline4="OPERADOR: "+cd[3]

                        ftotal=fline1+fline1a+fline1b+fline1c+fline1d+fline2+fline3+fline5+fline4
                        os.remove("maquina2.txt")
                        f = open("maquina2.txt", "a+")
                        f.write(ftotal)
                        f.close()
                        os.system('lpr "maquina2.txt"')
                    ser.close()
                    break
        except:
            popup = Popup(title='Alerta!',
                    content=Label(text='Error, pese rollo de nuevo!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()


    def printer(self):
        re22 = luc.cursor()
        #cargo of a guardar en canuto

        consulta = "select a.id_peso_mat,b.of_rollos, b.maquina, b.operador, a.codrollo,a.peso from peso_materia a, maquina_of b where a.ofab=b.of_rollos and b.estado='nuevo' and b.maquina='103' order by id_peso_mat desc limit 1"
        re22.execute(consulta)
        cd = re22.fetchone()
        ofs=cd[1]
        re22.close()
        sp1 = lio.cursor()
        qrysp1='SELECT a."DocNum", a."ItemCode", a."ProdName", c."ItmsGrpNam" FROM "SUPRALIVE_PRD"."OWOR" a INNER JOIN "SUPRALIVE_PRD"."OITM" b ON a."ItemCode" = b."ItemCode" INNER JOIN "SUPRALIVE_PRD"."OITB" c ON b."ItmsGrpCod" = c."ItmsGrpCod" where a."DocNum"='+ofs+' '
        sp1.execute(qrysp1)
        cds = sp1.fetchone()
        pp=cds[1]
        sp1.close()

        peso_fin = float(cd[5]) - float(self.peso_canuto) 
        fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')

        fline1="\nÓRDEN DE FAB: "+cd[1]+"     MÁQUINA:150\n\n"
        fline1a="CÓDIGO PRODUCTO: "+cds[1]+"\n"
        fline1b="PRODUCTO: "+cds[2]+"\n"
        fline1c="GRUPO: "+cds[3]+"\n\n"
        fline1d="PESO: "+str(peso_fin)+"\n\n"
        fline2="            CÓDIGO ROLLO \n"
        fline3="          "+cd[4]+"\n\n"
        fline5="FECHA: " + fecha_actual+"\n"
        fline4="OPERADOR: "+cd[3]
        ftotal=fline1+fline1a+fline1b+fline1c+fline1d+fline2+fline3+fline5+fline4
        os.remove("maquina2.txt")
        f = open("maquina2.txt", "a+")
        f.write(ftotal)
        f.close()
        os.system('lpr "maquina2.txt"')
            

Config.set('graphics', 'resizable', True)
Builder.load_file('rollo.kv')

class Root(GridLayout):
    pass

class Main(App):
    def build(self):
        return Root()
    
if __name__ == '__main__':
    Main().run()