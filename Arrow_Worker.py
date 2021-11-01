import pyautogui
from PIL import Image, ImageGrab
import keyboard
import os
import threading

class Arrow_Worker():
    def __init__(self, posX:int, posY:int, key:str, color:str):
        self.arrowSignal = None
        self.arrowStatus = None
        self.arrowThread = None

        self.running = False

        self.posX = posX
        self.posY = posY
        self.color = color
        self.key = key
    
    def Start(self, Screen):
        self.running = True
        arrowThread = threading.Thread(target=self.FindArrow, args=(Screen,))
        arrowThread.start()

    def FindArrow(self, Screen):
        pixel = Screen.getpixel((self.posX, self.posY))
        if str(pixel) == self.color:
            print("Found arrow")
            if os.name == 'nt':
                keyboard.press_and_release(self.key)
            else:
                pyautogui.press(self.key)