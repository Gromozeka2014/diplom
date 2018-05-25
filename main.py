import const
import configparser
import vk_requests
import time
from pymongo import MongoClient


def parse_group_member_ids(group_id):
    conf = pars_secure_config()
    api = vk_requests.create_api(service_token=conf.get('app', 'token'))
    ids = api.groups.getMembers(group_id=group_id, count=1000)
    ids = ids['items']
    return ids


def parse_users_data():
    conf = pars_secure_config()
    api = vk_requests.create_api(service_token=conf.get('app', 'token'))
    users_list = read_id('users_id.txt')
    new_users_list = []
    try:
        for user in users_list:
            parsed = api.users.get(user_ids=user, fields=const.parsed_info)
            user_data = dict(parsed[0])
            if 'deactivated' in user_data:
                print('пользователь ', user_data['id'], ' удален или забанен.')
            else:
                print(user_data['id'], 'добавлен.')
                db_save_users_data(user_data)
                new_users_list.append(user)
        with open('users_id.txt', 'w') as f:
            for line in new_users_list:
                f.write(str(line) + '\n')
    except Exception as e:
        print(e)
        time.sleep(1)


def pars_users_posts():
    conf = pars_secure_config()
    login = conf.get('account', 'login')
    password = conf.get('account', 'password')
    api_id = conf.get('account', 'api_id')
    api = vk_requests.create_api(app_id=api_id, login=login, password=password)
    new_users_list = read_id('users_id.txt')
    for user in new_users_list:
        try:
            parsed = api.wall.get(owner_id=user, count=2)
            print(parsed)
        except Exception as e:
            print(e)
            time.sleep(1)


def db_save_users_data(user_data):
    client = MongoClient()
    db = client['test']
    coll = db['users']
    user_id = user_data.pop('id')
    coll.save({"_id": user_id})
    dict_update(user_data)
    coll.update({"_id": user_id}, user_data)


def pars_secure_config():
    conf = configparser.RawConfigParser()
    conf.read('config.cfg')
    return conf


def read_id(sours):
    id_list = []
    f = open(sours, 'r')
    for line in f:
        id_list.append(line.strip())
    return id_list


def dict_update(data_dict):
    for home in const.home_title:
        if home in data_dict:
            data_dict.update({home: data_dict[home]['title']})
    if 'sex' in data_dict:
        data_dict.update({'sex': const.sex_id[data_dict['sex']]})
    if 'relation' in data_dict:
        data_dict.update({'relation': const.relation_id[data_dict['relation']]})
    if 'personal' in data_dict and 'political' in data_dict['personal']:
        data_dict['personal'].update({'political': const.political_id[data_dict['personal']['political']]})
    if 'personal' in data_dict and 'people_main' in data_dict['personal']:
        data_dict['personal'].update({'people_main': const.people_main_id[data_dict['personal']['people_main']]})
    if 'personal' in data_dict and 'life_main' in data_dict['personal']:
        data_dict['personal'].update({'life_main': const.life_main_id[data_dict['personal']['life_main']]})
    if 'personal' in data_dict and 'smoking' in data_dict['personal']:
        data_dict['personal'].update({'smoking': const.smoking_alcohol_id[data_dict['personal']['smoking']]})
    if 'personal' in data_dict and 'alcohol' in data_dict['personal']:
        data_dict['personal'].update({'alcohol': const.smoking_alcohol_id[data_dict['personal']['alcohol']]})
    if 'graduation' in data_dict and data_dict['graduation'] == 0:
        data_dict.pop('graduation')
    for info in const.useless_info:
        if info in data_dict:
            data_dict.pop(info)
    for info in const.empty_info:
        if info in data_dict and data_dict[info] == '':
            data_dict.pop(info)
    return data_dict


def main():
    answer = input("Производить сбор информации по Users или собрать id пользователей из Groups?   U | G     : ")
    if answer in const.Use_Group_id:
        group_list = read_id('group_id.txt')
        parsed = []
        filtered = []
        for group in group_list:
            parsed = parsed + parse_group_member_ids(group)
        for user in parsed:
            if user not in filtered:
                filtered.append(user)
        with open('users_id.txt', 'w') as f:
            for line in filtered:
                f.write(str(line) + '\n')
        print('id пользователей из указанных групп собраны.')
        main()
    elif answer in const.Use_Users_id:
        start_time = time.time()
        parse_users_data()
        pars_users_posts()
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        print("Некорректный запрос.")
        main()

if __name__ == '__main__':
        main()
