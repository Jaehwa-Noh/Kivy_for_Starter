import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

kivy.require('1.11.1')

import os
import urllib.request

image_list = ['png', 'gif', 'jbig', 'jbig2', 'jng', 'jpeg', 'mng', 'miff',
'pgm', 'ppm', 'pgf', 'sgi', 'tiff', 'tif', 'jpg']

class ContentArea(BoxLayout):
    pass

class Upper_bar(BoxLayout):
    pass

class LocationPop(Popup):
    def __init__(self, **kwargs):
        super(LocationPop, self).__init__(**kwargs)
        self.ids['filechooser'].path = os.getcwd()

class RootWidget(BoxLayout):
    pass

class TestApp(App):
    Save_path = os.getcwd()
    From_Url = str()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.123 Safari/537.36'

    headers={'User-Agent':user_agent}
    progress = 0

    def Save(self):
        if (self.From_Url is str()):
            return 1

        else:
            if self.From_Url.split(sep='/')[-1].split(sep='.')[-1].lower() not in image_list:
                return 1

            if os.path.isfile(self.Save_path + '/' + self.From_Url.split(sep='/')[-1]):
                return 2

            try:
                request = urllib.request.Request(url=self.From_Url, data=None, headers=self.headers)
                web_handler = urllib.request.urlopen(request)
                web_binary = web_handler.read()

            except:
                return 1


            file_path = self.Save_path + '/' + self.From_Url.split(sep='/')[-1]
            amout_file_size = len(web_binary)
            self.Progress_bar(file_path, amout_file_size, web_binary)


            return 0


    def Progress_bar(self, file_path, amout_size, data):

        for repeat in range(0, amout_size, 5000):
            with open(file_path, mode='ba') as file_handler:
                if repeat + 5000 < amout_size:
                    file_handler.write(data[repeat:repeat+5000])

                else:
                    file_handler.write(data[repeat:])

            print(repeat)
            self.root.ids['ContentArea'].ids['progress'].value = \
            os.stat(file_path).st_size/amout_size * 100.







if __name__ == '__main__':
    TestApp().run()
