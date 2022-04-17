from hashlib import sha256
from json import dumps

import requests

from config import CLIENT_ID, SIGN_KEY, RT_API


class APIRequests:
    HEADERS = {'X-Client-ID': CLIENT_ID}

    def set_header_x_client_sign(self, request_body):
        """
        Метод, формирующий цифровую подпись безопасности и добавляющих эту
        подписаь в заголовок запроса
        """
        sign = (CLIENT_ID + dumps(request_body) + SIGN_KEY).encode('utf-8')
        self.HEADERS['X-Client-Sign'] = sha256(sign).hexdigest()

    def domain_call_history(self, request_body: dict) -> str:
        """ Запрос на выгрузку журнала вызовов домена"""
        # Данный запрос работает и к тестовому и к боевому API.
        # Возвращается валидный order_id
        self.set_header_x_client_sign(request_body)
        uri = f'{RT_API}domain_call_history'

        order_id = requests.post(uri, json=request_body,
                                 headers=self.HEADERS).json()['order_id']
        return order_id

    def download_call_history(self, request_body: dict):
        """Запрос на скачивание журнала вызовов"""
        self.set_header_x_client_sign(request_body)
        uri = f'{RT_API}download_call_history'
        # Данный запрос работает только к тестовому API:
        # https://api-test.cloudpbx.rt.ru/
        # При запросе к боевому API возвращается ошибка 404 nginx
        csv_file = requests.post(uri, json=request_body, headers=self.HEADERS)
        # Здесь должен был вернуться csv файл с историей звонков, но вместо
        # этого возращает json вида:
        # {
        #     "result": "1",
        #     "resultMessage": "Операция выполнена успешно",
        #     "session_id": "5a56aff8-2352-4c94-8778-07cbfb60d242"
        # }

        session_id = csv_file.json()['session_id']

        return session_id, csv_file

    def get_record(self, request_body: dict) -> str:
        """Запрос записи разговора"""
        self.set_header_x_client_sign(request_body)
        uri = f'{RT_API}get_record'
        # Данный запрос работает только к тестовому API
        # https://api-test.cloudpbx.rt.ru/ и возвращает ссылку вида:
        # http://vpbx.server.ru/api/record/download/4ce65f38-f15a-4552-bea1-612bdb5662d9,
        # которая в свою очередь недоступна.
        # При запросе к боевому API возвращается ошибка 404 nginx

        record_link = requests.post(uri, json=request_body,
                                    headers=self.HEADERS).json()['url']

        return record_link


api_requests = APIRequests()
