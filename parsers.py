import file_handler
import db_handler
import const

import vk_requests
import time


def parse_group_member_ids(group_id):
    conf = file_handler.pars_secure_config()
    api = vk_requests.create_api(service_token=conf.get('app', 'token'), interactive=True)
    count = api.groups.getMembers(group_id=group_id, count=0)
    count = count['count']
    count_n = (count // 1000)
    ids_list = []
    try:
        for i in range(count_n + 1):
            ids = api.groups.getMembers(group_id=group_id, count=1000, offset=1000*i)
            ids_list = ids_list + ids['items']
        return ids_list
    except Exception as e:
        print(e)


def parse_users_data():
    conf = file_handler.pars_secure_config()
    api = vk_requests.create_api(service_token=conf.get('app', 'token'), interactive=True)
    users_list = file_handler.read_file('support_files/users_id.txt')
    new_users_list = []
    try:
        request_for_user(api, users_list, new_users_list)
    except Exception as e:
        print(e)
        time.sleep(1)
        request_for_user(api, users_list, new_users_list)
    with open('support_files/users_id.txt', 'w') as f:
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


def parse_users_posts_count(n):
    api = pars_posts_api_init()
    new_users_list = file_handler.read_file('support_files/users_id.txt')
    try:
        n = int(n)
    except Exception as e:
        return print(e)
    for user in new_users_list:
        try:
            request_for_posts_count(api, user, n)
        except Exception as e:
            if "error_code=18" in e.__str__():
                print(e)
            elif "error_code=6" in e.__str__():
                time.sleep(1)
                request_for_posts_count(api, user, n)
            else:
                print(e)


def request_for_posts_count(api, user, n):
    parsed = api.wall.get(owner_id=user, count=n)
    for post in parsed['items']:
        print(post['id'], "Обработан.")
        db_handler.db_save_users_posts(post)


def pars_posts_api_init():
    conf = file_handler.pars_secure_config()
    login = conf.get('account', 'login')
    password = conf.get('account', 'password')
    api_id = conf.get('account', 'api_id')
    api = vk_requests.create_api(app_id=api_id, login=login, password=password, interactive=True)
    return api


def parse_users_posts_dict():
    api = pars_posts_api_init()
    new_users_list = file_handler.read_file('support_files/users_id.txt')
    for user in new_users_list:
        try:
            request_for_posts_dict(api, user)
        except Exception as e:
            print(e)
            time.sleep(1)
            request_for_posts_dict(api, user)


def request_for_posts_dict(api, user):
    search = ''
    words = file_handler.read_file('support_files/keywords.txt')
    for word in words:
        search = search + ' ' + word
    parsed = api.wall.search(owner_id=user, query=search)
    for post in parsed['items']:
        print(post['id'], "Обработан.")
        db_handler.db_save_users_posts(post)
