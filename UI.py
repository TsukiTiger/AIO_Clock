import tkinter as tk
from tkinter import messagebox
import time

from MainClock import MainClock
from Bar import Bar

from WorldClock_Frame import WorldClock_Frame
from Alarm_Frame import Alarm_Frame
from StopWatch_Frame import StopWatch_Frame
from Timer_Frame import Timer_Frame


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.is_running = True

        self.FONT_S = ("times", 10, "bold")
        self.FONT_M = ("times", 20, "bold")
        self.FONT_L = ("times", 30, "bold")
        self.FONT_XL = ("times", 50, "bold")

        self.title('AIO-Clock')
        self.geometry("270x400")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.safe_quit)

        clock_frame = tk.Frame(self)
        self.MainClock = MainClock(clock_frame, self)
        clock_frame.place(x=0, y=0, anchor="nw", height=20, width=270)

        main_frame = tk.Frame(self,
                              bg='red')
        main_frame.place(x=0, y=20, anchor="nw", height=330, width=270)

        bar_frame = tk.Frame(self)
        self.Bar = Bar(bar_frame, self)
        bar_frame.place(x=0, y=350, anchor="nw", height=50, width=270)

        self.frames = {}
        for page in (WorldClock_Frame, Alarm_Frame, StopWatch_Frame, Timer_Frame):
            page_name = page.__name__
            frame = page(main_frame, self)
            frame.place(x=0, y=0, anchor="nw", height=330, width=270)
            self.frames[page_name] = frame

        self.show_frame('WorldClock_Frame')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def run(self):
        while self.is_running:
            self.MainClock.updating()
            self.frames['WorldClock_Frame'].updating()
            self.frames['Alarm_Frame'].updating()
            self.frames['StopWatch_Frame'].updating()
            self.frames['Timer_Frame'].updating()
            self.update()
            self.update_idletasks()

    def safe_quit(self):
        self.is_running = False
        response = messagebox.askyesno('Quit', 'Do you want to quit this program?')
        if response:
            self.quit()
        else:
            self.is_running = True
