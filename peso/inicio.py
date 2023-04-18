import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
import psycopg2
import configm

import inicio
luc = configm.cond
class Inicio(Screen):
    pass

    def generate_number(self):
        self.parent.current = 'rollo'
        idofab=self.ids.idofab.text
        re1 = luc.cursor()
        consulta = "INSERT into of_rollos(ordenf)values ('"+idofab+"')"
        re1.execute(consulta)
        luc.commit()
        count = re1.rowcount
        print("OF Grabada")     
        

Config.set('graphics', 'resizable', True)

Builder.load_file('inicio.kv')

class Root(GridLayout):
    pass


class Main(App):
    def build(self):
        return Root()

    
if __name__ == '__main__':
    Main().run()