import datetime
import pytz
import tkinter as tk
from tkinter import messagebox
from WorldClock import WorldClock


class WorldClock_Frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.running = True

        self.data = {'Africa': ['Tunis', 'Accra', "Cairo", "Lusaka"],
                     'America': ['Chicago', 'Los_Angeles', 'Denver', 'Detroit', 'New_York', 'Mexico_City'],
                     'Asia': ['Bangkok', 'Chongqing', 'Dubai', 'Hong_Kong', 'Shanghai', 'Tokyo'],
                     'Australia': ['Brisbane', 'Canberra', 'Darwin', 'Melbourne', 'Sydney'],
                     'Europe': ['Berlin', 'Budapest', 'Copenhagen', 'Dublin', 'Lisbon', 'London', 'Moscow', 'Paris',
                                'Rome', 'Vienna'],
                     'Pacific': ['Auckland', 'Easter', 'Fiji', 'Honolulu', 'Midway', 'Palau', 'Saipan']}

        self.continentList = tk.StringVar(self)
        self.cityList = tk.StringVar(self)

        self.clock_amount = 0
        self.editing_window = tk.Toplevel(self)
        self.editing_window.destroy()

        self.adding_button = tk.Button(self,
                                       text='+',
                                       font=controller.FONT_L,
                                       command=self.adding_clock)
        self.adding_button.place(x=270, y=0, anchor="ne", height=30, width=31)

        world_clock_label = tk.Label(self,
                                     text='World Clock',
                                     font=controller.FONT_M)
        world_clock_label.place(x=0, y=0, anchor="nw", height=30, width=150)

        self.clock = {1: 'none', 2: 'none', 3: 'none'}

    def editing_clock(self, clock_number, continent, city):
        self.disable_button()
        self.editing_window = tk.Toplevel(self)
        self.editing_window.resizable(False, False)
        self.editing_window.geometry('400x100+280+0')
        self.editing_window.title(f'Choose a New City for Clock #{clock_number}')
        self.editing_window.protocol("WM_DELETE_WINDOW", self.closing_editing_window)

        self.continentList.set(continent)
        self.cityList.set(city)

        self.continentMenu = tk.OptionMenu(self.editing_window, self.continentList, *self.data.keys())
        self.cityMenu = tk.OptionMenu(self.editing_window, self.cityList, '')
        self.attention = tk.Label(self.editing_window, text='Please click "Confirm" Button to exit.',
                                  font=("times", 10, "bold"), fg="Red")

        self.continentList.trace('w', self.update_option)

        self.continentMenu.place(x=10, y=20)
        self.cityMenu.place(x=110, y=20)
        self.attention.place(x=100, y=1)

        confirm_button = tk.Button(self.editing_window, text="Confirm", font=("times", 20, "bold"),
                                   command=lambda i=clock_number:
                                   self.change(self.continentList.get(), self.cityList.get(), i))
        self.editing_window.bind('<Return>',
                                 lambda event: self.change(self.continentList.get(), self.cityList.get(), clock_number))
        confirm_button.place(x=250, y=20)

    def update_option(self, *args):
        try:
            cities = self.data[self.continentList.get()]
        except KeyError:
            return
        self.cityList.set(cities[0])

        menu = self.cityMenu['menu']
        try:
            menu.delete(0, 'end')
        except AttributeError:
            pass

        for city in cities:
            try:
                menu.add_command(label=city, command=lambda nation=city: self.cityList.set(nation))
            except AttributeError:
                pass

    def adding_clock(self):
        current_clock_number = self.clock_amount + 1
        self.editing_clock(current_clock_number, '---', '---')

    def updating(self):
        if self.running:
            for i in range(1, self.clock_amount + 1):
                self.clock[i].updating()

    def closing_editing_window(self):
        response = messagebox.askyesno('Quiting', 'Do you want to leave without Choosing?')
        if response:
            self.editing_window.destroy()
            self.enable_button()

    def change(self, new_continent, new_city, clock_position):
        if new_continent == '---':
            self.closing_editing_window()
        else:
            if clock_position > self.clock_amount:
                self.clock_amount += 1
            self.clock[clock_position] = WorldClock(self, new_continent, new_city, clock_position)
            self.clock[clock_position].place(x=0, y=30 + (100 * (clock_position - 1)), anchor='nw',
                                             width=270, height=100)
            self.editing_window.destroy()
            self.enable_button()
            if self.clock_amount == 3:
                self.adding_button['state'] = 'disable'

    def deleted(self, position):
        self.running = False
        if self.clock_amount > position:
            for i in range(position, self.clock_amount):
                self.clock[i] = self.clock[i + 1]
                self.clock[i].place(x=0, y=30 + (100 * (i - 1)), anchor='nw',
                                    width=270, height=100)
                self.clock[i].reposition(i)
        self.clock_amount -= 1
        self.adding_button['state'] = 'normal'
        self.running = True

    def disable_button(self):
        self.adding_button['state'] = 'disable'
        for i in range(1, self.clock_amount + 1):
            self.clock[i].delete_button['state'] = 'disable'

    def enable_button(self):
        self.adding_button['state'] = 'normal'
        for i in range(1, self.clock_amount + 1):
            self.clock[i].delete_button['state'] = 'normal'
