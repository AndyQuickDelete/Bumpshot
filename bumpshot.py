import mss
import pystray
from pystray import Menu, MenuItem
from PIL import Image, ImageGrab
from datetime import datetime

import platform

if platform.system() == 'Windows':
    import pygetwindow as gw

if platform.system() == 'Darwin':
    import pywinctl as gw

import keyboard
import pyautogui
import os, sys, time

if platform.system() == 'Windows':
    from selenium.webdriver.common.by import By
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options
    from selenium.common.exceptions import WebDriverException

if platform.system() == 'Windows':
    import configparser
    Config = configparser.ConfigParser()
    Config.read(os.getcwd() + "\\myconfig.ini")

if platform.system() == 'Darwin':
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

if platform.system() == 'Windows':
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
else:
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads')

if platform.system() == 'Windows':
    driverb = os.getcwd() + '\\geckodriver.exe'

def exit_action(icon):
    icon.stop()
    os._exit(1)

def capture_screenshot():
    with mss.mss() as sct:
        fmt = '%Y-%m-%d_%H.%M.%S'
        now = datetime.now()
        current_time = now.strftime(fmt)

        if platform.system() == 'Windows':
            active_window = gw.getActiveWindow()
            if active_window == None or active_window == False:
                sct_img = sct.grab(monitor[1])
            else:
                monitor = {
                    "top": active_window.top,
                    "left": active_window.left + 7,
                    "width": active_window.width - 14,
                    "height": active_window.height - 7
                    }
                sct_img = sct.grab(monitor)

        if platform.system() == 'Darwin':
            monitor_1 = sct.monitors[1]
            active_window = gw.getActiveWindow()
            if active_window == None or active_window == False:
                sct_img = sct.grab(monitor_1)
            else:
                monitor = {
                    "top": active_window.top,
                    "left": active_window.left,
                    "width": active_window.width,
                    "height": active_window.height
                    }
                sct_img = sct.grab(monitor)

        if platform.system() == 'Darwin':
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(desktop + "/" + current_time + "-screenshot.png", "PNG")

        if platform.system() == 'Windows':
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(desktop + "\\" + current_time + "-screenshot.png", "PNG")

        time.sleep(2)

def capture_area_screenshot():
    left_x, left_y = pyautogui.position()
    while True:

        if keyboard.is_pressed("esc"):
            break
        
        if platform.system() == 'Windows':
            screenarea2 = Config.get('DEFAULT', 'ScreenArea2')
            if keyboard.is_pressed(str(screenarea2)):
                right_x, right_y = pyautogui.position()

                fmt = '%Y-%m-%d_%H.%M.%S'
                now = datetime.now()
                current_time = now.strftime(fmt)

                img_path = desktop + "\\" + current_time + "-screenshot.png"
                img = ImageGrab.grab(bbox=(left_x, left_y, right_x, right_y))
                img.save(img_path, "PNG")
                
                time.sleep(2)
                break
            
            if keyboard.is_pressed('u'):
                right_x, right_y = pyautogui.position()
                
                fmt = '%Y%m%dT%H%M%S'
                now = datetime.now()
                current_time = now.strftime(fmt)

                img_path = desktop + "\\" + current_time + "-screenshot.png"
                img = ImageGrab.grab(bbox=(left_x, left_y, right_x, right_y))
                img.save(img_path, "PNG")

                options = Options()
                options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

                serv = Service(driverb)
                
                browser = webdriver.Firefox(service=serv, options=options)
                try:
                    browser.get("https://images.suck-o.com/public_uploads")
                    browser.find_element(By.XPATH, "//input[@type='file']").send_keys(img_path)
                    browser.find_element(By.XPATH, "//input[@type='submit']").click()
                    return False
                except WebDriverException:
                    return True

        if platform.system() == 'Darwin':
            if keyboard.is_pressed('c'):
                right_x, right_y = pyautogui.position()

                fmt = '%Y-%m-%d_%H.%M.%S'
                now = datetime.now()
                current_time = now.strftime(fmt)

                img_path = desktop + "/" + current_time + "-screenshot.png"
                img = ImageGrab.grab(bbox=(left_x, left_y, right_x, right_y))
                img.save(img_path, "PNG")
                
                time.sleep(2)
                break
        
        
if __name__ == '__main__':
    if platform.system() == 'Windows':
        screenshot = Config.get('DEFAULT', 'Screenshot')
        screenarea1 = Config.get('DEFAULT', 'ScreenArea1')

        keyboard.add_hotkey(str(screenshot), capture_screenshot)
        keyboard.add_hotkey(str(screenarea1), capture_area_screenshot)

    
    if platform.system() == 'Darwin':
        keyboard.add_hotkey("alt+p", capture_screenshot)
        keyboard.add_hotkey("alt+1", capture_area_screenshot)        
    
    if platform.system() == 'Windows':
        image = Image.open("icon.ico")
    if platform.system() == 'Darwin':
        image = Image.open(resource_path("icon.icns"))

    icon = pystray.Icon('Bumpshot')
    icon.menu = Menu(
        MenuItem('Close Bumpshot', lambda : exit_action(icon)),
    )
    icon.icon = image
    icon.title = 'Bumpshot 1.0.4'
    icon.run()
