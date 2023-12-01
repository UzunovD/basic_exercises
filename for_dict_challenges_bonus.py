"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime

import lorem


def generate_chat_history():
    messages_amount = random.randint(200, 1000)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice(
                [
                    None,
                    (
                        random.choice([m["id"] for m in messages])
                        if messages else None
                    ),
                ],
            ),
            "seen_by": random.sample(users_ids,
                                     random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


class Statistic:
    def __init__(self):
        self.msgs = {}  # словарь всех сообщений {msg_id: msg}
        self.num_msg_by_sender_user_id = {}  # количество сообщений по отправителям
        self.most_common_sender_user_id = {'user_id': 0, 'cnt': 0}  # user_id, который написал больше всех сообщений
        self.num_msg_reply_by_source_msg_id = {}  # кол-во ответов на сообщения по id исходного сообщения
        self.num_msg_reply_by_source_msg_user_id = {}  # кол-во ответов на сообщения по user_id исходного сообщения
        self.most_common_msg_reply_user_id = {'user_id': 0, 'cnt': 0}  # user_id, на сообщения которого больше всего ответов
        self.uniq_user_seen_by_user_id = {}  # уникальные user_id просмотревших сообщение по user_id автора исходного сообщения
        self.num_uniq_user_seen_by_user_id = {}  # кол-во уникальных просмотров по user_id автора просмотренных сообщений
        self.most_common_uniq_user_seen_by_user_id = {'user_id': 0, 'cnt': 0}  # user_id, с наибольшим числом уникальных просмотров
        self.num_msg_by_time = {'утром': 0, 'днем': 0, 'вечером': 0}  # распределение сообщений по времени
        self.most_common_msg_by_time = {'time': '', 'cnt': 0}  # самое популярное время отправки

    def collect_statistics(self, msg: dict):
        self.msgs[msg['id']] = msg
        sent_by_user_id = msg['sent_by']

        self.count_by_sender(sent_by_user_id)

        if msg['reply_for']:
            self.count_by_reply(msg)

        self.count_by_uniq_seen(msg, sent_by_user_id)

        self.count_by_time(msg)

    def count_by_sender(self, sent_by_user_id: int):
        """
        Собирает статистику по количеству отправленных сообщений по авторам сообщений и
        находит айди пользователя, который написал больше всех сообщений

        :param sent_by_user_id:
        :return:
        """
        self.num_msg_by_sender_user_id.setdefault(sent_by_user_id, 0)
        self.num_msg_by_sender_user_id[sent_by_user_id] += 1
        if self.num_msg_by_sender_user_id[sent_by_user_id] > self.most_common_sender_user_id['cnt']:
            self.most_common_sender_user_id['user_id'] = sent_by_user_id
            self.most_common_sender_user_id['cnt'] = self.num_msg_by_sender_user_id[sent_by_user_id]

    def count_by_reply(self, msg):
        """
        Собирает статистику по ответам и находит айди пользователя, на сообщения которого больше всего отвечали

        :param msg:
        :return:
        """
        self.num_msg_reply_by_source_msg_id.setdefault(msg['reply_for'], 0)
        self.num_msg_reply_by_source_msg_id[msg['reply_for']] += 1
        user_id_msg_source = self.msgs[msg['reply_for']]['sent_by']
        self.num_msg_reply_by_source_msg_user_id.setdefault(user_id_msg_source, 0)
        self.num_msg_reply_by_source_msg_user_id[user_id_msg_source] += 1
        if self.num_msg_reply_by_source_msg_user_id[user_id_msg_source] > self.most_common_msg_reply_user_id['cnt']:
            self.most_common_msg_reply_user_id['user_id'] = user_id_msg_source
            self.most_common_msg_reply_user_id['cnt'] = self.num_msg_reply_by_source_msg_user_id[user_id_msg_source]

    def count_by_uniq_seen(self, msg, sent_by_user_id):
        """
        Собирает статистику пользователей, сообщения которых видело больше всего уникальных пользователей

        :param msg:
        :param sent_by_user_id:
        :return:
        """
        self.uniq_user_seen_by_user_id.setdefault(sent_by_user_id, set())
        self.uniq_user_seen_by_user_id[sent_by_user_id].update(msg['seen_by'])

    def count_by_time(self, msg: dict):
        """
        Собирает статистику по времени и определяет когда в чате больше всего сообщений

        :param msg:
        :return:
        """
        if msg['sent_at'].time() <= msg['sent_at'].time().replace(hour=12, minute=00):
            self.num_msg_by_time.setdefault('утром', 0)
            self.num_msg_by_time['утром'] += 1
            if self.num_msg_by_time['утром'] > self.most_common_msg_by_time['cnt']:
                self.most_common_msg_by_time['time'] = 'утром'
        elif msg['sent_at'].time() >= msg['sent_at'].time().replace(hour=18, minute=00):
            self.num_msg_by_time.setdefault('вечером', 0)
            self.num_msg_by_time['вечером'] += 1
            if self.num_msg_by_time['вечером'] > self.most_common_msg_by_time['cnt']:
                self.most_common_msg_by_time['time'] = 'вечером'
        else:
            self.num_msg_by_time.setdefault('днем', 0)
            self.num_msg_by_time['днем'] += 1
            if self.num_msg_by_time['днем'] > self.most_common_msg_by_time['cnt']:
                self.most_common_msg_by_time['time'] = 'днем'


if __name__ == "__main__":
    messages = generate_chat_history()
    print(messages)
    st = Statistic()

    for message in messages:
        st.collect_statistics(message)

    print(f'id пользователя, который написал больше всех сообщений - {st.most_common_sender_user_id["user_id"]}')
    print(f'id пользователя, на сообщения которого больше всего отвечали - {st.most_common_msg_reply_user_id["user_id"]}')
    most_uniq_seen_user_ids = sorted(st.uniq_user_seen_by_user_id.items(), key=lambda item: len(item), reverse=True)
    print('id пользователей, сообщения которых видело больше всего уникальных пользователей в невозрастающем порядке: '
          f'{", ".join([str(u[0]) for u in most_uniq_seen_user_ids][:3])}')
    print(f'В чате больше всего сообщений {st.most_common_msg_by_time["time"]}')
    most_long_tread_start = sorted(st.num_msg_reply_by_source_msg_id.items(), key=lambda item: len(item), reverse=True)
    print('Идентификаторы сообщений, которые стали началом для самых длинных тредов в невозрастающем порядке: '
          f'{", ".join([str(m_id[0]) for m_id in most_long_tread_start][:3])}')
