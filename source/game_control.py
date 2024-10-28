import random
import time

from datetime import datetime

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


def template_match(src, template):
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # 进行匹配
    result = cv2.matchTemplate(src_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if SHOW_THRESHOLD:
        print("maxval = ", max_val)
    if max_val >= THRESHOLD:
        _height, _width = template_gray.shape
        max_x, max_y = max_loc

        if IS_SHOW_MATCH_TEMP:
            cv2.rectangle(src, (max_x, max_y), (max_x + _width, max_y + _height), (0, 255, 0), 2)
            cv2.imshow("Template_match", src)
            cv2.waitKey(0)

        return max_x + _width // 2, max_y + _height // 2, max_val

    return None


def templates_match(src, template):
    img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # template = cv2.imread(template, 0)
    h, w = template_gray.shape[:2]

    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    # 取匹配程度大于%90的坐标
    # np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
    all_loc = np.where(res >= 0.90)

    # 圈出匹配部分
    if IS_SHOW_MATCH_TEMPS:
        for pt in zip(*all_loc[::-1]):
            bottom_right = (pt[0] + w, pt[1] + h)
            cv2.rectangle(src, pt, bottom_right, (100, 255, 100), 2)
            print(pt, bottom_right)
        cv2.imshow('Templates_match', src)
        cv2.waitKey(0)

    locs = list(zip(*all_loc[::-1]))
    for i in range(0, len(locs)):
        locs[i] = (locs[i][0] + w // 2, locs[i][1] + h // 2)
    return locs


def template_match_color(src, template):
    # src = src.astype(np.uint8)
    # template = template.astype(np.uint8)
    # 进行匹配
    result = cv2.matchTemplate(src, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= THRESHOLD:
        _height, _width = template.shape
        screen_x, screen_y = max_loc
        return screen_x + _width // 2, screen_y + _height // 2, max_val
    else:
        return None


def post_click(hwnd, client_x, client_y):
    # win32gui.PostMessage(hwnd, win32con.WM_ACTIVATEAPP, 1, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_SETCURSOR, 0, win32api.MAKELONG(win32con.HTCLIENT, win32con.WM_MOUSEMOVE))
    # 模拟鼠标左键单击
    LPARAM = win32api.MAKELONG(client_x, client_y)
    # win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, LPARAM)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, LPARAM)
    # win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, LPARAM)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, LPARAM)


def click_matched(hwnd, x, y, log_text, tInt):
    time.sleep(random.random())
    client_x = x + random.randint(CLICK_OFFSET * -1, CLICK_OFFSET)
    client_y = y + random.randint(CLICK_OFFSET * -1, CLICK_OFFSET)
    post_click(hwnd, client_x, client_y)
    time.sleep(CLICK_INTERVAL)
    print(f'[Clicked] | {hwnd} ({client_x},{client_y})', end='\n——————————————————————————\n')
    # 时间格式 %Y-%m-%d %H:%M:%S
    log_text.insert('end', datetime.now().strftime('%H:%M:%S') + f' | {tInt.get()} | [M]\n')
