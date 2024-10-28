import numpy as np
import win32con
import win32gui
import win32ui


class ScreenCapture:
    def __init__(self):
        self.hwnd = None
        self.rect = (0, 0, 0, 0)
        self.hwndDC = None
        self.mfcDC = None
        self.saveDC = None
        self.Bitmap = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def release(self):
        if self.mfcDC is not None:
            self.mfcDC.DeleteDC()
        if self.saveDC is not None:
            self.saveDC.DeleteDC()
        if self.hwndDC is not None and self.hwnd is not None:
            win32gui.ReleaseDC(self.hwnd, self.hwndDC)
        if self.Bitmap is not None and self.Bitmap.GetHandle() != 0:
            win32gui.DeleteObject(self.Bitmap.GetHandle())

    def capture(self, hwnd=None, rect=None, filepath=None):
        self.hwnd = hwnd or win32gui.GetDesktopWindow()
        self.rect = rect or win32gui.GetWindowRect(self.hwnd)
        w = self.rect[2] - self.rect[0]
        h = self.rect[3] - self.rect[1]
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        self.Bitmap = win32ui.CreateBitmap()
        self.Bitmap.CreateCompatibleBitmap(self.mfcDC, 820, 462)
        # self.Bitmap.CreateCompatibleBitmap(self.mfcDC, w, h)
        self.saveDC.SelectObject(self.Bitmap)
        # print(f'w={w},h={h}')

        #                   目标                              源
        self.saveDC.BitBlt((0, 0), (820, 462), self.mfcDC, (9, 35), win32con.SRCCOPY)
        # self.saveDC.BitBlt((0, 0), (w, h), self.mfcDC, (0, 0), win32con.SRCCOPY)

        if filepath is not None:
            self.Bitmap.SaveBitmapFile(self.saveDC, filepath)
        return self.get_image()

    def get_image(self) -> np.ndarray:
        bmp_info = self.Bitmap.GetInfo()
        bmp_data = self.Bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_data, dtype='uint8')
        img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
        return img
