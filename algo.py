from datetime import datetime
import math
from random import randrange
from db import BD


def age(b_date):
    if b_date is not None:
        current_datetime = datetime.now()
        date_format = "%d.%m.%Y"
        delta = (current_datetime - datetime.strptime(b_date, date_format))
        return int(math.floor(delta.days / 365))
    else:
        return None


def write_msg(user_id, vk_session, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def get_info(user_id, vk_session):
    info = vk_session.method('users.get', {"user_ids": user_id, "fields": "bdate,sex,city,relation"})
    if len(str(info[0].get('bdate')).split('.')) != 3 and 'city' not in info[0]:
        result_dict = {'age': None, 'sex': info[0].get('sex'),
                       'city': None,
                       'relation': info[0].get('relation')}
    else:
        if len(str(info[0].get('bdate')).split('.')) != 3:
            result_dict = {'age': None, 'sex': info[0].get('sex'),
                           'city': info[0].get('city').get('id'),
                           'relation': info[0].get('relation')}
        else:
            if 'city' not in info[0]:
                result_dict = {'age': age(info[0].get('bdate')), 'sex': info[0].get('sex'),
                               'city': None,
                               'relation': info[0].get('relation')}
            else:
                result_dict = {'age': age(info[0].get('bdate')), 'sex': info[0].get('sex'),
                               'city': info[0].get('city').get('id'),
                               'relation': info[0].get('relation')}
    for key, value in result_dict.items():
        if value is None:
            result_dict[key] = 0  # Обнулим пустые поля
    return result_dict  # Получим всю информацию по пользователю


def search(user_id, count, offset, vk_user_session):
    my_bd = BD()
    while True:
        search_setting = {'count': count, 'offset': offset, 'age_from': 20, 'age_to': 21, 'sex': 2, 'status': 6,
                          'fields': 'bdate'}
        data = ['age', 'sex', 'city', 'relation']
        for param in data:
            if param == 'age' or param == 'sex' or param == 'relation':
                if param == 'age':
                    search_setting['age_from'] = my_bd.get_param_bd(user_id, param) - 1
                    search_setting['age_to'] = my_bd.get_param_bd(user_id, param)
                if param == 'sex':
                    if my_bd.get_param_bd(user_id, param) == '2':
                        search_setting['sex'] = 1
                    else:
                        search_setting['sex'] = 2
                if param == 'relation':
                    pass
            else:
                search_setting[param] = my_bd.get_param_bd(user_id, param)
        res = vk_user_session.method('users.search', search_setting)
        result = {}
        if len(res['items']) == 0:
            offset += 1
        for elem in res['items']:
            if elem['is_closed'] is False:
                age_user = age(elem['bdate'])
                result[str(elem["id"])] = elem["first_name"] + ' ' + elem["last_name"] + ' ' + str(
                    age_user) + ' ' + 'лет'
                my_bd.update_param(user_id, 'offset', offset + 1)
                return result
            else:
                offset += 1
                break


def get_photo(user_id, vk_user_session):
    max_like = {'-1': -1}
    foto_param = {"album_id": "profile", "extended": "1", "photo_sizes": "1", "owner_id": str(user_id)}
    res = vk_user_session.method('photos.get', foto_param)
    for foto in res["items"]:
        if int(foto['likes']['count']) > min(max_like.values()):
            if len(max_like) < 3:
                max_like[str(foto['id'])] = int(foto['likes']['count'])
            else:
                lower = str(min(max_like, key=max_like.get))
                del max_like[lower]
                max_like[str(foto['id'])] = int(foto['likes']['count'])
    for key, val in list(max_like.items()):
        if val == -1:
            del max_like[key]
    return max_like
