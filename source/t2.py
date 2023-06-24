import ctypes
import subprocess
from tkinter import Tk, Button

from source.game_control import *


def callback(chwnd, param):
    if win32gui.GetWindowText(chwnd) == '隔离打开程序':
        post_click(chwnd, 63, 20)
        time.sleep(0.6)
        post_click(chwnd, 63, 20)
        time.sleep(0.6)


def t():
    subprocess.run(r'start /b E:\Download\Compressed\V5多开\V5.exe', shell=True)
    time.sleep(0.65)
    _v5_hwnd = win32gui.FindWindow(None, 'V5 程序多开器 0.1 Beta')
    win32gui.EnumChildWindows(_v5_hwnd, callback, None)
    win32api.PostMessage(_v5_hwnd, win32con.WM_CLOSE, 0, 0)


ctypes.windll.shcore.SetProcessDpiAwareness(2)
main = Tk()
main.geometry('350x300+700+400')
main.attributes('-topmost', True)
main.resizable(False, False)

btn = Button(main, width=5, command=t, text='Start')
btn.grid(row=0, column=1, sticky='n')

main.mainloop()
