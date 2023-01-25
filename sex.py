import curses
import ctypes
import time

import numpy as np
import pyautogui
from PIL import Image
import win32gui
import win32ui
from screeninfo import get_monitors


class Apple:
    def __init__(self, stdscr: curses.window, win: tuple):
        self.stdscr = stdscr
        self.size = 7
        self.time = time.time()  # to know fps
        self.grad = np.array(list("       ..''``,,^<~+=:;!i|Il(1?[{tfjrxnuvczeomwqpdbkhXYUQ#MW&8B№@"))
        self.hwnd, self.saveBitMap, self.saveDC = win

    def get_image(self) -> None:
        self.time = time.time()
        ctypes.windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), 0x00000002)
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        im.show()


def window_size(hwnd: int) -> tuple[int, int]:
    dpi = ctypes.windll.user32.GetDpiForSystem()
    dpi = dpi / ctypes.windll.user32.GetDpiForWindow(hwnd)  # dpi affects on resolution
    rect = win32gui.GetWindowRect(hwnd)  # these values aren't exact
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    a = []
    monitors = get_monitors()
    for m in monitors:  # search for the nearest values
        a.append([abs(m.width - w + m.height - h)])
    indx = a.index(min(a))
    w = int(monitors[indx].width / dpi)
    h = int(monitors[indx].height / dpi)
    return w, h


def get_window(win_name: str) -> tuple[int, 'PyCBitmap', 'PyCDC']:
    hwnd = 0
    user32 = ctypes.windll.user32
    for title in pyautogui.getAllTitles():  # to get win by not exact title
        if win_name.lower() in title.lower():
            hwnd = win32gui.FindWindow(None, title)
            break
    else:
        print("Window not found")
        exit()

    w, h = window_size(hwnd)

    hwndDC = user32.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    return hwnd, saveBitMap, saveDC


def main():
    a = curses.wrapper(Apple, get_window("opera"))
    while True:
        a.get_image()


if __name__ == '__main__':
    main()
