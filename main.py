import ctypes
import logging
import threading
from tkinter import *

from screen_capture import *
from config import *
from window_control import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('AutoYinyangshi.log', encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def auto():
    if tInt.get() > 0:
        logger.info("========开始匹配========")
        btn['state'] = DISABLED
        btn['text'] = 'Running'

        hwnd_list = []
        win32gui.EnumWindows(EnumWindowsProc, hwnd_list)
    else:
        logger.warning('-----匹配次数为0！-----')
        return

    while tInt.get() > 0:
        for hwnd in hwnd_list:
            show_window(hwnd)
            with ScreenCapture() as sc:
                # sc.capture(hwnd, filepath='resource/sc.png')
                sc.capture(hwnd)
                for temp in TEMP_LIST:
                    print(f'match {temp}')
                    loc = template_matching(sc.get_image(), read_pic('./resource/' + temp))
                    if loc:
                        # logger.info(f'匹配成功，坐标为：{loc[0]}, {loc[1]}')
                        print(f'匹配成功，坐标为：{loc[0]}, {loc[1]}')
                        click_matched(hwnd, loc, log, tInt)
                        if temp == '1.png':
                            tInt.set(tInt.get() - 1)
                        break
            time.sleep(T_INTERVAL)

    btn['command'] = lambda: threading.Thread(target=auto).start()
    btn['state'] = NORMAL
    btn['text'] = 'Start'


def on_closing():
    main.destroy()
    # sys.exit()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    main = Tk()
    main.protocol("WM_DELETE_WINDOW", on_closing)
    main.geometry('350x300+700+400')
    main.attributes('-topmost', True)
    main.resizable(False, False)

    tInt = IntVar()
    tInt.set(DEFAULT_COUNT)
    entry = Entry(main, textvariable=tInt)
    entry.grid(row=0, column=0, sticky=W + E)

    btn = Button(main, width=5, command=lambda: threading.Thread(target=auto).start(), text='Start')
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

    log = Text(main, width=24, spacing2=10, height=10)
    log.grid(row=1, column=0, rowspan=3)

    main.mainloop()
