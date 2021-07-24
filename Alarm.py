import tkinter as tk
import pytz
from datetime import datetime
from tkinter import messagebox


class Alarm(tk.Frame):
    def __init__(self, controller, alarm_time, repeat_mode, position):
        tk.Frame.__init__(self, controller)

        self.alarm_time = alarm_time
        self.repeat_mode = repeat_mode
        self.position = position
        self.controller = controller

        self.ONorOFF = 'ON'
        self.activated = False
        self.snoozed_time = self.snooze_time_text()
        self.snoozed = False

        self.alarm_time_label = tk.Label(self, text=alarm_time, font=("times", 33, "bold"))
        nota = tk.Label(self, text="Hours   Minutes", font=("times", 10, "bold"))
        self.switchButton = tk.Button(self, text="ON", font=("times", 20, "bold"), state='normal',
                                      fg="lime", command=self.switch)
        self.repeat_nota = tk.Label(self, text="Repeat", font=("times", 8, "bold"))
        self.repeat_label = tk.Label(self, text=self.repeat_mode_text(), font=("times", 10, "bold"))
        self.delete_button = tk.Button(self, text='x', font=("times", 20, "bold"), fg='red',
                                       command=self.deleting)
        self.alarm_number = tk.Label(self, text="Alarm #" + str(position), font=("times", 12))

        self.alarm_time_label.place(x=30, y=40)
        nota.place(x=30, y=80)
        self.switchButton.place(x=190, y=50)
        self.repeat_nota.place(x=30, y=2)
        self.repeat_label.place(x=30, y=22)
        self.delete_button.place(x=0, y=0)
        self.alarm_number.place(x=200, y=10)

    def repeat_mode_text(self):
        if self.repeat_mode == ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
            text = 'Weekdays'
        elif self.repeat_mode == ['Sun', 'Sat']:
            text = 'Weekends'
        elif self.repeat_mode == ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
            text = 'Everyday'
        else:
            text = self.repeat_mode
        return text

    def snooze_time_text(self):
        alarm_time = self.alarm_time
        alarm_hour = alarm_time[:2]
        alarm_minute = alarm_time[-2:]
        new_min = int(alarm_minute) + 9
        if new_min >= 60:
            new_min = int(new_min) - 60
            new_hour = int(alarm_hour) + 1
            if new_hour >= 24:
                new_hour = int(new_hour) - 24
        else:
            new_hour = alarm_hour
        text = f'{new_hour}:{new_min}'
        return text

    def switch(self):
        if self.ONorOFF == "OFF":
            self.ONorOFF = "ON"
            self.switchButton.config(text="ON", fg="lime", padx=5)
        else:
            self.ONorOFF = "OFF"
            self.switchButton.config(text="OFF", fg="red", padx=0)

    def updating(self):
        if self.ONorOFF == 'ON' and not self.activated:
            if not self.snoozed:
                self.check_alarm(self.alarm_time)
            else:
                self.check_alarm(self.snoozed_time)

    def check_alarm(self, checked_time):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
        current_time = current_time[:-5]
        current_day = now.strftime("%a")
        alarm_time = f"{checked_time}:00.0"
        if alarm_time == current_time and current_day in self.repeat_mode:
            self.activated = True
            self.alarming()
        elif self.repeat_mode == ['Never'] and alarm_time == current_time:
            self.alarming()
            self.activated = True

    def alarming(self):
        # More methods could be added as the alarm is working, ex. some video player.
        title_text = f'Alarm #{self.position} is Ringing'
        self.alarming_window = tk.Toplevel(self)
        self.alarming_window.title(title_text)
        self.alarming_window.resizable(False, False)
        self.alarming_window.geometry('301x300+400+300')
        self.alarming_window.protocol("WM_DELETE_WINDOW", self.cancel)

        cancel_button = tk.Button(self.alarming_window, text="Cancel",
                                  font=("times", 10, "bold"), state='normal',
                                  fg="black", command=self.cancel)
        cancel_button.pack(side='top')
        snooze_button = tk.Button(self.alarming_window, text="Snooze",
                                  font=("times", 50, "bold"),
                                  state='normal',
                                  fg="black", command=self.snooze)
        snooze_button.pack(side='top')
        if self.snoozed:
            snooze_button['state'] = 'disable'
            self.snoozed_label.destroy()
            second_ring_label = tk.Label(self.alarming_window, text='Second Ring!',
                                         font=("times", 50, "bold"),
                                         fg='red')
            second_ring_label.pack(side='bottom')

    def cancel(self):
        if self.repeat_mode == ['Never']:
            self.switch()
        self.activated = False
        self.snoozed = False
        self.alarming_window.destroy()

    def snooze(self):
        self.snoozed = True
        self.activated = False
        self.alarming_window.destroy()
        self.snoozed_label = tk.Label(self, text='+9 min', font=("times", 12, 'bold'), fg='red')
        self.snoozed_label.place(x=130, y=40)

    def reposition(self, new_position):
        self.position = new_position
        self.alarm_number = tk.Label(self, text="Alarm #" + str(self.position), font=("times", 12))
        self.alarm_number.place(x=200, y=10)

    def deleting(self):
        response = messagebox.askyesno('Deleting', f'Do You want to Delete Alarm #{self.position}?')
        if response:
            for widgets in self.winfo_children():
                widgets.destroy()
            self.controller.deleted(self.position)
