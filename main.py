import file_handler
import parsers
import db_handler

import os
from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.ttk import *


def main():
    def pars_id_group():
        group_list = file_handler.read_file('support_files/group_id.txt')
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
        text.insert(1.0, "ID Пользователей из групп собранны!\n")

    def pars_users():
        parsers.parse_users_data()
        text.insert(1.0, "Информация о пользователях собранна и добавлена в БД!\n")

    def pars_posts_n():
        try:
            parsers.parse_users_posts_count(n.get())
            text.insert(1.0, "Посты пользователей обработаны и добавлены в БД!\n")
        except Exception as e:
            print(e)

    def pars_posts_dict():
        parsers.parse_users_posts_dict()
        text.insert(1.0, "Посты пользователей обработаны и добавлены в БД!\n")

    def start_db_server():
        os.system('db_start.bat')
        text.insert(1.0, "Сервер запущен!\n")

    def start_db_manager():
        os.system('db_manager.bat')
        text.insert(1.0, "Менеджер запущен!\n")

    def export_db():
        os.startfile('db_export.bat')
        text.insert(1.0, "Экспорт запущен!\n")

    def db_data_remove():
        answer = mb.askyesno(title="Вы уверены???", message="Удалить все данные из БД???")
        if answer is True:
            db_handler.db_data_remove()
            text.insert(1.0, "Данные удалены!\n")

    def insert_text():
        try:
            file_name = fd.askopenfilename()
            f = open(file_name)
            fa = f.read()
            text.insert(1.0, fa)
            f.close()
        except Exception as e:
            print(e)

    def extract_text():
        try:
            file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                        ("CFG files", "*.cfg"),
                                                        ("All files", "*.*")))
            f = open(file_name, 'w')
            fa = text.get(1.0, END)
            f.write(fa)
            f.close()
        except Exception as e:
            print(e)

    def clr_text():
        answer = mb.askyesno(title="Вы уверены???", message="Удалить все данные из окна ввода???")
        if answer is True:
            text.delete(1.0, END)

    def db_find_users():
        client = MongoClient()
        db = client['test']
        coll = db['users']
        for user in coll.find({}):
            text.insert(1.0, user)
            text.insert(1.0, '\n\n')
        text.insert(1.0, coll.find({}).count())
        text.insert(1.0, "Количество профилей в колекции users: ")

    def db_find_posts():
        client = MongoClient()
        db = client['test']
        coll = db['posts']
        for post in coll.find({}):
            try:
                text.insert(1.0, post)
                text.insert(1.0, '\n\n')
            except Exception as e:
                print(e)
        text.insert(1.0, coll.find({}).count())
        text.insert(1.0, "Количество постов в колекции posts: ")

    root = Tk()

    s = Style()
    s.configure('My.TFrame', background='silver')
    root.title("Приложения для сбора и обработки данных пользователей ВКонтакте")
    root.geometry("600x400")

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
    entry_count = Entry(frame3, textvariable=n, width=5)
    entry_count.pack(side=LEFT, padx=5, pady=5)
    import_db_manager_btn = Button(frame3, text="Экспорт БД", command=export_db)
    import_db_manager_btn.pack(side=RIGHT, padx=5, pady=5)

    frame4 = Frame(borderwidth=1)
    frame4.pack(fill=BOTH)
    posts_parser_dict_btn = Button(frame4, text="Сбор постов по ключевым словам", command=pars_posts_dict)
    posts_parser_dict_btn.pack(side=LEFT, padx=5, pady=5)
    db_data_remove_btn = Button(frame4, text="Отчистить БД", command=db_data_remove)
    db_data_remove_btn.pack(side=RIGHT, padx=5, pady=5)
    db_find_users_btn = Button(frame4, text="Вывод Users", command=db_find_users)
    db_find_users_btn.pack(side=RIGHT, padx=5, pady=5)
    db_find_posts_btn = Button(frame4, text="Вывод Posts", command=db_find_posts)
    db_find_posts_btn.pack(side=RIGHT, padx=5, pady=5)

    frame5 = Frame(style='My.TFrame', borderwidth=1)
    frame5.pack(fill=BOTH)
    open_file_btn = Button(frame5, text="Открыть", command=insert_text)
    open_file_btn.pack(side=RIGHT, padx=5, pady=5)
    save_file_btn = Button(frame5, text="Сохранить", command=extract_text)
    save_file_btn.pack(side=RIGHT, padx=5, pady=5)
    clr_text_btn = Button(frame5, text="Очистить", command=clr_text)
    clr_text_btn.pack(side=RIGHT, padx=5, pady=5)
    info = Label(frame5, text="Поле ввода, вывода и редактирования:", font="8")
    info.pack(side=LEFT, padx=5, pady=5)

    frame6 = Frame(style='My.TFrame', borderwidth=1)
    frame6.pack(fill=BOTH, expand=True)
    text = Text(frame6, width=74, height=13, wrap=WORD)
    text.pack(side="left", fill="both", expand=True)
    root.mainloop()

if __name__ == '__main__':
        main()
