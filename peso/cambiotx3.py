from cgitb import text
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from hdbcli import dbapi
from datetime import datetime, timezone
import configm

import psycopg2
luc = configm.cond


class Cambiotx3(Screen):
    pass

    def validar_usuario(self):
        user = self.ids.login
        pwd = self.ids.password
        info = self.ids.rlabel
        operador = self.ids.idoperador

        uname = user.text
        password = pwd.text
        opera = operador.text

        re1 = luc.cursor()
        consulta_id_maquina = luc.cursor()

        consulta = "SELECT ordenf FROM of_troquelado where parada='3' and estado not in ('finalizado') order by id desc limit 1 "
        re1.execute(consulta)
        cd = re1.fetchone()
        re1.close()
        ofrollo = cd[0]

        # CONSULTA PARA OBTENER EL ID DE LA TABLA MAQUINA
        consulta = "SELECT id_parada FROM parada where id_parada='3'"
        consulta_id_maquina.execute(consulta)
        id = consulta_id_maquina.fetchone()
        consulta_id_maquina.close()
        id_maquina = id[0]

        # linea para agregar la fecha
        dt = datetime.today().strftime('%Y-%m-%d %H:%M')

        re2 = luc.cursor()
        consulta = "SELECT password, nombres FROM usuarios WHERE username='" + \
            uname+"' and estado=1"
        re2.execute(consulta, uname)
        rows = re2.fetchall()
        re2.close()
        for row in rows:
            tpassword = row[0]
            print(password)
            print(tpassword)

            if uname == '' or password == '':
                info.text = 'usuario y/o contraseña son requeridas'
            else:
                if password == tpassword:
                    info.text = 'Bienvenido ' + row[1] + ' !!'
                    conx = configm.cond
                    curx = conx.cursor()
                    re3 = luc.cursor()

                    consultag = "INSERT into of_troquelado(ordenf,usuario,estado,parada) values ('" + \
                        ofrollo+"','"+uname+"','activo','3')"
                    re3.execute(consultag)
                    luc.commit()

                    re3.close()
                    print(consultag)
                    self.parent.current = 'rollot'

                else:
                    info.text = '| X | Usuario y/o contraseña incorrectas'


Config.set('graphics', 'resizable', True)

Builder.load_file('cambiotx3.kv')


class Root(GridLayout):
    pass


class Main(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    Main().run()
