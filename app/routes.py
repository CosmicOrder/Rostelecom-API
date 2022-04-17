from flask import Flask

from app.api_requests import api_requests

app = Flask(__name__)


@app.route('/')
def index():
    # запрос на выгрузку журнала вызовов домена
    request_body_to_upload_the_domain_call_log = {
        'date_start': '2021-10-1 00:00:00',
        'date_end': '2021-10-11 00:00:00',
        'direction': 1,
        'state': 0
    }

    order_id = api_requests.domain_call_history(
        request_body_to_upload_the_domain_call_log)

    # запрос на скачивание журнала вызовов
    request_body_to_download_the_domain_call_log = {
        'order_id': order_id
    }

    session_id, csv_file = api_requests.download_call_history(
        request_body_to_download_the_domain_call_log)

    # запрос ссылки на скачивание записи разговора
    request_for_a_link_to_record_conversations = {
        "session_id": session_id,
        "ip_adress": "76.156.12.39"
    }

    record_link = api_requests.get_record(
        request_for_a_link_to_record_conversations)

    return record_link
