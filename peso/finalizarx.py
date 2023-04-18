from cgitb import text
from this import d
from turtle import title
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from hdbcli import dbapi
from datetime import datetime, timezone
from validaciones import campos_vacios
from funciones import ReporteCorreo
import configm
import psycopg2

luc = configm.cond


class Finalizarx(Screen):
    pass

    def regresar(self):
        self.parent.current = 'rollo'

    def validar_usuario(self):
        user = self.ids.login
        pwd = self.ids.password
        info = self.ids.rlabel

        uname = user.text
        password = pwd.text

        # valido para que el usuario ingrese los datos
        if len(uname) == 0 or len(password) == 0:
            popup = Popup(title='Alerta',
                          content=Label(
                              text='Por favor, ingrese su usuario y contraseña!'),
                          size_hint=(None, None), size=(410, 150))
            popup.open()
        else:
            re2 = luc.cursor()
            # consulta el usuario que esta usando la maquina
            consulta = "SELECT password, nombres FROM usuarios WHERE username='" + \
                uname+"' and estado=1"
            re2.execute(consulta, uname)
            rows = re2.fetchall()
            re2.close
            for row in rows:
                tpassword = row[0]
                print(password)
                print(tpassword)

                if uname == '' or password == '':
                    info.text = 'usuario y/o contraseña son requeridas'
                else:
                    if password == tpassword:
                        info.text = 'Bienvenido ' + row[1] + ' !!'
                        re3 = luc.cursor()

                        # imprime el reporte.
                        # self.imprimirReporte()
                        # finalizo uso de maquina
                        fina = "UPDATE parada set estado='inactivo' where id_parada='1' "
                        re3.execute(fina)
                        re3.close()

                        reporte = ReporteCorreo.ReporteCorreo(str(uname))
                        reporte.imprimirReporte()

                        re4 = luc.cursor()
                        consulint = "SELECT ordenf from of_troquelado where parada='1' order by id desc limit 1"
                        re4.execute(consulint)
                        cd = re4.fetchone()
                        re4.close()
                        of = cd[0]

                        re5 = luc.cursor()
                        finb = "UPDATE of_troquelado set estado='finalizado' where ordenf='" + \
                            of+"' and parada='1'  "
                        print(finb)
                        re5.execute(finb)

                        luc.commit()
                        re5.close()
                        # Main.stop(self)
                        # self.root.destroy()
                        self.parent.current = 'login'

                    else:
                        info.text = '| X | Usuario y/o contraseña incorrectas'


Config.set('graphics', 'resizable', True)

Builder.load_file('finalizarx.kv')


class Root(GridLayout):
    pass


class Main(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    Main().run()
