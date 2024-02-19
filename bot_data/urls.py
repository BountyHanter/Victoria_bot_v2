import json
import os

# Получаем путь к текущему файлу
current_file_path = os.path.realpath(__file__)

# Получаем путь к каталогу, в котором находится текущий файл
current_directory = os.path.dirname(current_file_path)

# Создаем путь к файлу 'counter.txt'
counter_file_path = str(os.path.join(current_directory, 'link.json', ))


class Config:
    @property
    def client_url(self):
        with open(counter_file_path, 'r') as f:
            data = json.load(f)
        return data['client_url']


config = Config()


def update_client_url(new_url):
    # Открываем файл на чтение, чтобы получить текущие данные
    with open(counter_file_path, 'r') as f:
        data = json.load(f)

    # Обновляем значение client_url
    data['client_url'] = new_url

    # Открываем файл на запись, чтобы сохранить обновленные данные
    with open(counter_file_path, 'w') as f:
        json.dump(data, f)


dev_url = 'https://b24-idzi0o.bitrix24.ru/rest/1/2k2rrk0gfqyb4by2/'
# Теперь, когда вы обращаетесь к config.client_url, программа автоматически читает значение из JSON файла
result_url = config.client_url
urls = {
    'contact_add': result_url + 'crm.contact.add',
    'company_add': result_url + 'crm.company.add',
    'deal_add': result_url + 'crm.deal.add',
    'comment_add': result_url + 'crm.timeline.comment.add'
}