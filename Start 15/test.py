import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

kivy.require('1.11.1')

import os
import urllib.request
import threading

from android.permissions import request_permissions, Permission
request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
request_permissions([Permission.READ_EXTERNAL_STORAGE])

import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


from jnius import autoclass, cast,\
                PythonJavaClass, java_method

PythonActivity = autoclass('org.kivy.android.PythonActivity')
currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
Context = cast('android.content.Context', PythonActivity.getApplicationContext())

Intent = autoclass('android.content.Intent')

Connection = autoclass('android.media.MediaScannerConnection')

MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
AdView = autoclass('com.google.android.gms.ads.AdView')
AdSize = autoclass("com.google.android.gms.ads.AdSize")
AdRequest = autoclass("com.google.android.gms.ads.AdRequest")
AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
AdListener = autoclass("com.google.android.gms.ads.AdListener")
LinearLayout = autoclass("android.widget.LinearLayout")
LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
Bottom = int(80)

from android.runnable import run_on_ui_thread


image_list = ['png', 'gif', 'jbig', 'jbig2', 'jng', 'jpeg', 'mng', 'miff',
'pgm', 'ppm', 'pgf', 'sgi', 'tiff', 'tif', 'jpg']

class Set_DCIM_Path():

    def GET(self):
        DCIM_Image_path = str()

        where_to_find = Context.getExternalFilesDir(None).toString()
        split_where_to_find = where_to_find.split(sep='/')
        for_list_dir = str()

        for repeat in range(len(split_where_to_find)):
            if repeat == 0:
                for_list_dir = '/'
            else:
                for_list_dir += split_where_to_find[repeat] + '/'

            try:
                result_list_dir = os.listdir(for_list_dir)
                dcim_index = result_list_dir.index('DCIM')
                dcim = result_list_dir[dcim_index]
                DCIM_Image_path = str(for_list_dir)+str(dcim)+'/'
                break

            except Exception as EX:
                print('EX:', EX)

        if os.path.isdir(DCIM_Image_path + 'URL Download'):
            return DCIM_Image_path + 'URL Download/'

        else:
            try:
                os.mkdir(DCIM_Image_path + 'URL Download/')
                DCIM_Image_path = DCIM_Image_path + 'URL Download/'

            except:
                pass

            return DCIM_Image_path

Image_path = Set_DCIM_Path().GET()

class Init_AdMob():

    @run_on_ui_thread
    def __init__(self):
        MobileAds.initialize(currentActivity, 'ca-app-pub-') # Add yours
        self._adView = AdView(currentActivity)
        self._adView.setAdSize(AdSize.SMART_BANNER)
        self._adView.setAdUnitId('ca-app-pub-') # Add yours
        self.adRequestBuilder = AdRequestBuilder()
        self.adRequestBuilder.addTestDevice('03F') # Add yours
        self.banerRequest = self.adRequestBuilder.build()
        linearLayout = LinearLayout(currentActivity)
        linearLayout.addView(self._adView)
        layoutParams = LayoutParams(
            LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT
        )
        linearLayout.setLayoutParams(layoutParams)
        linearLayout.setGravity(Bottom)
        currentActivity.addContentView(linearLayout, layoutParams)
        self._adView.loadAd(self.banerRequest)



class Check_Path():
    def check(self):
        update_image_path = Image_path

        return update_image_path

class PythonMediaClient(PythonJavaClass):
    __javainterfaces__ = ['android/media/MediaScannerConnection$MediaScannerConnectionClient']

    @java_method('()V')
    def onMediaScannerConnected(self):
        scan_image_path = Check_Path().check()
        scan_file_list = os.listdir(scan_image_path)

        for image_name in scan_file_list:
            try:
                connection.scanFile(scan_image_path + image_name, None)
            except:
                pass

    @java_method('(Ljava/lang/String;Landroid/net/Uri;)V')
    def onScanCompleted(self, path, uri):
        print('SCAN IS ENDED:', path, uri)


Client = PythonMediaClient()
connection = Connection(Context, Client)


class ContentArea(BoxLayout):
    pass

class Upper_bar(BoxLayout):
    pass

class LocationPop(Popup):
    def __init__(self, **kwargs):
        super(LocationPop, self).__init__(**kwargs)
        self.ids['filechooser'].path = Image_path

class RootWidget(BoxLayout):
    pass

class TestApp(App):


    def build(self):
        Init_AdMob()


    From_Url = str()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.123 Safari/537.36'

    headers={'User-Agent':user_agent}
    progress = 0

    EX=str()

    def Change_Path(self):
        global Image_path
        Image_path = self.Save_path


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
                web_handler = urllib.request.urlopen(request, context=ctx)
                web_binary = web_handler.read()

            except Exception as EX:
                self.EX = str(EX)
                return 3


            file_path = self.Save_path + '/' + self.From_Url.split(sep='/')[-1]
            amout_file_size = len(web_binary)
            thread = self.doing(self.Progress_bar, args=(file_path, amout_file_size, web_binary))
            thread.start()

            return 0


    def Progress_bar(self, file_path, amout_size, data):
        self.root.ids['ContentArea'].ids['Save_Button'].disabled=True

        for repeat in range(0, amout_size, 700):
            with open(file_path, mode='ba') as file_handler:
                if repeat + 700 < amout_size:
                    file_handler.write(data[repeat:repeat+700])

                else:
                    file_handler.write(data[repeat:])

            self.root.ids['ContentArea'].ids['progress'].value = \
            os.stat(file_path).st_size/amout_size * 100.

        self.root.ids['ContentArea'].ids['Save_Button'].disabled=False
        connection.connect()
        connection.disconnect()


    def doing(self, target, args):
        thread = threading.Thread(target=target, args=args)

        return thread



if __name__ == '__main__':
    TestApp().run()
