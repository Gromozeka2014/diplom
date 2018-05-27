import const

from pymongo import MongoClient
import datetime


def db_save_users_data(user_data):
    client = MongoClient()
    db = client['test']
    coll = db['users']
    user_id = user_data.pop('id')
    coll.save({"_id": user_id})
    dict_update(user_data)
    coll.update({"_id": user_id}, user_data)


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


def db_save_users_posts(post):
    client = MongoClient()
    db = client['test']
    coll = db['posts']
    text = post.pop('text')
    if text != "":
        post_id = post.pop('id')
        owner_id = post.pop('owner_id')
        date = datetime.datetime.fromtimestamp(post.pop('date')).strftime('%Y-%m-%d %H:%M:%S')
        coll.save({"id": post_id, "owner_id": owner_id, "date": date, "text": text})