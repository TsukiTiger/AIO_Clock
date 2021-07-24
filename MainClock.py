import datetime
import tkinter as tk


class MainClock(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.current_time_label = tk.Label(parent, text=self.label_text(),
                                           font=controller.FONT_S)

        self.current_time_label.pack(side='left', fill='both')

    @staticmethod
    def current_time():
        local_time = datetime.datetime.now()
        time = local_time.strftime("%H:%M:%S")
        return time

    @staticmethod
    def current_timezone():
        local_time = datetime.datetime.now()
        local_timezone = local_time.astimezone().tzinfo
        return local_timezone

    def label_text(self):
        text = f'Current Time: {self.current_time()}  Timezone: {self.current_timezone()}'
        return text

    def updating(self):
        self.current_time_label['text'] = self.label_text()
