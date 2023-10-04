import ctypes
import logging
import threading
from datetime import *
from tkinter import *
from tkinter.ttk import Combobox

from screen_capture import *
from window_control import *
from config import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('AutoYinyangshi.log', encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def set_ui():
    global entry_count, btn_start, btn_stop, btn_clear, btn_resize, log_text, combobox_mission

    main.protocol("WM_DELETE_WINDOW", on_closing)
    main.geometry('367x260+760+640')
    main.attributes('-topmost', True)
    # main.resizable(False, False)

    tInt.set(DEFAULT_COUNT)

    log_text = Text(main, width=30, spacing2=10, height=10)
    log_text.place(x=0, y=2, width=198, height=250)
    label_count = Label(main, text="Times:")
    label_count.place(x=200, y=0, width=50)
    entry_count = Entry(main, textvariable=tInt)
    entry_count.place(x=265, y=0, width=100)
    label_option = Label(main, text="Option: ")
    label_option.place(x=200, y=25, width=65)
    combobox_mission = Combobox(main, values=["御魂", "斗技", "结界"], state="readonly")
    combobox_mission.place(x=265, y=25, width=100)
    combobox_mission.set("御魂")
    btn_start = Button(main, width=5, command=start_mission, text='Start')
    btn_start.place(x=200, y=52, width=82)
    btn_stop = Button(main, width=5, command=lambda: tInt.set(0), text='Stop', state="disable")
    btn_stop.place(x=283, y=52, width=82)
    btn_clear = Button(main, width=5, command=lambda: log_text.delete('0.0', END), text='Clear')
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
    if select_mission == "御魂":
        TEMP_LIST = YuHun
        LOOP_FLAG = TEMP_LIST[1]
        threading.Thread(target=orochi).start()
    elif select_mission == "斗技":
        TEMP_LIST = DouJi
        LOOP_FLAG = TEMP_LIST[1]
        threading.Thread(target=orochi).start()
    elif select_mission == "结界":

        threading.Thread(target=field).start()


def enable_widget():
    entry_count['state'] = NORMAL
    btn_start['state'] = NORMAL
    btn_start['text'] = 'Start'
    btn_stop['state'] = DISABLED
    combobox_mission['state'] = NORMAL


def diable_widget():
    entry_count['state'] = DISABLED
    btn_start['state'] = DISABLED
    btn_start['text'] = 'Running'
    btn_stop['state'] = NORMAL
    combobox_mission['state'] = DISABLED


def orochi():
    if tInt.get() <= 0:
        tInt.set(DEFAULT_COUNT)
    logger.info("========开始匹配========")
    diable_widget()

    hwnd_list = []
    win32gui.EnumWindows(EnumWindowsProc, hwnd_list)
    _last_matched = False

    while tInt.get() > 0:
        for _hwnd in hwnd_list:
            show_window(_hwnd)
            with ScreenCapture() as _sc:
                # _sc.capture(_hwnd, filepath='resource/sc.png')
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
        # print(f"{x},{y} = ", end="")
        return get_i(_rate_x) + get_i(_rate_y) * 3

    if tInt.get() <= 0:
        tInt.set(DEFAULT_COUNT)
    print("---------结界突破---------")
    diable_widget()

    hwnd_list = []
    win32gui.EnumWindows(EnumWindowsProc, hwnd_list)
    for hwnd in hwnd_list:
        while True:
            with ScreenCapture() as _sc:
                show_window(hwnd)
                _sc.capture(hwnd)
                loc = template_match(_sc.get_image(), read_pic(RESOURCE_PATH + 'Scene_Filed.png'))
                if loc is not None:
                    # 浅拷贝，使用深拷贝会导致原始列表被删除
                    reloc = Filed_Loc[:]
                    _sc.capture(hwnd)
                    locs = template_match(_sc.get_image(), read_pic(RESOURCE_PATH + 'Filed_Finished.png'))
                    # 判断是否有已突破结界
                    if locs is not None:
                        if len(locs) == 9:
                            print("结界已突破完毕！")
                            return
                        # 有已突破的结界则除去对应坐标
                        for loc in locs:
                            index = get_index(loc[0], loc[1])
                            print("filed_loc : ", Filed_Loc[index])
                            reloc.remove(Filed_Loc[index])

                    loc = reloc[0]
                    print("loc = ", loc)
                    show_window(hwnd)
                    print("未突破结界位置：", loc[0], loc[1])
                    post_click(hwnd, loc[0], loc[1])
                    time.sleep(0.5)
                    _sc.capture(hwnd)
                    # cv2.imshow("screen shot", _sc.get_image())
                    # cv2.waitKey(0)
                    loc1 = template_match(_sc.get_image(), read_pic(RESOURCE_PATH + 'Filed_Attack.png'))
                    if loc1 is not None:
                        print("进攻结界位置：", loc1[0], loc1[1])
                        post_click(hwnd, loc1[0], loc1[1])
                        time.sleep(0.5)
                    else:
                        print("未匹配到进攻结界按钮")
                else:
                    print("不在结界突破界面")
                    continue


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
