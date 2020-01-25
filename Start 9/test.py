import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

kivy.require('1.11.1')

import os

class ContentArea(BoxLayout):
    pass

class Upper_bar(BoxLayout):
    pass

class LocationPop(Popup):
    def __init__(self, **kwargs):
        super(LocationPop, self).__init__(**kwargs)
        self.ids['filechooser'].path = os.getcwd()

class TestApp(App):
    pass

if __name__ == '__main__':
    TestApp().run()
