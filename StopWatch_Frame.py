import tkinter as tk
import time
from datetime import datetime


class StopWatch_Frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.running = False

        self.time_start = datetime.now()
        self.time_ran = datetime.now()-datetime.now()
        self.time_dif = datetime.now()-datetime.now()
        self.time_lapped = datetime.now()-datetime.now()
        self.time_current_lap = datetime.now()-datetime.now()

        self.lap_amount = 1

        self.laps = {}

        self.state = 'rest'

        self.time_label = tk.Label(self,
                                   text='0:00:00.000000',
                                   font=controller.FONT_L)
        self.start_stop_button = tk.Button(self,
                                           text='Start',
                                           font=controller.FONT_L,
                                           fg='green',
                                           command=self.start_stop)
        self.lap_reset_button = tk.Button(self,
                                          text='lap',
                                          font=controller.FONT_L,
                                          state='disable',
                                          command=self.lap_reset)
        self.result_frame = tk.Frame(self, bg='grey')
        self.current_lap_label = tk.Label(self.result_frame)
        self.current_lap_label.destroy()
        self.result_box = tk.Listbox(self.result_frame)
        self.result_box.destroy()

        limit_label = tk.Label(self, text='Lap amount was limited to 20.', font=("times", 6, "bold"), fg='grey')
        limit_label.place(x=0, y=0)

        self.time_label.place(x=40, y=7)
        self.start_stop_button.place(x=190, y=50)
        self.lap_reset_button.place(x=10, y=50)
        self.result_frame.place(x=0, y=100, width=270, height=230, anchor='nw')

    def start_stop(self):
        if self.state == 'rest':
            self.state = 'run'
            self.current_lap_label = tk.Label(self.result_frame, font=self.controller.FONT_M)
            self.current_lap_label.pack(side='top')
            self.result_box = tk.Listbox(self.result_frame)
            self.result_box.pack(side='top')
            self.time_start = datetime.now()
            self.lap_reset_button.config(state='normal', text='lap', fg='black')
            self.start_stop_button.config(text='Stop', fg='red')
            self.running = True
        elif self.state == 'stopped':
            self.time_start = datetime.now()
            self.state = 'run'
            self.lap_reset_button.config(state='normal', text='lap', fg='black')
            self.start_stop_button.config(text='Stop', fg='red')
            self.running = True
        else:
            self.lap_reset_button.config(text='Reset', fg='blue')
            self.running = False
            self.start_stop_button.config(text='Start', fg='green')
            self.time_ran = self.time_dif
            self.state = 'stopped'

    def updating(self):
        if self.running:
            now = datetime.now()
            self.time_dif = now - self.time_start + self.time_ran
            self.time_current_lap = self.time_dif - self.time_lapped
            lap_text = f'lap {self.lap_amount}: {self.time_current_lap}'
            self.time_label.config(text=self.time_dif)
            self.current_lap_label.config(text=lap_text)

    def lap_reset(self):
        if self.state == 'stopped':
            # Reset
            self.time_start = datetime.now()
            self.time_ran = datetime.now() - datetime.now()
            self.time_dif = datetime.now() - datetime.now()
            self.time_lapped = datetime.now() - datetime.now()
            self.time_current_lap = datetime.now() - datetime.now()
            self.lap_amount = 1
            self.running = False
            self.time_label.config(text='0:00:00.000000')
            self.state = 'rest'
            self.lap_reset_button.config(text='lap', state='disable')
            self.start_stop_button.config(state='normal')
            self.laps = {}
            for widgets in self.result_frame.winfo_children():
                widgets.destroy()
        else:
            # lapping
            text = f'lap {self.lap_amount}: {self.time_current_lap}'
            self.laps[self.lap_amount] = self.time_current_lap
            self.result_box.insert(0, text)
            self.time_lapped += self.time_current_lap
            self.coloring()
            self.lap_amount += 1
            if self.lap_amount > 20:
                self.start_stop()
                self.start_stop_button.config(state='disable')
                self.current_lap_label.destroy()

    def coloring(self):
        for index in range(self.lap_amount):
            self.result_box.itemconfig(index, fg='black')
        if self.lap_amount > 2:
            key_max = self.key_max(self.laps)
            self.result_box.itemconfig(self.lap_amount-key_max, fg='red')
            key_min = self.key_min(self.laps)
            self.result_box.itemconfig(self.lap_amount-key_min, fg='green')

    @staticmethod
    def key_max(d):
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(max(v))]

    @staticmethod
    def key_min(d):
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(min(v))]