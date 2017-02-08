# -*- coding: utf-8 -*-

#   Copyright 2017 Zachary Marv (马子昂)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


#   Library tagger GUI
#
#   When tagging libraries using this script, you could refer to
#   https://raw.githubusercontent.com/pkumza/LibRadar/v1.4.0/data/tgst5.dat and
#   https://github.com/pkumza/LibRadar/blob/dev/extract/step2.py
#
#   Introduction:
#       This script is not used for tagging libraries actually, It gives you some untagged libraries and you could set a
#       rule for tagging.
#       As there would be so many packages and so many libraries, it not possible to tag them one by one.
#       There could be many versions of libraries, so there's some repeat work.
#
#       We presume that more than half package names of a library is un-obfuscated, in this case, we could know the true
#       package name but we could not get the real library name, the website, type, or the other information.
#
#       tag_rules.csv is a projection from un-obfuscated package name to its detailed information.
#
#   Usage:
#       Run this script or just modify Data/IntermediateData/tag_rules.csv


import lib_tagging
import csv
import os
from _settings import FILE_RULE

from Tkinter import *           # 导入 Tkinter 库
import ttk


class TaggerGui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        # Frame 1 Welcome
        self.create_f1_welcome()
        # read csv
        # contains items like android/support/v4, org/apache/http,
        self.labeled_prefix = list()
        # contains items like com/android, com/google
        self.no_lib_prefix = list()
        if os.path.exists(FILE_RULE):
            file_rules = open(FILE_RULE, 'r')
            csv_rules_reader = csv.reader(file_rules, delimiter=',', quotechar='|')
            for row in csv_rules_reader:
                if row[1] == "no":
                    self.no_lib_prefix.append(row[0])
                else:
                    self.labeled_prefix.append(row[0])
            file_rules.close()
        self.file_rules_w = open(FILE_RULE, 'a')
        self.csv_rule_writer = csv.writer(self.file_rules_w, delimiter=',', quotechar='|')

    def create_f1_welcome(self):
        self.hello_label = Label(self,
                                 text='\nHello!\nThis is LibRadar Tagging System.\n'
                                      'Author:  Zachary Marv')
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
        self.hello_label = Label(self,
                                 text="\nPlease input some arguments for this system.\nThis would take a few moments,"
                                      " please wait.")
        self.hello_label.pack()
        self.count_label = Label(self, text="Base count (default 20):")
        self.count_label.pack()
        self.count_text = StringVar()
        self.count_entry = Entry(self, textvariable=self.count_text)
        self.count_entry.pack()
        self.weight_text = StringVar()
        self.weight_label = Label(self, text="Weight count (default 20):")
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
            if self.weight_text.get() == "":
                self.base_weight = 20
            else:
                self.base_weight = int(self.weight_text.get())
            if self.count_text.get() == "":
                self.base_count = 20
            else:
                self.base_count = int(self.count_text.get())

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
            self.init_data_for_f3()
        else:
            self.create_f2_init()

    def init_data_for_f3(self):
        """frame for tagging"""
        # self.master.geometry("300x120")
        self.tagger = lib_tagging.Tagger(self.base_count, self.base_weight)
        self.features = self.tagger.get_potential_list()
        self.create_f3_init()

    def create_f3_init(self):
        """

        :return:
        """
        """
        INFO
        """
        self.master.geometry("300x520")
        self.label_index = -1
        self.labeled_cnt = 0

        """
        GUI
        """
        self.label_message = Label(self, text="")
        self.label_message.pack()
        self.label_progress = Label(self, text="\nProgress:")
        self.label_progress.pack()

        self.label_count = Label(self, text="\nPopularity:")
        self.label_count.pack()
        self.n_label_count = Label(self, text="")
        self.n_label_count.pack()
        self.label_weight = Label(self, text="API number:")
        self.label_weight.pack()
        self.n_label_weight = Label(self, text="")
        self.n_label_weight.pack()
        self.label_package_name = Label(self, text="Package Name:")
        self.label_package_name.pack()
        self.n_label_package_name = Label(self, text="")
        self.n_label_package_name.pack()
        self.label_tagging = Label(self, text="Library prefix:")
        self.label_tagging.pack()
        self.t_lib_prefix = StringVar()
        self.entry_prefix = Entry(self, textvariable=self.t_lib_prefix)
        self.entry_prefix.pack()
        self.label_lib_name = Label(self, text="Library Name:")
        self.label_lib_name.pack()
        self.t_lib_name = StringVar()
        self.entry_name = Entry(self, textvariable=self.t_lib_name)
        self.entry_name.pack()
        self.label_type = Label(self, text="Library Type:")
        self.label_type.pack()
        self.t_lib_type = StringVar()
        self.type_chosen = ttk.Combobox(self, textvariable=self.t_lib_type)
        self.type_chosen['values'] = (
            "Development Aid",
            "Social Network",
            "Advertisement",
            "App Market",
            "Mobile Analytics",
            "Payment",
            "Game Engine",
            "Map/LBS",
            "GUI Component",
            "Development Framework",
            "Not Sure"
        )
        self.type_chosen.current(0)
        self.type_chosen.pack()
        self.label_website = Label(self, text="Official SDK Website:")
        self.label_website.pack()
        self.t_website = StringVar()
        self.entry_website = Entry(self, textvariable=self.t_website)
        self.entry_website.pack()
        self.button_tag = Button(self, text="Tag!", command=self.insert_csv)
        self.button_tag.pack()
        self.button_ignore = Button(self, text="I don't know", command=self.ignore_f3)
        self.button_ignore.pack()
        self.button_not = Button(self, text="This package is definitely not a library!", command=self.insert_not_csv)
        self.button_not.pack()

        self.create_f3()

    def tagged(self, package_name):
        """
        Determine if package_name needed to be tagged.
        :param package_name: the package name to be determined.
        :return: boolean
        """
        # never found it is tagged.
        flag = False
        for prefix in self.labeled_prefix:
            if prefix in package_name:
                flag = True
                break
        if flag:
            return flag
        for prefix in self.no_lib_prefix:
            if prefix == package_name:
                flag = True
                break
        return flag

    def create_f3(self):
        """
        loop and loop
        :return:
        """

        # Clear Text
        self.t_website.set("")
        self.t_lib_name.set("")

        # Index++
        self.label_index += 1
        # Ignore those tagged libs.
        while self.label_index < len(self.features) and self.tagged(self.features[self.label_index][3]):
            self.label_index += 1
        if self.label_index >= len(self.features):
            self.destroy_f3()
            return

        self.t_lib_prefix.set(self.features[self.label_index][3])
        # Show information
        self.label_progress["text"] = "\nProgress: %d/%d" % (self.label_index + 1, len(self.features))
        self.n_label_count["text"] = str(self.features[self.label_index][1])
        self.n_label_weight["text"] = str(self.features[self.label_index][2])
        self.n_label_package_name["text"] = str(self.features[self.label_index][3])

    def ignore_f3(self):
        self.label_message["text"] = ""
        self.create_f3()

    def insert_csv(self):
        """

        :return:
        """
        self.label_message["text"] = ""
        good_flag = True
        lib_name = ""
        lib_type = ""
        website = ""
        prefix = ""
        try:
            prefix = self.t_lib_prefix.get()
            if self.features[self.label_index][3][:len(prefix)] != prefix:
                self.label_message["text"] = "Prefix not the same! try again!"
                self.label_index -= 1
                self.create_f3()
                return
            lib_name = self.t_lib_name.get()
            website = self.t_website.get()
            lib_type = self.t_lib_type.get()
        except:
            good_flag = False
        if good_flag:
            # insert into csv
            self.csv_rule_writer.writerow([prefix, lib_name, lib_type, website])
            # insert the prefix into list
            self.labeled_prefix.append(prefix)
        else:
            # ignore
            pass
        self.create_f3()

    def insert_not_csv(self):
        """

        :return:
        """
        self.label_message["text"] = ""
        good_flag = True
        lib_name = ""
        website = ""
        prefix = ""
        try:
            prefix = str(self.features[self.label_index][3])
            lib_name = "no"
            website = "no"
        except:
            good_flag = False
        if good_flag:
            # insert into csv
            self.csv_rule_writer.writerow([prefix, lib_name, "no", website])
            # insert the prefix into list
            self.no_lib_prefix.append(prefix)
        else:
            # ignore
            pass
        self.create_f3()


    def destroy_f3(self):
        self.label_message.destroy()
        self.label_progress.destroy()
        self.label_count.destroy()
        self.n_label_count.destroy()
        self.label_weight.destroy()
        self.n_label_weight.destroy()
        self.label_package_name.destroy()
        self.n_label_package_name.destroy()
        self.label_tagging.destroy()
        self.entry_prefix.destroy()
        self.label_lib_name.destroy()
        self.entry_name.destroy()
        self.label_website.destroy()
        self.entry_website.destroy()
        self.button_tag.destroy()
        self.button_ignore.destroy()
        self.button_not.destroy()

        # Create Exit
        self.create_f4()

    def create_f4(self):
        """
        You have tagged XXXX libs.
        :param self:
        :return:
        """
        self.hello_label = Label(self, text='The End\nplease exit.')
        self.hello_label.pack(side=TOP)
        pass


if __name__ == '__main__':
    app = TaggerGui()
    # Set title
    app.master.title('LibRadar Tagging System')
    # Size
    app.master.geometry("300x160")
    # Main loop
    app.mainloop()
