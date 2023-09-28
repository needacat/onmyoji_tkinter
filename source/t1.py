# _*_coding:utf-8_*_
# 作者：   Java Punk
# 时间：   2022-10-09 14:49:45

import cv2 as cv2
import numpy as np


def get_index(x, y):
    def get_i(num):
        if 0 <= num < 0.33:
            return 0
        elif 0.33 <= num < 0.66:
            return 1
        elif 0.66 <= num <= 1:
            return 2

    # 结界图片偏移
    _offset_x = -94
    _offset_y = -93
    _w = 626
    _h = 249

    _rate_x = round((x + _offset_x) / _w, 3)
    _rate_y = round((y + _offset_y) / _h, 3)
    # print(f"{x},{y} = ", end="")
    return get_i(_rate_x) + get_i(_rate_y) * 3


def templates_match1111(src, template):
    img = cv2.imread(src)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    h, w = template.shape[:2]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 取匹配程度大于%90的坐标
    threshold = 0.9
    # np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
    all_loc = np.where(res >= threshold)
    locs = list(zip(*all_loc[::-1]))
    for loc in locs:
        loc[0] -= w // 2
        loc[1] -= h // 2
    return locs


# 多个模板匹配
def templates_match(image, templ):
    img = cv2.imread(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templ, 0)
    h, w = template.shape[:2]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 取匹配程度大于%90的坐标
    threshold = 0.9
    # np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
    loc = np.where(res >= threshold)
    locs = list(zip(*loc[::-1]))
    print(locs[1][1])
    for pt in zip(*loc[::-1]):
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img, pt, bottom_right, (100, 255, 100), 2)
        # print(pt, bottom_right)
    cv2.imshow('img_rgb', img)
    cv2.waitKey(0)


def templates_match_origin(image, templ):
    img = cv2.imread(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(templ, 0)
    h, w = template.shape[:2]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 取匹配程度大于%90的坐标
    threshold = 0.9
    # np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img, pt, bottom_right, (100, 255, 100), 1)
        print(pt, bottom_right)
    cv2.imshow('img_rgb', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    # 图片路径自己设置，下面是我本地的路径，记得替换！！！
    templates_match('../resource/img.png', '../resource/Filed_Finished.png')
