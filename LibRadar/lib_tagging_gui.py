# -*- coding: utf-8 -*-
"""
    Library tagger GUI

"""

import lib_tagging

from Tkinter import *           # 导入 Tkinter 库


class TaggerGui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        # Frame 1 Welcome
        self.create_f1_welcome()

    def create_f1_welcome(self):
        self.hello_label = Label(self, text='\nHello!\nThis is LibRadar Tagging System.\n'
                                           'Version: 2.0.1.dev1\n'
                                           'Author:  Zachary Ma')
        self.hello_label.pack(side=TOP)
        self.next_button = Button(self, text="Next", command=self.destroy_f1)
        self.next_button.pack()
        self.quit_button = Button(self, text='Quit', command=self.quit)
        self.quit_button.pack()

    def destroy_f1(self):
        self.hello_label.destroy()
        self.next_button.destroy()
        self.quit_button.destroy()
        self.create_f2_init()

    def create_f2_init(self):
        self.master.geometry("300x210")
        self.hello_label = Label(self, text="\nPlease input some arguments for this system.\n")
        self.hello_label.pack()
        self.count_label = Label(self, text="Base count:")
        self.count_label.pack()
        self.count_text = StringVar()
        self.count_entry = Entry(self, textvariable=self.count_text)
        self.count_entry.pack()
        self.weight_text = StringVar()
        self.weight_label = Label(self, text="Weight count:")
        self.weight_label.pack()
        self.weight_entry = Entry(self, textvariable=self.weight_text)
        self.weight_entry.pack()
        self.d2c3_button = Button(self, text="Next", command=self.destroy_f2)
        self.d2c3_button.pack()

    def destroy_f2(self):
        self.base_count = -1
        self.base_weight = -1
        good_flag = True
        try:
            self.base_count = int(self.count_text.get())
            self.base_weight = int(self.weight_text.get())
        except:
            good_flag = False
        if self.base_count < 0:
            good_flag = False
        if self.base_weight < 0:
            good_flag = False
        self.hello_label.destroy()
        self.count_label.destroy()
        self.count_entry.destroy()
        self.weight_label.destroy()
        self.weight_entry.destroy()
        self.d2c3_button.destroy()
        if good_flag:
            self.create_f3()
        else:
            self.create_f2_init()

    def create_f3(self):
        self.master.geometry("300x120")
        self.hello_label = Label(self, text="\nWaiting...\n")
        self.hello_label.pack()
        self.tagger = lib_tagging.Tagger(self.base_count, self.base_weight)
        self.features = self.tagger.get_potential_list()
        print self.features

if __name__ == '__main__':
    app = TaggerGui()
    # Set title
    app.master.title('LibRadar Tagging System')
    # Size
    app.master.geometry("300x160")
    # Main loop
    app.mainloop()