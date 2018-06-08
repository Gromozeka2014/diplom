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
            try:
                parsed = parsed + parsers.parse_group_member_ids(group)
            except Exception as e:
                print(e)
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
        parsers.parse_users_posts_count(n.get())
        text.insert(1.0, "Посты пользователей обработаны и добавлены в БД!\n")

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
        text.insert(1.0, " - количество профилей в колекции users\n")
        text.insert(1.0, coll.find({}).count())

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
        text.insert(1.0, " - количество постов в колекции posts\n")
        text.insert(1.0, coll.find({}).count())

    def db_users_search():

        def search_param():
            client = MongoClient()
            db = client['test']
            coll = db['users']
            request = {}
            if name.get() != "":
                request["first_name"] = name.get()
            if sex_name.get() != "":
                request["sex"] = sex_name.get()
            if relation_name.get() != "":
                request["relation"] = relation_name.get()
            if country_name.get() != "":
                request["country"] = country_name.get()
            if city_name.get() != "":
                request["city"] = city_name.get()
            if university_name.get() != "":
                request["university_name"] = university_name.get()
            if faculty_name.get() != "":
                request["faculty_name"] = faculty_name.get()
            if graduation.get() != "":
                try:
                    grad = graduation.get()
                    grad = int(grad)
                except Exception as e:
                    return print(e)
                request["graduation"] = grad
            if political_name.get() != "":
                request["political"] = political_name.get()
            if religion_name.get() != "":
                request["religion"] = religion_name.get()
            if people_main_name.get() != "":
                request["people_main"] = people_main_name.get()
            if life_main_name.get() != "":
                request["life_main"] = life_main_name.get()
            if smoke_name.get() != "":
                request["smoking"] = smoke_name.get()
            if alcohol_name.get() != "":
                request["alcohol"] = alcohol_name.get()
            for user in coll.find(request):
                text.insert(1.0, user)
                text.insert(1.0, '\n\n')
            text.insert(1.0, " - найдено по данным параметрам\n")
            text.insert(1.0, coll.find(request).count())

        search = Toplevel()
        s_search = Style()
        s_search.configure('My.TFrame', background='silver')
        search.title("Выбор параметров поиска")
        search.geometry("600x268")
        search_frame1 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame1.pack(fill=BOTH)
        name_label = Label(search_frame1, text="Имя:")
        name_label.pack(side=LEFT, padx=5, pady=5)
        name = StringVar()
        entry_name = Entry(search_frame1, textvariable=name, width=20)
        entry_name.pack(side=LEFT, padx=5, pady=5)
        family_name = StringVar()
        entry_family_name = Entry(search_frame1, textvariable=family_name, width=20)
        entry_family_name.pack(side=RIGHT, padx=5, pady=5)
        family_name_label = Label(search_frame1, text="Фамилия:")
        family_name_label.pack(side=RIGHT, padx=5, pady=5)

        search_frame2 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame2.pack(fill=BOTH)
        name_label3 = Label(search_frame2, text="Пол:")
        name_label3.pack(side=LEFT, padx=5, pady=5)
        sex_name = StringVar()
        combobox1 = Combobox(search_frame2, values=[u"мужской", u"женский"], textvariable=sex_name, width=20)
        combobox1.pack(side=LEFT, padx=5, pady=5)
        relation_name = StringVar()
        combobox2 = Combobox(search_frame2, values=[u"не женат/не замужем", u"есть друг/есть подруга",
                                                    u"помолвлен/помолвлена", u"женат/замужем", u"всё сложно",
                                                    u"в активном поиске", u"влюблён/влюблена", u"в гражданском браке",
                                                    u"не указано"], textvariable=relation_name, width=20)
        combobox2.pack(side=RIGHT, padx=5, pady=5)
        name_label4 = Label(search_frame2, text="Отношения:")
        name_label4.pack(side=RIGHT, padx=5, pady=5)

        search_frame3 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame3.pack(fill=BOTH)
        name_label5 = Label(search_frame3, text="Город:")
        name_label5.pack(side=LEFT, padx=5, pady=5)
        city_name = StringVar()
        entry_city_name = Entry(search_frame3, textvariable=city_name, width=20)
        entry_city_name.pack(side=LEFT, padx=5, pady=5)
        country_name = StringVar()
        entry_country_name = Entry(search_frame3, textvariable=country_name, width=20)
        entry_country_name.pack(side=RIGHT, padx=5, pady=5)
        name_label6 = Label(search_frame3, text="Страна:")
        name_label6.pack(side=RIGHT, padx=5, pady=5)

        search_frame4 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame4.pack(fill=BOTH)
        name_label7 = Label(search_frame4, text="Университет:")
        name_label7.pack(side=LEFT, padx=5, pady=5)
        university_name = StringVar()
        entry_university_name = Entry(search_frame4, textvariable=university_name, width=20)
        entry_university_name.pack(side=LEFT, padx=5, pady=5)
        name_label8 = Label(search_frame4, text="Факультет:")
        name_label8.pack(side=LEFT, padx=5, pady=5)
        faculty_name = StringVar()
        entry_faculty_name = Entry(search_frame4, textvariable=faculty_name, width=20)
        entry_faculty_name.pack(side=LEFT, padx=5, pady=5)
        name_label9 = Label(search_frame4, text="Год окончания:")
        name_label9.pack(side=LEFT, padx=5, pady=5)
        graduation = StringVar()
        entry_graduation = Entry(search_frame4, textvariable=graduation, width=10)
        entry_graduation.pack(side=LEFT, padx=5, pady=5)

        search_frame5 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame5.pack(fill=BOTH)
        name_label10 = Label(search_frame5, text="Политические взгляды:")
        name_label10.pack(side=LEFT, padx=5, pady=5)
        political_name = StringVar()
        combobox3 = Combobox(search_frame5, values=[u"коммунистические", u"социалистические", u"умеренные",
                                                    u"либеральные", u"консервативные", u"монархические",
                                                    u"ультраконсервативные", u"индифферентные", u"либертарианские"],
                             textvariable=political_name, width=20)
        combobox3.pack(side=LEFT, padx=5, pady=5)
        religion_name = StringVar()
        entry_religion_name = Entry(search_frame5, textvariable=religion_name, width=20)
        entry_religion_name.pack(side=RIGHT, padx=5, pady=5)
        name_label11 = Label(search_frame5, text="Религиозные взгляды:")
        name_label11.pack(side=RIGHT, padx=5, pady=5)

        search_frame6 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame6.pack(fill=BOTH)
        name_label11 = Label(search_frame6, text="Главное в людях:")
        name_label11.pack(side=LEFT, padx=5, pady=5)
        people_main_name = StringVar()
        combobox4 = Combobox(search_frame6, values=[u"ум и креативность", u"доброта и честность", u"красота и здоровье",
                                                    u"власть и богатство", u"смелость и упорство",
                                                    u"юмор и жизнелюбие"],
                             textvariable=people_main_name, width=20)
        combobox4.pack(side=LEFT, padx=5, pady=5)
        life_main_name = StringVar()
        combobox5 = Combobox(search_frame6, values=[u"семья и дети", u"карьера и деньги", u"развлечения и отдых",
                                                    u"наука и исследования", u"совершенствование мира", u"саморазвитие",
                                                    u"красота и искусство", u"слава и влияние"],
                             textvariable=life_main_name, width=20)
        combobox5.pack(side=RIGHT, padx=5, pady=5)
        name_label12 = Label(search_frame6, text="Главное в жизни:")
        name_label12.pack(side=RIGHT, padx=5, pady=5)

        search_frame7 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame7.pack(fill=BOTH)
        name_label13 = Label(search_frame7, text="Отношение к курению:")
        name_label13.pack(side=LEFT, padx=5, pady=5)
        smoke_name = StringVar()
        combobox6 = Combobox(search_frame7, values=[u"резко негативное", u"негативное", u"компромиссное",
                                                    u"нейтральное", u"положительное", u"саморазвитие"],
                             textvariable=smoke_name, width=20)
        combobox6.pack(side=LEFT, padx=5, pady=5)
        name_label14 = Label(search_frame7, text="Отношение к алкоголю:")
        name_label14.pack(side=LEFT, padx=5, pady=5)
        alcohol_name = StringVar()
        combobox7 = Combobox(search_frame7, values=[u"резко негативное", u"негативное", u"компромиссное",
                                                    u"нейтральное", u"положительное", u"саморазвитие"],
                             textvariable=alcohol_name, width=20)
        combobox7.pack(side=LEFT, padx=5, pady=5)

        search_frame8 = Frame(search, style='My.TFrame', borderwidth=1)
        search_frame8.pack(fill=BOTH)
        start_db_search = Button(search_frame8, text="Запуск поиска", command=search_param)
        start_db_search.pack(padx=5, pady=5)

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
    db_data_remove_btn = Button(frame3, text="Очистить БД", command=db_data_remove)
    db_data_remove_btn.pack(side=RIGHT, padx=5, pady=5)

    frame4 = Frame(borderwidth=1)
    frame4.pack(fill=BOTH)
    posts_parser_dict_btn = Button(frame4, text="Сбор постов по ключевым словам", command=pars_posts_dict)
    posts_parser_dict_btn.pack(side=LEFT, padx=5, pady=5)
    db_find_users_btn = Button(frame4, text="Вывод Users", command=db_find_users)
    db_find_users_btn.pack(side=RIGHT, padx=5, pady=5)
    db_find_posts_btn = Button(frame4, text="Вывод Posts", command=db_find_posts)
    db_find_posts_btn.pack(side=RIGHT, padx=5, pady=5)
    db_find_posts_btn = Button(frame4, text="Поиск по пользователям", command=db_users_search)
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
