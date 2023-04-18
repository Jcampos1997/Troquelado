from kivy.uix.popup import Popup
from kivy.uix.label import Label


def validar_entranda(texto1, texto2):

    if len(texto1) == 0 or len(texto2) == 0:
            popup = Popup(title='Alerta',
                    content=Label(text='Por favor, llene todos los campos!'),
                    size_hint=(None, None), size=(410, 150))
            popup.open()
    
    

    


        