import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from tkinter import messagebox


class Timer_Frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.state = 'rest'
        self.running = False

        self.time_remain = datetime.now() - datetime.now()
        self.time_alarm = datetime.now() - datetime.now()
        self.time_start = datetime.now() - datetime.now()

        hour_choice = []
        min_choice = []
        sec_choice = []
        for hour in range(0, 24):
            if hour < 10:
                hour = f"{hour:02d}"
                hour_choice.append(hour)
            else:
                hour_choice.append(hour)
        for minute in range(0, 60, 5):
            if minute < 10:
                minute = f"{minute:02d}"
                min_choice.append(minute)
            else:
                min_choice.append(minute)
        for second in range(0, 60, 5):
            if second < 10:
                second = f"{second:02d}"
                sec_choice.append(second)
            else:
                sec_choice.append(second)

        self.hour_shown = tk.StringVar(self)
        self.min_shown = tk.StringVar(self)
        self.sec_shown = tk.StringVar(self)
        self.hour_shown.set('00')
        self.min_shown.set('00')
        self.sec_shown.set('00')

        input_limit_23 = self.register(self.ok_input_23)
        input_limit_59 = self.register(self.ok_input_59)

        self.hour_menu = ttk.Combobox(self, textvariable=self.hour_shown, values=hour_choice,
                                      width=3, height=5, state="normal",
                                      validate='all', validatecommand=(input_limit_23, '%P', '%S'))
        self.min_menu = ttk.Combobox(self, textvariable=self.min_shown, values=min_choice,
                                     width=3, height=5, state='normal',
                                     validate='all', validatecommand=(input_limit_59, '%P', '%S'))
        self.sec_menu = ttk.Combobox(self, textvariable=self.sec_shown, values=sec_choice,
                                     width=3, height=5, state='normal',
                                     validate='all', validatecommand=(input_limit_59, '%P', '%S'))
        hour_min_sec_label = tk.Label(self, text='hours                  minutes                  seconds',
                                      font=self.controller.FONT_S)

        self.start_pause_resume_button = tk.Button(self, text='Start',
                                                   font=self.controller.FONT_M,
                                                   fg='green',
                                                   command=self.start_pause_resume)
        self.cancel_button = tk.Button(self, text='Cancel',
                                       font=self.controller.FONT_M,
                                       state='disable',
                                       command=self.cancel)
        self.count_down_frame = tk.Frame(self, bg='grey')

        hour_min_sec_label.place(x=20, y=5)
        self.hour_menu.place(x=10, y=25)
        self.min_menu.place(x=100, y=25)
        self.sec_menu.place(x=190, y=25)
        self.start_pause_resume_button.place(x=190, y=50)
        self.cancel_button.place(x=10, y=50)
        self.count_down_frame.place(x=0, y=80, width=270, height=(330 - 80), anchor='nw')

    @staticmethod
    def ok_input_23(after, what):
        if not what.isdigit():
            return False
        elif len(after) > 2:
            return False
        elif len(after) == 0:
            return True
        elif int(after) > 23:
            return False
        else:
            return True

    @staticmethod
    def ok_input_59(after, what):
        if not what.isdigit():
            return False
        elif len(after) > 2:
            return False
        elif len(after) == 0:
            return True
        elif int(after) > 59:
            return False
        else:
            return True

    @staticmethod
    def zero_entry(entry):
        try:
            entry = int(entry)
            return entry
        except ValueError:
            entry = 0
            return entry

    def updating(self):
        self.start_button_disable()
        if self.running:
            if self.state == 'running':
                now = datetime.now()
                alarm = self.time_alarm
                alarm_text = alarm.strftime('%H:%M:%S.%f')
                alarm_text = alarm_text[:-6]
                now_text = now.strftime('%H:%M:%S.%f')
                now_text = now_text[:-6]
                self.time_remain = alarm - now
                self.countdown_label.config(text=self.time_remain)
                if alarm_text == now_text:
                    self.alarming()
                    self.cancel()

            else:
                # Paused
                self.time_alarm = datetime.now() + self.time_remain
                alarm_time = self.time_alarm
                alarm_text = alarm_time.strftime('%H:%M')
                self.alarm_label.config(text=alarm_text)

    def alarming(self):
        # More methods could be added as the alarm is working, ex. some video player.
        self.alarming_window = tk.Toplevel(self)
        self.alarming_window.title("It's Time!!!")
        self.alarming_window.resizable(False, False)
        self.alarming_window.geometry('300x300+400+300')

        close_button = tk.Button(self.alarming_window, text="close",
                                 font=("times", 15, "bold"), state='normal',
                                 fg="black", command=self.close)
        close_button.pack(side='top')

    def start_button_disable(self):
        hour = self.zero_entry(self.hour_shown.get())
        minute = self.zero_entry(self.min_shown.get())
        second = self.zero_entry(self.sec_shown.get())
        if int(hour) == 0 and int(minute) == 0 and int(second) == 0:
            self.start_pause_resume_button.config(state='disable')
        else:
            self.start_pause_resume_button.config(state='normal')

    def close(self):
        self.alarming_window.destroy()

    def start_pause_resume(self):
        if self.state == 'rest':
            # to Start
            hours = self.hour_shown.get()
            minute = self.min_shown.get()
            seconds = self.sec_shown.get()
            self.state = 'running'
            time_delta = timedelta(hours=int(hours), minutes=int(minute), seconds=int(seconds))
            self.time_remain = time_delta
            self.countdown_label = tk.Label(self.count_down_frame, font=self.controller.FONT_L)
            self.alarm_label = tk.Label(self.count_down_frame, font=self.controller.FONT_M)
            self.countdown_label.pack(side='top')
            self.alarm_label.pack(side='top')
            self.time_alarm = datetime.now() + self.time_remain
            alarm_time = self.time_alarm
            alarm_text = alarm_time.strftime('%H:%M')
            self.alarm_label.config(text=alarm_text)
            self.start_pause_resume_button.config(text='Pause', fg='orange')
            self.cancel_button.config(state='normal')
            self.hour_menu.config(state='disable')
            self.min_menu.config(state='disable')
            self.sec_menu.config(state='disable')
            self.running = True
        elif self.state == 'running':
            # to Pause
            self.start_pause_resume_button.config(text='Resume', fg='green')
            self.state = 'paused'
        else:
            # to Resume
            self.start_pause_resume_button.config(text='Pause', fg='orange')
            self.state = 'running'

    def cancel(self):
        # to Reset
        self.running = False
        self.state = 'rest'
        self.cancel_button.config(state='disable')
        self.start_pause_resume_button.config(text='Start', fg='green')
        self.time_remain = datetime.now() - datetime.now()
        self.time_alarm = datetime.now() - datetime.now()
        self.time_start = datetime.now() - datetime.now()
        self.hour_menu.config(state='normal')
        self.min_menu.config(state='normal')
        self.sec_menu.config(state='normal')
        for widgets in self.count_down_frame.winfo_children():
            widgets.destroy()
