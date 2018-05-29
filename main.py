import file_handler
import parsers

import time
import os


def main():
    menu = input("Для начала сбора информации, введите 'I'\n"
                 "Для управления БД, введите 'B'\n")
    if menu.upper() == "I":
        menu_pars = input("Для запуска сбора информации по списку пользователей, введите 'U'\n"
                          "Для запуска сбора информации о пользователях из списка групп, введите 'G'\n")
        if menu_pars.upper() == "G":
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
            print('id пользователей из указанных групп собраны.')
            main()
        elif menu_pars.upper() == "U":
            start_time = time.time()
            parsers.parse_users_data()
            parsers.parse_users_posts()
            print("--- %s seconds ---" % (time.time() - start_time))
        else:
            print("Некорректный запрос.")
            main()
    elif menu.upper() == "B":

        menu_db = input("Для запуска сервера MongoDB, введите 'S'\n"
                        "Для запуска менеджера MongoDB введите: 'M'\n"
                        "Для того что бы импортировать базу данных, введите: 'I'\n")
        if menu_db.upper() == "S":
            os.system('db_start.bat')
            main()
        elif menu_db.upper() == "M":
            os.system('db_manager.bat')
            main()
        elif menu_db.upper() == "I":
            os.system('db_import.bat')
            main()
        else:
            print("Некорректный запрос.")
            main()
    else:
        print("Некорректный запрос.")
        main()

if __name__ == '__main__':
        main()
