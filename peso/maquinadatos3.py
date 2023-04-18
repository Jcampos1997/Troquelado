from email.mime import image
from imp import reload
from itertools import count
from logging import root
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import time
# import serial
import psycopg2
from kivy.clock import Clock
from datetime import datetime, timezone
from kivy.uix.image import Image
from kivy.properties import StringProperty
from inicio import Inicio
from kivy.core.window import Window
import random
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import configm
luc = configm.cond
Window.clearcolor = (0.5, 0.5, 0.5, 1)

Window.maximize()


class P(FloatLayout):
    pass


class Maquinadatos3(Screen):
    def __init__(self, **kwargs):
        super(Maquinadatos3, self).__init__(**kwargs)
        print('inicie')
        # connect DB

    def regresar(self):
        self.parent.current = 'maquina'

    def iniciomaq1(self):
        print("")  # enviar a

    def inicioprocesom1(self):
        ofmaq = self.ids.txt_ofmaq1.text
        opmaq = self.ids.txt_opmaq1.text

        # VALIDACION PARA EVITAR INGRESAR DATOS VACIOS
        if len(ofmaq) == 0 or len(opmaq) == 0:
            popup = Popup(title='Alerta',
                          content=Label(
                              text='Por favor, ingrese una orden de fabricación y un operador!'),
                          size_hint=(None, None), size=(410, 150))
            popup.open()
        else:
            fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')
            # insertamos registro de peso
            re1 = luc.cursor()

            consulta_id_maquina = luc.cursor()

            # OBTENER EL ID DE LA MAQUINA
            consulta = "SELECT id_parada FROM parada where id_parada='3'"
            consulta_id_maquina.execute(consulta)
            id = consulta_id_maquina.fetchone()
            id_maquina = id[0]
            consulta_id_maquina.close()

            consulta = "INSERT into of_troquelado(ordenf, usuario, estado, parada)values ('" + \
                ofmaq+"','','Procesando','3')"
            re1.execute(consulta)
            # SE ACTUALIZAR LA TABLA DE AUDITORIA DE TROQUELADO
            consultax = "INSERT into auditoria_troquelado(peso_rollo,peso_picado,ordenf) values ('0','1','"+ofmaq+"')"
            re1.execute(consultax)
            act_parada = "UPDATE parada set estado='activo' where id_parada='3'"
            re1.execute(act_parada)
            luc.commit()
            count = re1.rowcount
            re1.close()
            print("Parada #3 iniciada")
            self.parent.current = 'rollot'
            # Clock.schedule_once(self.setup, 3)


Config.set('graphics', 'resizable', True)
Builder.load_file('maquinadatos3.kv')


class Root(GridLayout):
    pass


class Main(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    Main().run()
