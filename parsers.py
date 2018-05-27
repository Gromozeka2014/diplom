import file_handler
import db_handler
import const

import vk_requests
import time


def parse_group_member_ids(group_id):
    conf = file_handler.pars_secure_config()
    api = vk_requests.create_api(service_token=conf.get('app', 'token'))
    ids = api.groups.getMembers(group_id=group_id, count=1000)
    ids = ids['items']
    return ids


def parse_users_data():
    conf = file_handler.pars_secure_config()
    api = vk_requests.create_api(service_token=conf.get('app', 'token'))
    users_list = file_handler.read_id('users_id.txt')
    new_users_list = []
    try:
        request_for_user(api, users_list, new_users_list)
    except Exception as e:
        print(e)
        time.sleep(1)
        request_for_user(api, users_list, new_users_list)
    with open('users_id.txt', 'w') as f:
        for line in new_users_list:
            f.write(str(line) + '\n')


def request_for_user(api, users_list, new_users_list):
    for user in users_list:
        parsed = api.users.get(user_ids=user, fields=const.parsed_info)
        user_data = dict(parsed[0])
        if 'deactivated' in user_data:
            print('пользователь ', user_data['id'], ' удален или забанен.')
        else:
            print(user_data['id'], 'добавлен.')
            db_handler.db_save_users_data(user_data)
            new_users_list.append(user)


def parse_users_posts():
    n = -1
    conf = file_handler.pars_secure_config()
    login = conf.get('account', 'login')
    password = conf.get('account', 'password')
    api_id = conf.get('account', 'api_id')
    api = vk_requests.create_api(app_id=api_id, login=login, password=password)
    new_users_list = file_handler.read_id('users_id.txt')
    while type(n) is not int or n < 0 or n > 100:
        n = count_test()
    for user in new_users_list:
            try:
                request_for_posts(api, user, n)
            except Exception as e:
                print(e)
                time.sleep(1)
                request_for_posts(api, user, n)


def request_for_posts(api, user, n):
    parsed = api.wall.get(owner_id=user, count=n)
    for post in parsed['items']:
        print(post['id'], "добавлен.")
        db_handler.db_save_users_posts(post)


def count_test():
    try:
        n = input("Введите количество обрабатываемых постов для одного пользователя (не более 100): ")
        n = int(n)
        return n
    except Exception as e:
        print(e)
