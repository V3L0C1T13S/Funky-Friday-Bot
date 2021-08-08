from PIL import Image, ImageGrab
import pyautogui
import keyboard
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
# Only needed for command line arguments
import traceback, sys

import threading

print(os.name)

size = pyautogui.size()
print(size)

x1 = size[0]/2+160; y1=size[1]/2-470
x2 = x1+596; y2 = y1+144

#Screen = ImageGrab.grab(bbox = (x1, y1, x2, y2))
#Screen.show()

class ArrowStatus(QLabel):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)
        self.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        #self.setParent = parent
        #self.show()
    def setStatus(self, status):
        time.sleep(0.5)
        self.setText(status)

class ThoughtOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 64)")
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setFixedSize(QSize(300, 500))
        self.move(47, 50)
        #self.show()

running = False
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    #progress = pyqtSignal(int)
    arrowSignal = pyqtSignal(str)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['arrow_callback'] = self.signals.arrowSignal

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

# start application up here so we can do stuff
if __name__== '__main__':
    app = QApplication([])
    thoughtswindow = ThoughtOverlay()
    #thoughtswindow.show()

# Subclass for main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.running = False
        self.setWindowTitle("FNF AI")

        self.ToggleAIButton = QPushButton("Start AI")
        #button.setCheckable(True)
        self.ToggleAIButton.clicked.connect(self.ai_start_clicked)

        self.Arrows = []
        #self.ThoughtsUI = ThoughtOverlay()
        list.insert(self.Arrows, 0, ArrowStatus("LEFT: FALSE"))
        list.insert(self.Arrows, 1, ArrowStatus("UP: FALSE"))
        list.insert(self.Arrows, 2, ArrowStatus("DOWN: FALSE"))
        list.insert(self.Arrows, 3, ArrowStatus("RIGHT: FALSE"))

        arrowoffset = 0
        for Arrow in self.Arrows:
            Arrow.setParent(thoughtswindow)
            arrowoffset += 20
            Arrow.move(-155,20 + arrowoffset)
            Arrow.show()
        self.setFixedSize(QSize(800, 600))
        # Set central widget
        self.setCentralWidget(self.ToggleAIButton)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        #self.ThoughtsUI.show()
    
    def result(self, s):
        print("yes")
    def finished(self):
        print("thread finished")
    def set_txt_threading2(self, label, s):
        label.setText(s)
    def set_txt_threading(self, seconds, label, txt):
        time.sleep(seconds)
        return label, txt
    def print_output(self, s):
        print("RECIEVED SIGNAL "+s)
        if s == "LEFT":
            self.Arrows[0].setText(s+": TRUE")
            worker = Worker(self.set_txt_threading, 0.01, self.Arrows[0], s+": FALSE")
            worker.signals.result.connect(self.set_txt_threading2)
        elif s == "UP":
            self.Arrows[1].setText(s+": TRUE")
            worker = Worker(self.set_txt_threading, 0.01, self.Arrows[1], s+": FALSE")
            worker.signals.result.connect(self.set_txt_threading2)
        elif s == "DOWN":
            self.Arrows[2].setText(s+": TRUE")
            worker = Worker(self.set_txt_threading, 0.01, self.Arrows[2], s+": FALSE")
            worker.signals.result.connect(self.set_txt_threading2)
        elif s == "RIGHT":
            self.Arrows[3].setText(s+": TRUE")
            worker = Worker(self.set_txt_threading, 0.01, self.Arrows[3], s+": FALSE")
            worker.signals.result.connect(self.set_txt_threading2)
    def FrameCapture(self, arrow_callback):
        print("called")
        def returnstuff(ser):
            return ser
        while self.running == True:
            #print("yes")
            #time.sleep(0.005)
            Screen = ImageGrab.grab(bbox = (x1, y1, x2, y2))

            ArrowLeftPix = Screen.getpixel((48, 75))
            ArrowUpPix = Screen.getpixel((392, 47))
            ArrowDownPix = Screen.getpixel((221, 47))
            ArrowRightPix = Screen.getpixel((550, 79))

            results = []
            #print("yes")
            #print(str(ArrowLeftPix))
            if str(ArrowLeftPix) == "(194, 75, 153)":
                print("left arrow detected")
                print("sleeping")
                #time.sleep(1)
                if os.name == "nt":
                    keyboard.press_and_release('a')
                else:
                    pyautogui.press('left')
                print("pushed left arrow key")
                arrow_callback.emit("LEFT")
            if str(ArrowUpPix) == "(18, 250, 5)":
                print("up arrow detected")
                print("sleeping")
                #time.sleep(1)
                if os.name == "nt":
                    keyboard.press_and_release('w')
                else:
                    pyautogui.press('up')
                print("pushed up arrow key")
                arrow_callback.emit("UP")
            if str(ArrowDownPix) == "(0, 255, 255)":
                print("down arrow detected")
                print("sleeping")
                #time.sleep(1)
                if os.name == "nt":
                    keyboard.press_and_release('s')
                else:
                    pyautogui.press('down')
                print("pushed down arrow key")
                arrow_callback.emit("DOWN")
            if str(ArrowRightPix) == "(249, 57, 63)":
                print("right arrow detected")
                print("sleeping")
                #time.sleep(1)
                if os.name == "nt":
                    keyboard.press_and_release('d')
                else:
                    pyautogui.press('right')
                print("pushed right arrow key")
                arrow_callback.emit("RIGHT")
            #progress_callback.emit(results)
            #returnstuff(results)
    def ai_start_clicked(self):
        print("Clicked!")
        self.running = not self.running
        print(self.running)
        if self.running == True:
            self.setWindowTitle("FNF AI - Running")
            self.ToggleAIButton.setText("Stop AI")
            thoughtswindow.show()
            worker = Worker(self.FrameCapture)
            worker.signals.result.connect(self.result)
            worker.signals.finished.connect(self.finished)
            worker.signals.arrowSignal.connect(self.print_output)
            # Start threadpool
            self.threadpool.start(worker)
        else:
            self.setWindowTitle("FNF AI - Stopped")
            self.ToggleAIButton.setText("Start AI")
            thoughtswindow.close()
    def add_component(UI, component):
        component.setParent(UI)
        component.show()
    
# Create a GUI for our user
if __name__== '__main__':
    window = MainWindow()
    window.show()
    app.exec()