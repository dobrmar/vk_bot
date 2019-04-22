import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from films import FILMS

def choice_film(choice):
    global FILMS
    f_sort = list(FILMS.keys())
    for i in range(len(choice)):
        f_sort = list(filter(lambda x: choice[i] in FILMS[x][i], f_sort))
    return f_sort

def write_msg(user_id, random_id, message):
    vk.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'message': message})

GENRE = ['драма', 'комедия', 'биография', 'триллер', 'вестерн',
        'приключения', 'криминал', 'детектив', 'фантастика', 'фэнтези',
        'боевик', 'спорт', 'мелодрама', 'военный',
        'мультфильмы', 'мюзикл', 'исторический', 'ужасы', 1]
GENRE_STR = 'Выбери жанр:\n0 - закончить диалог'
for i in range(len(GENRE) - 1):
    GENRE_STR += '\n{} - {}'.format(str(i + 1), GENRE[i])
GENRE_STR += '\n{} - не важно\n\nОтвет напиши числом'.format(str(len(GENRE)))

COUNTRY = ['Франция', 'США', 'Тайвань (Китай)',
          'Великобритания', 'Россия', 'Китай', 'Германия', 1]
COUNTRY_STR = 'Выбери страну:\n0 - закончить диалог'
for i in range(len(COUNTRY) - 1):
    COUNTRY_STR += '\n{} - {}'.format(str(i + 1), COUNTRY[i])
COUNTRY_STR += '\n{} - не важно\n\nОтвет напиши числом'.format(str(len(COUNTRY)))

users = {}

token = "b80d46be1ae3f1fb10cda3ac422c15a3162bf39abbd217ee626d5d75ec8856897b9cfb073eef74cd01d3b"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            if not event.user_id in users:
                users[event.user_id] = [0, []]
            wait = users[event.user_id][0]

            if request == '0':
                del users[event.user_id]
                write_msg(event.user_id, event.random_id, "Удачного просмотра!\nНапиши любое сообщение, если захочешь начать новый диалог")
            elif not wait:
                users[event.user_id][0] = 1
                write_msg(event.user_id, event.random_id, "Привет! Хочешь посмотреть фильм? Пиши '1'")

            elif wait == 1:
                users[event.user_id][0] = 2
                write_msg(event.user_id, event.random_id, COUNTRY_STR)

            elif wait == 2:
                try:
                    i = int(request)
                    if i > 0:
                        users[event.user_id][1].append(COUNTRY[i - 1])
                        users[event.user_id][0] = 3
                        write_msg(event.user_id, event.random_id, GENRE_STR)
                    else:
                        write_msg(event.user_id, event.random_id, "Неверное число!\nПопробуй ещё раз")
                except ValueError:
                    write_msg(event.user_id, event.random_id, "Ответом должно быть число!\nПопробуй ещё раз")
                except IndexError:
                    write_msg(event.user_id, event.random_id, "Неверное число!\nПопробуй ещё раз")

            elif wait == 3:
                try:
                    i = int(request)
                    if i > 0:
                        users[event.user_id][1].append(GENRE[i - 1])
                        users[event.user_id].append(choice_film(users[event.user_id][1]))
                        users[event.user_id].append([])
                        if len(users[event.user_id][2]) == 0:
                            write_msg(event.user_id, event.random_id, 'Извини, подходящих фильмов нет.\n0 - закончить диалог')
                            users[event.user_id][0] = 5
                        else:
                            users[event.user_id][3].append(random.choice(users[event.user_id][2]))
                            write_msg(event.user_id, event.random_id, 'Этот фильм подходит под параметры:\n{}\n\n0 - закончить диалог\n1 - посмотреть другой вариант\n2 - посмотреть все варианты'.format(users[event.user_id][3][-1]))
                            del users[event.user_id][2][users[event.user_id][2].index(users[event.user_id][3][-1])]
                            users[event.user_id][0] = 4
                    else:
                        write_msg(event.user_id, event.random_id, "Неверное число!\nПопробуй ещё раз")
                except ValueError:
                    write_msg(event.user_id, event.random_id, "Ответом должно быть число!\nПопробуй ещё раз")
                except IndexError:
                    write_msg(event.user_id, event.random_id, "Неверное число!\nПопробуй ещё раз")
            elif wait == 4:
                try:
                    i = int(request)
                    if i == 1:
                        if len(users[event.user_id][2]) == 0:
                            write_msg(event.user_id, event.random_id, '0 - закончить диалог\nДругих подходящих фильмов нет')
                            users[event.user_id][0] = 5
                        else:
                            users[event.user_id][3].append(random.choice(users[event.user_id][2]))
                            del users[event.user_id][2][users[event.user_id][2].index(users[event.user_id][3][-1])]
                            write_msg(event.user_id, event.random_id, 'Этот фильм подходит под параметры:\n{}\n\n0 - закончить диалог\n1 - посмотреть другой вариант\n2 - посмотреть все варианты'.format(users[event.user_id][3][-1]))
                    elif i == 2:
                        message = '0 - закончить диалог\n'
                        if len(users[event.user_id][2]) == 0:
                            message += 'Других подходящих фильмов нет'
                        for j in users[event.user_id][2]:
                            message += '\n- {}'.format(j)
                        write_msg(event.user_id, event.random_id, message)
                        users[event.user_id][0] = 5
                except ValueError:
                    write_msg(event.user_id, event.random_id, "Ответом должно быть число!\nПопробуй ещё раз")
