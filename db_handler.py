import const
import re

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
    personal_dict = {}
    for home in const.home_title:
        if home in data_dict:
            data_dict.update({home: data_dict[home]['title']})
    if 'sex' in data_dict:
        data_dict.update({'sex': const.sex_id[data_dict['sex']]})
    if 'relation' in data_dict:
        data_dict.update({'relation': const.relation_id[data_dict['relation']]})
    if 'personal' in data_dict:
        personal_dict = data_dict.pop('personal')
    if 'political' in personal_dict:
        data_dict.update({'political': const.political_id[personal_dict['political']]})
    if 'religion' in personal_dict:
        data_dict.update({'religion': personal_dict['religion']})
    if 'people_main' in personal_dict:
        data_dict.update({'people_main': const.people_main_id[personal_dict['people_main']]})
    if 'life_main' in personal_dict:
        data_dict.update({'life_main': const.life_main_id[personal_dict['life_main']]})
    if 'smoking' in personal_dict:
        data_dict.update({'smoking': const.smoking_alcohol_id[personal_dict['smoking']]})
    if 'alcohol' in personal_dict:
        data_dict.update({'alcohol': const.smoking_alcohol_id[personal_dict['alcohol']]})
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
    copy_text = ""
    if 'copy_history' in post:
        copy_history = post.pop('copy_history')
        copy_history = copy_history[0]
        copy_text = copy_history['text']
    if text != "":
        post_id = post.pop('id')
        owner_id = post.pop('owner_id')
        date = datetime.datetime.fromtimestamp(post.pop('date')).strftime('%Y-%m-%d %H:%M:%S')
        text = re.sub('[\n]', '', text)
        coll.save({"id": post_id, "owner_id": owner_id, "date": date, "text": text})
    elif text == "" and copy_text != "":
        post_id = post.pop('id')
        owner_id = post.pop('owner_id')
        date = datetime.datetime.fromtimestamp(post.pop('date')).strftime('%Y-%m-%d %H:%M:%S')
        copy_text = re.sub('[\n]', '', copy_text)
        coll.save({"id": post_id, "owner_id": owner_id, "date": date, "text": text, "copy_text": copy_text})


def db_data_remove():
    client = MongoClient()
    db = client['test']
    coll = db['users']
    coll.remove({})
    coll = db['posts']
    coll.remove({})
