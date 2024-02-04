import requests
import json
from datetime import datetime
from bot_data.urls import urls
import os


class AddComment:
    """
    id - id клиента который получаем из bitrix_add_contact
    Получаем данные со счётчика, для названия карточки, отправляем данные на сайт, получаем ответ
    Если ответ 200 - прибавляем к счётчику +1 и возвращаем True
    Если получили ошибку - формируется json файл с url, данными и ошибкой и возвращает False
    """
    def __init__(self, comment: str, id: int,):
        self.comment = comment
        self.id = id
        self.url = urls['comment_add']

    def send_request(self):
        data = {
            "fields": {
                "ENTITY_TYPE": f"deal",
                "ENTITY_ID": self.id,
                'COMMENT': f"{self.comment}"
            },
        }
        response = requests.post(self.url, json=data)
        if response.status_code == 200:
            print("Добавлен комментарий в обсуждение с ID " + str(response.json()))
        else:
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"error_{now_str}.json"
            print("Ошибка: " + str(response.json()))
            error_data = {
                "url": self.url,
                "data": data,
                "error": response.json()
            }
            with open(filename, 'w') as f:
                json.dump(error_data, f)
        return True if response.status_code == 200 else False


if __name__ == '__main__':
    # тест
    gg = AddComment('Коммент сделки',141)
    gg.send_request()





