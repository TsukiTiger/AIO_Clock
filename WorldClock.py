import tkinter as tk
import pytz
from datetime import datetime
from tkinter import messagebox


class WorldClock(tk.Frame):
    def __init__(self, controller, continent, city, position):
        tk.Frame.__init__(self, controller)

        self.city = city
        self.continent = continent
        self.position = position
        self.controller = controller

        city_label = tk.Label(self, text=self.city, font=("times", 20, "bold"))
        city_label.place(x=60, y=5)
        self.time = tk.Label(self, text=self.label_time(), font=("times", 33, "bold"))
        self.time.place(x=30, y=40)
        nota = tk.Label(self, text="Hours   Minutes   Seconds", font=("times", 10, "bold"))
        nota.place(x=30, y=80)
        self.clock_number = tk.Label(self, text="Clock #" + str(position), font=("times", 12))
        self.clock_number.place(x=200, y=10)

        self.delete_button = tk.Button(self, text='x', font=("times", 20, "bold"), fg='red',
                                       command=self.deleting)
        self.delete_button.place(x=0, y=0)

    def label_time(self):
        place = str(self.continent) + "/" + str(self.city)
        timezone = pytz.timezone(place)
        local_time = datetime.now(timezone)
        current_time = local_time.strftime("%H:%M:%S")
        return current_time
    
    def updating(self):
        self.time['text'] = self.label_time()
        
    def reposition(self, new_position):
        self.position = new_position
        self.clock_number = tk.Label(self, text="Clock #" + str(self.position), font=("times", 12))
        self.clock_number.place(x=200, y=10)

    def deleting(self):
        response = messagebox.askyesno('Deleting', f'Do You want to Delete Clock #{self.position}?')
        if response:
            for widgets in self.winfo_children():
                widgets.destroy()
            self.controller.deleted(self.position)
