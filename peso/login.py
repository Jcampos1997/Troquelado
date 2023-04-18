from cgitb import text
#from tkinter import Button
from turtle import onclick
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from hdbcli import dbapi
from kivy.uix.vkeyboard import VKeyboard 
import configm #ARCHIVO DE LA CONEXIÓN A LA BASE DE DATOS
from funciones import ReporteCorreo103
import psycopg2

luc = configm.cond
class Teclado(VKeyboard): 
    player = VKeyboard()

class VkeyboardApp(App): 
    def build(self): 
        return Teclado()

#CLASE LOGIN        
class Login(Screen):
    pass

 #se enviara el reporte en pdf una vez que 
    #finalize la orden de fabricacion
    #este método se ejecutara dentro del
    #método validar_usuario
    def imprimirReporte(self):
        ultima_consulta = luc.cursor()
        reporte  = luc.cursor() 
        ultima_orden_fabricacion = "SELECT pm.ofab "\
	                               "FROM peso_materia pm "\
	                               "INNER JOIN maquina_of mo ON mo.id = pm.id_maquina_of "\
	                               "INNER JOIN peso_desperdicio pd ON mo.id = pd.id_maquina_of "\
	                               "GROUP BY pm.Fecha_creacion,mo.operador,pm.ofab,pm.id_peso_mat "\
	                               "ORDER BY pm.id_peso_mat DESC LIMIT 1"
        
        ultima_consulta.execute(ultima_orden_fabricacion)
        orden_fab = ultima_consulta.fetchone()
        orden = str(orden_fab[0])
       

        consulta = "SELECT CONCAT(EXTRACT(year FROM pm.fecha_creacion)," \
                   "EXTRACT(MONTH FROM pm.fecha_creacion),"\
	               "EXTRACT(day FROM pm.fecha_creacion)),"\
	               "EXTRACT(HOUR FROM pm.fecha_creacion),"\
	               "pm.fecha_creacion, "\
                   "pm.ofab, mo.operador,"\
	               "SUM(pm.peso),"\
	               "SUM(pd.peso) "\
	               "FROM peso_materia pm "\
	               "INNER JOIN maquina_of mo ON mo.id = pm.id_maquina_of "\
	               "INNER JOIN peso_desperdicio pd ON mo.id = pd.id_maquina_of "\
	               "WHERE pm.ofab like " + orden + \
                   " GROUP BY pm.Fecha_creacion,mo.operador,pm.ofab, pm.id_peso_mat "\
	               "ORDER BY pm.id_peso_mat DESC"
             
        reporte.execute(consulta)
        orden_fab = reporte.fetchall()
        
        for fila in orden_fab:
            print("Fecha: {} , Hora: {}, Fecha Creación {}, Orden Fab:{},\
                  Operador: {}, Peso Ok: {}, Peso Desp: {}".format(fila[0],fila[1], fila[2],
                                                                   fila[3], fila[4], fila[5],
                                                                   fila[6]))

     #FUNCION PARA VALIDAR A UN USUARIO QUE VA A INGRESAR AL SISTEMA 
    def validar_usuario(self):
        user = self.ids.login
        pwd = self.ids.password
        info = self.ids.rlabel
        #reporte = ReporteCorreo103.ReporteCorreo103('Frank')
        #reporte.imprimirReporte()

        uname = user.text  #NOMBRE DE USUARIO  
        password = pwd.text #PASSWORD

        if len(uname) == 0 or len(password) == 0:
            #contenido  = Button(text="Imprimir datos", onclick=)
            popup = Popup(title='Alerta',
                    content=Label(text='Por favor, ingrese su usuario y contraseña!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
        else:
            #con = dbapi.connect(address='10.254.254.254',port=30015,user='SVAGRT_DBREADER',password='dPtWhDwV2aRHR5bA')
            re1 = luc.cursor()
            #consulta ='SELECT a."StreetNoW",a."StreetNoW" FROM "DB_SUPRALIVE_PRUEBAS"."OHEM" a where a."jobTitle"=\'SUPERVISOR EXPANDIDO\' and  a."StreetNoW"='+uname+' '
            #print(consulta)

            #self.imprimirReporte()

            #REALIZAMOS LA CONSULTA SQL PARA ENCONTRAR EL USUARIO(EL USUARIO DEBE ESTAR EN estado=1 o activo)
            consulta = "SELECT password, nombres FROM usuarios WHERE username='"+uname+"' and estado=1"
            re1.execute(consulta)
            rows = re1.fetchall()
            re1.close()
            for row in rows:
                    tpassword = row[0]
            
                    if uname == '' or password == '':
                        info.text = 'usuario y/o contraseña son requeridas'
                    else: 
                        if password == tpassword:
                            print(row[1])
                        
                            info.text = 'Bienvenido '+ row[1] +' !!'
                            self.parent.current = 'maquina' #EN CASO DE QUE LOS DATOS DE INGRESO
                                                            #SEAN CORRECTOS
                                                            #PERMITE QUE SE  MUESTRE
                                                            #LA PANTALLA DE MAQUINAS

                        else:
                            info.text = 'Usuario y/o contraseña incorrectas'
                            #info.text TOMA UN TEXTO PARA MOSTRAR UN MENSAJE.
                
Config.set('graphics', 'resizable', True) #EVITA QUE SE REDIMENCIONE LA PANTALLA

Builder.load_file('login.kv') #CARGA LOS EL DISEÑO QUE ESTA EN EL ARCHIVO login.kv

class Root(GridLayout):
    pass


class Main(App):
    def build(self):
        return Root()

    
if __name__ == '__main__':
    Main().run()