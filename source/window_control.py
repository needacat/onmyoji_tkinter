import subprocess
import traceback

import config
from game_control import *


def post_key(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.2)
    # 发送 WM_KEYUP 消息
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def open_games():
    try:
        subprocess.run(r'start /b ' + V5_PATH, shell=True)
    except:
        traceback.print_exc()


def close_games():
    try:
        _hwnd_list = []
        win32gui.EnumWindows(EnumWindowsProc, _hwnd_list)
        for _hwnd in _hwnd_list:
            win32gui.PostMessage(_hwnd, win32con.WM_QUIT, 0, 0)
    except:
        traceback.print_exc()


def show_window(hwnd):
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, 1)


def resize_window(hwnd, width, height):
    show_window(hwnd)
    x, y, _, _ = win32gui.GetWindowRect(hwnd)
    win32gui.MoveWindow(hwnd, x, y, width, height, True)


def EnumWindowsProc(hwnd, hwnd_list):
    # 检查窗口标题是否包含关键字
    title = win32gui.GetWindowText(hwnd)
    if config.WIN_KEYWORDS in title:
        hwnd_list.append(hwnd)
    return True


def resize_all():
    # 存储符合条件的窗口句柄
    hwnd_list = []

    # 枚举所有顶级窗口，依次调用回调函数
    win32gui.EnumWindows(EnumWindowsProc, hwnd_list)

    if len(hwnd_list) != 0:
        for hwnd in hwnd_list:
            show_window(hwnd)
            resize_window(hwnd, 900, 506)
            win32gui.SetForegroundWindow(hwnd)
