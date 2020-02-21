import test_android
import test_window
from kivy.utils import platform

print('platform:', platform)

if __name__ == '__main__':
    if platform == 'android':
        test_android.Test_androidApp().run()

    if platform == 'win':
        test_window.Test_windowApp().run()
