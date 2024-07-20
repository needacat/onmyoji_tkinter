import threading
from datetime import *
from tkinter import *
from tkinter.ttk import Combobox

from screen_capture import *
from window_control import *
from config import *


def set_ui():
    def plus30(event):
        tInt.set(tInt.get() + 30)

    def btnClear():
        log_text.delete('0.0', END)
        tInt.set(0)

    def switchOption(event):
        if combobox_mission.current() == 2:
            combobox_mission.current(0)
        else:
            combobox_mission.current(combobox_mission.current() + 1)

    global entry_count, btn_start, btn_stop, btn_clear, btn_resize, log_text, combobox_mission

    main.title('OSS by 1y')
    main.wm_iconbitmap(ICON)
    main.protocol('WM_DELETE_WINDOW', on_closing)
    main.geometry('367x260+760+640')
    main.attributes('-topmost', True)
    main.resizable(False, False)

    tInt.set(DEFAULT_COUNT)

    log_text = Text(main, width=30, spacing2=10, height=10)
    log_text.place(x=0, y=2, width=198, height=250)
    # 次数label
    label_count = Label(main, text='Times:')
    label_count.place(x=200, y=0, width=50)
    label_count.bind('<Button-1>', plus30)
    # 次数输入框
    entry_count = Entry(main, textvariable=tInt)
    entry_count.place(x=265, y=0, width=100)
    # 选项label
    label_option = Label(main, text='Option: ')
    label_option.place(x=200, y=25, width=65)
    label_option.bind('<Button-1>', switchOption)
    # 选项下拉框
    combobox_mission = Combobox(main, values=['御魂', '斗技', '结界'], state='readonly')
    combobox_mission.place(x=265, y=25, width=100)
    combobox_mission.set('御魂')
    btn_start = Button(main, width=5, command=start_mission, text='Start')
    btn_start.place(x=200, y=52, width=82)
    btn_stop = Button(main, width=5, command=lambda: tInt.set(0), text='Stop', state='disabled')
    btn_stop.place(x=283, y=52, width=82)
    btn_clear = Button(main, width=5, command=btnClear, text='Clear')
    btn_clear.place(x=200, y=87, width=82)
    btn_resize = Button(main, width=5, command=lambda: resize_all(), text='Resize')
    btn_resize.place(x=283, y=87, width=82)
    btn_open = Button(main, width=10, command=open_games, text='Open')
    btn_open.place(x=200, y=122, width=82)
    btn_exit = Button(main, width=10, command=close_games, text='Close')
    btn_exit.place(x=283, y=122, width=82)


def start_mission():
    global combobox_mission, TEMP_LIST, LOOP_FLAG
    select_mission = combobox_mission.get()
    if select_mission == '御魂':
        TEMP_LIST = YuHun
        LOOP_FLAG = TEMP_LIST[2]
        threading.Thread(target=orochi).start()
    elif select_mission == '斗技':
        TEMP_LIST = DouJi
        LOOP_FLAG = TEMP_LIST[1]
        threading.Thread(target=orochi).start()
    elif select_mission == '结界':

        threading.Thread(target=field).start()


def enable_widget():
    entry_count['state'] = NORMAL
    btn_start['state'] = NORMAL
    btn_start['text'] = 'Start'
    btn_stop['state'] = DISABLED
    combobox_mission['state'] = 'readonly'


def disable_widget():
    entry_count['state'] = DISABLED
    btn_start['state'] = DISABLED
    btn_start['text'] = 'Running'
    btn_stop['state'] = NORMAL
    combobox_mission['state'] = DISABLED


def orochi():
    if tInt.get() <= 0:
        tInt.set(DEFAULT_COUNT)
    disable_widget()

    hwnd_list = []
    win32gui.EnumWindows(EnumWindowsProc, hwnd_list)
    _last_matched = False

    while tInt.get() > 0:
        for _hwnd in hwnd_list:
            show_window(_hwnd)
            with ScreenCapture() as _sc:
                _sc.capture(_hwnd)
                for _temp_name in TEMP_LIST:
                    _img = _sc.get_image()
                    _temp = read_pic(RESOURCE_PATH + _temp_name)
                    if _img is None or _temp is None:
                        enable_widget()
                        return
                    _match_result = template_match(_img, _temp)
                    if _match_result:
                        if _temp_name == LOOP_FLAG and _last_matched != LOOP_FLAG:
                            tInt.set(tInt.get() - 1)
                        _last_matched = _temp_name
                        _match_x, _match_y, _max_val = _match_result
                        print(f'[M] | {_temp_name[:-4]}')
                        print(f'[R] | {_max_val:.2f}')
                        print(f'[L] | ({_match_x},{_match_y})')
                        log_text.insert('end', f'{_temp_name[:-4]}\n')
                        click_matched(_hwnd, _match_x, _match_y, log_text, tInt)
                        break
            time.sleep(M_INTERVAL)
    enable_widget()


def field():
    def get_i(num):
        if 0 <= num < 0.33:
            return 0
        elif 0.33 <= num < 0.66:
            return 1
        elif 0.66 <= num <= 1:
            return 2

    def get_index(x, y):

        # 结界图片偏移
        _offset_x = -94
        _offset_y = -93
        _w = 626
        _h = 249

        _rate_x = round((x + _offset_x) / _w, 3)
        _rate_y = round((y + _offset_y) / _h, 3)
        return get_i(_rate_x) + get_i(_rate_y) * 3

    if tInt.get() <= 0:
        tInt.set(FILED_DEFAULT_COUNT)
    print('---------结界突破---------')
    disable_widget()

    hwnd_list = []
    _sc = ScreenCapture()
    # 获取所有阴阳师的窗口句柄
    win32gui.EnumWindows(EnumWindowsProc, hwnd_list)
    # 定义 hwnd:counts 的字典
    _down_grade = {}
    # 初始化窗口属性
    for hwnd in hwnd_list:
        _down_grade[hwnd] = [0, False, False]
    while tInt.get() > 0:
        if len(hwnd_list) <= 0:
            enable_widget()
            return
        for hwnd in hwnd_list:
            for _temp in Filed:
                # 浅拷贝结界位置list
                _filed_locs = Filed_Locs[:]
                _sc.capture(hwnd)
                _matched_loc = template_match(_sc.get_image(), read_pic(RESOURCE_PATH + _temp))
                _sc.release()
                # 若是最后一个模板未匹配到，匹配下一个窗口；否则继续匹配下一个模板。
                if _matched_loc is None and _temp == Filed[-1]:
                    break
                elif _matched_loc is None:
                    continue
                # print(f'matched {_temp}')
                # 匹配到的是进攻按钮则直接点击
                if _temp == 'Filed_Attack.png':
                    # 判断进攻标志
                    if _down_grade[hwnd][2] == False:
                        tInt.set(tInt.get() - 1)
                        click_matched(hwnd, _matched_loc[0], _matched_loc[1], log_text, tInt)
                        _down_grade[hwnd][2] == True
                    else:
                        hwnd_list.remove(hwnd)
                        break
                # 匹配到在进攻结界场景中
                elif _temp == 'Filed_Attacking.png':
                    # 重置 进攻标志
                    _down_grade[hwnd][2] == False
                    # 若降级次数大于1则点击返回退出进攻
                    if _down_grade[hwnd][0] > 0:
                        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
                        time.sleep(0.08)
                        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)
                        # 结界降级次数减1
                        _down_grade[hwnd][0] = _down_grade[hwnd][0] - 1
                        print(f'降级 = {_down_grade[hwnd][0]}')
                        time.sleep(1)
                # 匹配到在结界突破主界面，计算可突破结界数
                elif _temp == 'Filed_Scene.png':
                    _sc.capture(hwnd)
                    # 依次匹配成功*2、失败*2共四个模板
                    for _temp1 in Filed_Count:
                        # 结界降级次数不为0，则计算可突破结界数时不排除战败结界
                        if (_temp1 == 'Filed_Failed1.png' or _temp1 == 'Filed_Failed2.png') and _down_grade[
                            hwnd][0] > 0:
                            continue
                        _matched_locs = templates_match(_sc.get_image(), read_pic(RESOURCE_PATH + _temp1))
                        if _matched_locs is None:
                            continue
                        for _loc in _matched_locs:
                            index = get_index(_loc[0], _loc[1])
                            # 多目标匹配会有重复，导致未进攻结界坐标重复移除
                            try:
                                _filed_locs.remove(Filed_Locs[index])
                            except Exception as e:
                                print(f'[Error] : ' + e.__str__())
                                # pass
                    _sc.release()
                    # 判断是否全为已突破和突破失败结界
                    if len(_filed_locs) == 0:
                        _sc.capture(hwnd)
                        _flash_loc = template_match(_sc.get_image(), read_pic(RESOURCE_PATH + 'Filed_Flash.png'))
                        _sc.release()
                        if _flash_loc is not None:
                            click_matched(hwnd, _flash_loc[0], _flash_loc[1], log_text, tInt)
                        continue
                    # 未突破结界数为9，且还未进行结界降级
                    elif len(_filed_locs) == 9 and _down_grade[hwnd][1] == False:
                        _down_grade[hwnd][0] = 4
                        _down_grade[hwnd][1] = True
                    elif len(_filed_locs) == 8 and _down_grade[hwnd][1] == True:
                        _down_grade[hwnd][1] = False
                    # 有未突破结界，点击剩余结界的第一个
                    click_matched(hwnd, _filed_locs[0][0], _filed_locs[0][1], log_text, tInt)
                # 其余图标匹配到则直接点击
                else:
                    click_matched(hwnd, _matched_loc[0], _matched_loc[1], log_text, tInt)
                    break

    enable_widget()


def on_closing():
    main.destroy()
    # sys.exit()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    entry_count = btn_start = btn_stop = btn_clear = btn_resize = log_text = combobox_mission = None
    thread_mission = None
    TEMP_LIST = LOOP_FLAG = None

    main = Tk()
    tInt = IntVar()

    set_ui()

    main.mainloop()
