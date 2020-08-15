import tkinter as tk
from tkinter import ttk


class MyTab(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        #self.master = master #  super() already set it

        self.btn = tk.Button(self, text='click me', command=self.change_green)
        self.btn.pack()

        self.other_tab = None # default value at start

    def change_green(self):
        if self.other_tab:

            # change color in other tab
            self.other_tab.btn.config(bg = 'green')

            # get active tab ID
            print('active tab ID:', self.master.select())

            # get button in active tab
            active_tab = root.nametowidget(self.master.select())
            print('active tab - btn text:', active_tab.btn['text'])

            # get all tabs
            print('all tabs:', self.master.children.items())

            # set other tab as active
            self.master.select(self.other_tab)

class MainApplication(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        #self.master = master #  super() already set it

        self.tab_control = ttk.Notebook(self.master)

        self.tab_1 = MyTab(self.tab_control)
        self.tab_2 = MyTab(self.tab_control)

        self.tab_1.other_tab = self.tab_2
        self.tab_2.other_tab = self.tab_1

        self.tab_control.add(self.tab_1, text = 'tab 1')
        self.tab_control.add(self.tab_2, text = 'tab 2')
        self.tab_control.pack(fill = 'both', expand = 1)

if __name__ == "__main__":
    root = tk.Tk()
    main_window = MainApplication(root)
    main_window.pack(side="top", fill="both", expand=True)
    root.mainloop()