import requests as rq
from config import API

def town_code(town):
    """
        Выдает код города, который используется при API запросе в Яндекс расписаниях, по его названию

        :param town: Название города, для которого нужно получить код.
        :type town: str
        :return: Код города в формате Яндекс.
        :rtype: str

        Пример использования:
            >>> town_code('Москва')
            'c213'
        """
    url = 'https://suggests.rasp.yandex.net/all_suggests'

    params = {
        'part': f'{town}'
    }
    response = rq.get(url, params=params)
    data = response.json()

    return data['suggests'][0]['point_key']

def path(depart_town, arrive_town, date, api=API):
    """
        Получает информацию о маршрутах между двумя городами на указанную дату с использованием API Яндекс.Расписаний.

        :param depart_town: Название города отправления.
        :type depart_town: str
        :param arrive_town: Название города прибытия.
        :type arrive_town: str
        :param date: Дата поездки в формате 'YYYY-MM-DD'.
        :type date: str
        :param api: API-ключ для доступа к Яндекс.Расписаниям. По умолчанию используется глобальная переменная API, которая записана в конфигурационном файле.
        :type api: str
        :return: JSON-объект с информацией о маршрутах.
        :rtype: dict
        :raises Exception: Если запрос к API завершился ошибкой.

        Пример использования:
            >>> path('Москва', 'Санкт-Петербург', '2023-12-25')
            {
                'segments': [...],
                'pagination': {...}
            }
        """
    depart_town_code = town_code(depart_town)
    arrive_town_code = town_code(arrive_town)

    url = 'https://api.rasp.yandex.net/v3.0/search'
    params = {
        'apikey': api,
        'from': depart_town_code,
        'to': arrive_town_code,
        'lang': 'ru_RU',
        'date': date,
        'transfers': 'true'
    }
    response = rq.get(url, params=params)
    data = response.json()
    return data