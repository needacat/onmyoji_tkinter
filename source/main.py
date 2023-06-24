import ctypes
import logging
import threading
from datetime import *
from tkinter import *

from screen_capture import *
from window_control import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('AutoYinyangshi.log', encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def orochi():
    if tInt.get() <= 0:
        tInt.set(DEFAULT_COUNT)
    logger.info("========开始匹配========")
    btn['state'] = DISABLED
    btn['text'] = 'Running'
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
                        return
                    _match_result = template_matching(_img, _temp)
                    if _match_result:
                        if _temp_name == LOOP_FLAG and _last_matched != LOOP_FLAG:
                            tInt.set(tInt.get() - 1)
                        _last_matched = _temp_name
                        _match_x, _match_y, _max_val = _match_result
                        print(f'[M] | {_temp_name[:-4]}')
                        print(f'[R] | {_max_val:.2f}')
                        print(f'[L] | ({_match_x},{_match_y})')
                        log.insert('end',
                                   datetime.now().strftime('%H:%M:%S') + f' | {tInt.get()} | [L] | {_temp_name[:-4]}\n')
                        click_matched(_hwnd, _match_x, _match_y, log, tInt)
                        break
            time.sleep(M_INTERVAL)

    btn['command'] = lambda: threading.Thread(target=orochi).start()
    btn['state'] = NORMAL
    btn['text'] = 'Start'


def on_closing():
    main.destroy()
    # sys.exit()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    main = Tk()
    main.protocol("WM_DELETE_WINDOW", on_closing)
    main.geometry('400x300+700+400')
    main.attributes('-topmost', True)
    main.resizable(False, False)

    tInt = IntVar()
    tInt.set(DEFAULT_COUNT)
    entry = Entry(main, textvariable=tInt)
    entry.grid(row=0, column=0, sticky=W + E)

    btn = Button(main, width=5, command=lambda: threading.Thread(target=orochi).start(), text='Start')
    btn.grid(row=0, column=1, sticky=N)

    btn_reset = Button(main, width=5, command=lambda: tInt.set(0), text='Stop')
    btn_reset.grid(row=0, column=2, sticky=N)

    btn_clear = Button(main, width=5, command=lambda: log.delete('0.0', END), text='Clear')
    btn_clear.grid(row=1, column=1, padx=2, sticky=N)

    btn_resize = Button(main, width=5, command=lambda: resize_all(), text='Resize')
    btn_resize.grid(row=1, column=2, padx=2, sticky=N)

    btn_resize = Button(main, width=10, command=open_games, text='OpenGames')
    btn_resize.grid(row=2, column=1, columnspan=2, padx=0, sticky=N)

    btn_resize = Button(main, width=10, command=close_games, text='CloseGames')
    btn_resize.grid(row=3, column=1, columnspan=2, padx=2, sticky=N)

    log = Text(main, width=30, spacing2=10, height=10)
    log.grid(row=1, column=0, rowspan=3)

    main.mainloop()
