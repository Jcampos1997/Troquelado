

from email.mime import image
from imp import reload
from itertools import count
from logging import root
from tkinter import W, Button
from turtle import onclick
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import configm

luc = configm.cond
Window.clearcolor = (0.5, 0.5, 0.5, 1)  # SE ESTABLECE UN COLOR DE FONDO

Window.maximize()  # MAXIMIZA EL TAMAÑO DE LA VENTANA


class Px(FloatLayout):

    def envio(self):
        print('kivy')
        Clock.schedule_once(self.changeScreen, 3)

    def changeScreen(self, *args):
        # now switch to the screen 1
        self.parent.current = "rollo"


class Px2(FloatLayout):

    def envio(self):
        print('kivy')
        Clock.schedule_once(self.changeScreen, 3)

    def changeScreen(self, *args):
        # now switch to the screen 3
        self.parent.current = "rollod"


class Px3(FloatLayout):

    def envio(self):
        print('kivy')
        Clock.schedule_once(self.changeScreen, 3)

    def changeScreen(self, *args):
        # now switch to the screen 3
        self.parent.current = "rollot"


# LA CLASE MAQUINA CON TIENE LOS CÓDIGOS QUE NOS PERMITIRÁN USAR LAS MÁQUINAS 105, 150 Y 170
class Maquina(Screen):
    def __init__(self, **kwargs):
        super(Maquina, self).__init__(**kwargs)
        print('inicie')
        # connect DB

    # FUNCIÓN PARA LA PARADA 1, ESTA FUNCIÓN SE LLAMA EN EL ARCHIVO maquina.kv
    def maq_uno(self):
        def show_popup():  # MUESTRA UN POPUP O UNA ALERTA
            show = Px()
            popupWindow = Popup(title="PARADA OCUPADA", content=show, size_hint=(
                None, None), size=(300, 150))
            popupWindow.open()
        re1 = luc.cursor()
        # contar cantidad de rollos pesados
        consulta = "SELECT id_parada FROM parada where id_parada='1' and estado='activo'"
        re1.execute(consulta)
        cd = re1.fetchone()
        re1.close()
        if cd == None:
            print('no existo')
            self.parent.current = 'maquinadatos'  # ABRE LA VENTATA DE maquina.py
        else:
            print('si existo')
            show_popup()

    def envio(self):
        self.parent.current = 'rollo'

    # FUNCIÓNN PARA LA PARADA 2, ESTA FUNCIÓN SE LLAMA EN EL ARCHIVO maquina.kv
    def maq_dos(self):

        def show_popup2():
            show = Px2()
            popupWindow = Popup(title="PARADA OCUPADA", content=show, size_hint=(
                None, None), size=(300, 150))
            popupWindow.open()

        re2 = luc.cursor()
        # contar cantidad de rollos pesados
        consulta = "SELECT id_parada FROM parada where id_parada='2' and estado='activo'"
        re2.execute(consulta)
        cd = re2.fetchone()
        re2.close()
        if cd == None:
            print('no existo')
            self.parent.current = 'maquinadatos2'
        else:
            print('si existo')
            show_popup2()

    # FUNCIÓN PARA LA PARADA 3, ESTA FUNCIÓN SE LLAMA EN EL ARCHIVO maquina.kv
    def maq_tres(self):
        def show_popup3():
            show = Px3()
            popupWindow = Popup(title="PARADA OCUPADA", content=show, size_hint=(
                None, None), size=(300, 150))
            popupWindow.open()
        re3 = luc.cursor()
        # contar cantidad de rollos pesados
        consulta = "SELECT id_parada FROM parada where id_parada='3' and estado='activo'"
        re3.execute(consulta)
        cd = re3.fetchone()
        re3.close()
        if cd == None:
            print('no existo')
            self.parent.current = 'maquinadatos3'
        else:
            print('si existo')
            show_popup3()


kivy.require('2.0.0')
# PERMITE QUE LAS VENTANA SE PUEDA REDIMENSIONAR
Config.set('graphics', 'resizable', True)


class Root(GridLayout):
    pass


class Main(App):
    def build(self):
        # PERMITE CARGAR EL DISEÑO QUE ESTA DENTRO DE maquina.kv
        return Builder.load_file('maquina.kv')


if __name__ == '__main__':
    Main().run()
