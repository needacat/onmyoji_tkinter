import random
import time

import cv2
import numpy as np
import win32api
import win32con
import win32gui

from config import *


def read_pic(tempPath):
    # [:, :, :3] 用于剔除alpha通道
    try:
        with open(tempPath, 'rb') as pic:
            img = cv2.imdecode(np.frombuffer(pic.read(), np.uint8), cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(e)
        return None


def template_matching(src, template):
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # 进行匹配
    result = cv2.matchTemplate(src_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= MATCHING_RATE:
        _height, _width = template_gray.shape
        screen_x, screen_y = max_loc
        print(f'{screen_x}, {screen_y}')
        return screen_x + _width // 2, screen_y + _height // 2, max_val
    else:
        return None


def post_click(hwnd, client_x, client_y):
    win32gui.PostMessage(hwnd, win32con.WM_ACTIVATEAPP, 1, 0)
    win32gui.PostMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)
    win32gui.PostMessage(hwnd, win32con.WM_SETCURSOR, 0, win32api.MAKELONG(win32con.HTCLIENT, win32con.WM_MOUSEMOVE))
    # 模拟鼠标左键单击
    LPARAM = win32api.MAKELONG(client_x, client_y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, LPARAM)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, LPARAM)


def click_matched(hwnd, x, y, log, tInt):
    time.sleep(random.random() + random.randint(0, 1))
    client_x = x + random.randint(CLICK_OFFSET * -1, CLICK_OFFSET)
    client_y = y + random.randint(CLICK_OFFSET * -1, CLICK_OFFSET)
    post_click(hwnd, client_x, client_y)
    # logger.info(f'post {hwnd} {client_x},{client_y}')
    print(f'[P] | {hwnd} ({client_x},{client_y})', end='\n——————————————————————————\n')
    # 时间格式 %Y-%m-%d %H:%M:%S
    # log.insert(tk.END, datetime.now().strftime('%H:%M:%S') + f' | {tInt.get()} | [M]\n')
    time.sleep(2)
