from vk_api import *
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_token, my_vk_id, tg_token, my_tg_id
import telebot
import time

vk_session = VkApi(token=vk_token)
vk = vk_session.get_api()

# telebot для пересылки сообщений в телеграм
client = telebot.TeleBot(tg_token)


def send_message(user_id, message, message_id):
    vk.messages.send( user_id=user_id, message=message, random_id=message_id)
    print('ответ: ' + message)


# основной цикл
while True:
    try:
        for event in VkLongPoll(vk_session).listen():
            # если приходит сообщение
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                user_data = vk.users.get(user_id = user_id)
                user = user_data[0]['first_name'] + ' ' + user_data[0]['last_name'] + ' | ' + str(user_data[0]['id'])
                date = str(time.asctime())

                if msg != '' and user_id != my_vk_id:
                    print('\n' + user + ' | ' +  date)
                    print(msg)
                    send_message(user_id, 'сообщение перислано пользователю', get_random_id())
                    # пересылка сообщения в телеграм
                    client.send_message(my_tg_id, 'перислано от: ' + user + '\n' + msg)
                else:
                    send_message(user_id, 'я могу обрабатывать только текстовые сообщения', get_random_id())

    except:
        time.sleep(5)
        print('Error ' + time.asctime())




