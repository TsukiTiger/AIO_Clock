import datetime
import pytz
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Alarm import Alarm


class Alarm_Frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.running = True

        self.alarm_amount = 0
        self.repeat_options = ['Never', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.repeat_mode_temp = ['Never']

        self.editing_window = tk.Toplevel(self)
        self.editing_window.destroy()

        self.adding_button = tk.Button(self,
                                       text='+',
                                       font=controller.FONT_L,
                                       command=self.adding_alarm)
        self.adding_button.place(x=270, y=0, anchor="ne", height=30, width=31)

        alarm_label = tk.Label(self,
                               text='Alarm',
                               font=controller.FONT_M)
        alarm_label.place(x=0, y=0, anchor="nw", height=30, width=150)

        self.alarm = {1: 'none', 2: 'none', 3: 'none'}
        self.alarm_time = {1: 'none', 2: 'none', 3: 'none'}

    def editing_alarm(self, alarm_number, current_hour, current_minute):
        self.disable_button()
        self.editing_window = tk.Toplevel(self)
        self.editing_window.resizable(False, False)
        self.editing_window.geometry('400x100+280+0')
        self.editing_window.title(f'Choose a New City for Clock #{alarm_number}')
        self.editing_window.protocol("WM_DELETE_WINDOW", self.closing_editing_window)

        input_limit_23 = self.editing_window.register(self.ok_input_23)
        input_limit_59 = self.editing_window.register(self.ok_input_59)

        hour_choice = []
        min_choice = []
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

        self.hour_shown = tk.StringVar(self.editing_window)
        self.min_shown = tk.StringVar(self.editing_window)
        self.repeat_shown = tk.StringVar(self.editing_window)
        self.hour_shown.set(current_hour)
        self.min_shown.set(current_minute)

        hour_min_repeat_label = tk.Label(self.editing_window, text="Hours         Minutes      Repeat",
                                         font=("times", 10, "bold"))
        hour_menu = ttk.Combobox(self.editing_window, textvariable=self.hour_shown, values=hour_choice,
                                 width=3, height=5, state="normal",
                                 validate='all', validatecommand=(input_limit_23, '%P', '%S'))
        min_menu = ttk.Combobox(self.editing_window, textvariable=self.min_shown, values=min_choice,
                                width=3, height=5, state='normal',
                                validate='all', validatecommand=(input_limit_59, '%P', '%S'))
        self.repeat_menu_button = tk.Menubutton(self.editing_window, text='Never', indicatoron=True,
                                                relief="raised")
        self.repeat_menu = tk.Menu(self.repeat_menu_button, tearoff=False)
        self.choices = {}
        for choice in self.repeat_options:
            self.choices[choice] = tk.IntVar(value=0)
            self.repeat_menu.add_checkbutton(label=choice, variable=self.choices[choice],
                                             onvalue=1, offvalue=0, command=self.printValues)
        self.repeat_menu_button.config(menu=self.repeat_menu)
        confirm_button = tk.Button(self.editing_window, text="Confirm", font=("times", 20, "bold"),
                                   command=lambda i=alarm_number:
                                   self.change(i))
        self.editing_window.bind('<Return>', lambda event: self.change(alarm_number))

        hour_min_repeat_label.place(x=30, y=1)
        hour_menu.place(x=25, y=20)
        min_menu.place(x=85, y=20)
        self.repeat_menu_button.place(x=145, y=20)
        confirm_button.place(x=270, y=20)

    def printValues(self):
        if self.choices['Never'].get() == 1 and 'Never' not in self.repeat_mode_temp:
            for day, var in self.choices.items():
                if var.get() == 1 and not day == 'Never':
                    self.choices[day].set(0)
        else:
            self.choices['Never'].set(0)
        chosen_day = []
        for day, var in self.choices.items():
            if var.get() == 1:
                chosen_day.append(day)
        self.repeat_mode_temp = chosen_day
        self.repeat_menu_button.config(text=chosen_day)

    def adding_alarm(self):
        current_alarm_number = self.alarm_amount + 1
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_min = now.strftime("%M")
        self.editing_alarm(current_alarm_number, current_hour, current_min)

    def updating(self):
        if self.running:
            for i in range(1, self.alarm_amount + 1):
                self.alarm[i].updating()

    def closing_editing_window(self):
        response = messagebox.askyesno('Quiting', 'Do you want to leave without Choosing?')
        if response:
            self.editing_window.destroy()
            self.enable_button()

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

    def duplicated(self, calling_position, new_time):
        times = self.alarm_time
        times[calling_position] = 'none'
        if new_time in times.values():
            return True
        else:
            return False

    @staticmethod
    def zero_entry(entry):
        try:
            entry = int(entry)
            return entry
        except ValueError:
            entry = 0
            return entry

    def change(self, alarm_position):
        new_hour = self.zero_entry(self.hour_shown.get())
        new_min = self.zero_entry(self.min_shown.get())
        new_time = "{}:{}".format(new_hour, new_min)
        if self.duplicated(alarm_position, new_time):
            messagebox.showerror("ERROR", "Please do not have two alarm the same time.")
        else:
            if int(new_hour) < 10:
                new_hour = f"{int(new_hour):02d}"
            if int(new_min) < 10:
                new_min = f"{int(new_min):02d}"
            new_time = "{}:{}".format(new_hour, new_min)
            chosen_day = []
            for day, var in self.choices.items():
                if var.get() == 1:
                    chosen_day.append(day)
            if chosen_day == []:
                chosen_day = ['Never']
            self.alarm[alarm_position] = Alarm(self, new_time, chosen_day, alarm_position)
            self.alarm[alarm_position].place(x=0, y=30 + (100 * (alarm_position - 1)), anchor='nw',
                                             width=270, height=100)
            self.alarm_time[alarm_position] = new_time
            self.alarm_amount += 1
            self.enable_button()
            if self.alarm_amount == 3:
                self.adding_button['state'] = 'disable'
            self.editing_window.destroy()

    def deleted(self, position):
        self.running = False
        if self.alarm_amount > position:
            for i in range(position, self.alarm_amount):
                self.alarm[i] = self.alarm[i + 1]
                self.alarm[i].place(x=0, y=30 + (100 * (i - 1)), anchor='nw',
                                    width=270, height=100)
                self.alarm[i].reposition(i)
        self.alarm_time[self.alarm_amount] = 'none'
        self.alarm_amount -= 1
        self.adding_button['state'] = 'normal'
        self.running = True

    def disable_button(self):
        self.adding_button['state'] = 'disable'
        for i in range(1, self.alarm_amount + 1):
            self.alarm[i].delete_button['state'] = 'disable'

    def enable_button(self):
        self.adding_button['state'] = 'normal'
        for i in range(1, self.alarm_amount + 1):
            self.alarm[i].delete_button['state'] = 'normal'
