import file_handler
import parsers

import time
import os
from tkinter import *
from tkinter.ttk import *


def main():
    def pars_id_group():
        group_list = file_handler.read_id('support_files/group_id.txt')
        parsed = []
        filtered = []
        for group in group_list:
            parsed = parsed + parsers.parse_group_member_ids(group)
        for user in parsed:
            if user not in filtered:
                filtered.append(user)
        with open('support_files/users_id.txt', 'w') as f:
            for line in filtered:
                f.write(str(line) + '\n')

    def pars_users():
        parsers.parse_users_data()

    def pars_posts_n():
        try:
            parsers.parse_users_posts_count(n.get())
        except Exception as e:
            print(e)

    def pars_posts_dict():
        parsers.parse_users_posts_dict()

    def start_db_server():
        os.system('db_start.bat')

    def start_db_manager():
        os.system('db_manager.bat')

    def import_db():
        os.system('db_import.bat')

    root = Tk()

    s = Style()
    s.configure('My.TFrame', background='silver')
    root.title("Приложения для сбора и обработки данных пользователей ВКонтакте")
    root.geometry("600x250")

    frame1 = Frame(style='My.TFrame', borderwidth=1)
    frame1.pack(fill=BOTH)
    parse_id_groups_btn = Button(frame1, text="Сбор ID из групп", command=pars_id_group)
    parse_id_groups_btn.pack(side=LEFT, padx=5, pady=5)
    start_db_btn = Button(frame1, text="Запуск сервера БД", command=start_db_server)
    start_db_btn.pack(side=RIGHT, padx=5, pady=5)

    frame2 = Frame(borderwidth=1)
    frame2.pack(fill=BOTH)
    users_parser_btn = Button(frame2, text="Сбор информации о пользователях", command=pars_users)
    users_parser_btn.pack(side=LEFT, padx=5, pady=5)
    start_db_manager_btn = Button(frame2, text="Запуск менеджера БД", command=start_db_manager)
    start_db_manager_btn.pack(side=RIGHT, padx=5, pady=5)

    frame3 = Frame(style='My.TFrame', borderwidth=1)
    frame3.pack(fill=BOTH)
    n = IntVar()
    posts_parser_count_btn = Button(frame3, text="Сбор последних N постов", command=pars_posts_n)
    posts_parser_count_btn.pack(side=LEFT, padx=5, pady=5)
    entry_count = Entry(frame3, textvariable=n)
    entry_count.pack(side=LEFT, padx=5, pady=5)
    import_db_manager_btn = Button(frame3, text="Импорт БД", command=import_db)
    import_db_manager_btn.pack(side=RIGHT, padx=5, pady=5)

    frame4 = Frame(borderwidth=1)
    frame4.pack(fill=BOTH)
    posts_parser_dict_btn = Button(frame4, text="Сбор постов по ключевым словам", command=pars_posts_dict)
    posts_parser_dict_btn.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
        main()
