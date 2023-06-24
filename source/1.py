import win32gui


def EnumChildProc(hwnd, lParam):
    class_name = win32gui.GetClassName(hwnd)
    text = win32gui.GetWindowText(hwnd)
    print('Child window:', hwnd, class_name, text)

    return True


# 获取窗口句柄
hwnd = win32gui.FindWindow(None, '阴阳师-网易游戏')
print(hwnd)

win32gui.EnumWindows(EnumChildProc, None)
# 枚举子窗口
win32gui.EnumChildWindows(hwnd, EnumChildProc, None)
