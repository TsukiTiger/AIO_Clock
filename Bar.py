import tkinter as tk


class Bar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.Button = {}
        self.key_list = ['WorldClock', 'Alarm', 'StopWatch', 'Timer']

        self.controller = controller

        for choice in self.key_list:
            self.Button[choice] = tk.Button(parent,
                                            text=choice,
                                            command=lambda i=choice: self.clicked(i),
                                            font=controller.FONT_S,
                                            fg='black',
                                            width=11, height=50)
            self.Button[choice].pack(side='left')

        self.Button['WorldClock'].config(fg='red')

    def clear(self):
        for key in self.key_list:
            self.Button[key].config(fg='black')

    def clicked(self, text):
        self.clear()
        self.Button[text].config(fg='red')
        page_name = f'{text}_Frame'
        self.controller.show_frame(page_name)
