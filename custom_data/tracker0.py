import win32gui
import win32process
import psutil
import time
import threading
import json

from datetime import datetime
from pynput import mouse, keyboard


fdata = {}

MOUSE_MOVED = 0
MOUSE_CLICKED = 0
MOUSE_SCROLLED = 0
TEST = 0


# TODO: things i want to change to better improve the data tracking
#   1. change the time.sleep of app tracking smaller, or somehow able to get event of when the focus changes to dif. wind
#   2. including keyboard presses
#   3. add keyboard keys and mouse buttons
#   4. (optional) specific amount of mouse scrolls, click position, etc.


def application_tracking(lock_mouse_counters: threading.Lock):
    while threading.main_thread().is_alive():
        time.sleep(1)
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        proc_name = psutil.Process(pid[-1]).name()
        wind_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())

        if proc_name in fdata:
            pass
        else:
            fdata[proc_name] = {
                "MOUSE_MOVED": 0,
                "MOUSE_CLICKED": 0,
                "MOUSE_SCROLLED": 0,
            }
        if not lock_mouse_counters.locked():
            lock_mouse_counters.acquire()
            print("MOUSE: MOVED", MOUSE_MOVED, ", CLICKED", MOUSE_CLICKED, ", SCROLLED", MOUSE_SCROLLED)
            lock_mouse_counters.release()
    print("PROGRAM ENDED")


def mouse_tracking(lock_mouse_counters: threading.Lock):
    def on_move(x, y):
        lock_mouse_counters.acquire()
        global MOUSE_MOVED
        MOUSE_MOVED += 1
        lock_mouse_counters.release()

    def on_click(x, y, button, pressed):
        lock_mouse_counters.acquire()
        global MOUSE_CLICKED
        MOUSE_CLICKED += 1
        lock_mouse_counters.release()

    def on_scroll(x, y, dx, dy):
        lock_mouse_counters.acquire()
        global MOUSE_SCROLLED
        MOUSE_SCROLLED += 1
        lock_mouse_counters.release()

    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()


def keyboard_tracking():
    def on_press(key):
        print("PRESSED", key)

    def on_release(key):
        print("RELEASED", key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


lock_mouse_counters = threading.Lock()
app_thread = threading.Thread(target=application_tracking, args=(lock_mouse_counters,), daemon=False)
mouse_thread = threading.Thread(target=mouse_tracking, args=(lock_mouse_counters,), daemon=False)
keyboard_thread = threading.Thread(target=keyboard_tracking, daemon=False)
app_thread.start()
mouse_thread.start()
keyboard_thread.start()

while True:
    time.sleep(100000)  # appears the program, the main thread, is still active until it is forcefully exited


