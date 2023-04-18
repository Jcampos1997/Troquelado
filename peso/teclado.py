# import kivy module
import kivy
	
kivy.require("1.9.1")
from kivy.app import App
from kivy.uix.vkeyboard import VKeyboard
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class Teclado(Screen):
    def __init__(self, **kwargs):
        super(Teclado, self).__init__(**kwargs)
        print('inicie')

class Test(VKeyboard):
	player = VKeyboard()

# Create the App class
class VkeyboardApp(App):
	def build(self):
		return Test()
Builder.load_file('teclado.kv')	

# run the App
if __name__ == '__main__':
	VkeyboardApp().run()
