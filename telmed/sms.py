# sms.py
import math
import requests

def count_sms(message):
    GSM_7BIT_MAX_CHARS = 160
    UNICODE_MAX_CHARS = 70

    total_length = len(message)
    is_unicode = any(ord(char) > 127 or ord(char) <
                     32 or ord(char) == 127 for char in message)

    if is_unicode:
        return math.ceil(total_length / UNICODE_MAX_CHARS)
    else:
        return math.ceil(total_length / GSM_7BIT_MAX_CHARS)


def send_sms(number, msg):
    api_key = "HdTxGTca5R3GheB6ueQn"
    sender_id = "8809604902610"
    url = f"http://bulksmsbd.net/api/smsapi?api_key={api_key}&type=text&number={number}&senderid={sender_id}&message={msg}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Response:")
        print(response.text)
    else:
        print("API request failed with status code:", response.status_code)