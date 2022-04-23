import os
import dotenv
import requests
import re

dotenv.load_dotenv()
channel_id = os.environ['CHANNEL_ID']


def get_keys():
    load_url = f'https://www.youtube.com/channel/{channel_id}/live'
    html = requests.get(load_url)
    match_key = re.search(r'innertubeApiKey":".*?"', html.content.decode())
    apikey = match_key.group().split('"')[2]
    match_key = re.search(r'continuation":".*?"', html.content.decode())
    continuation = match_key.group().split('"')[2]
    return apikey, continuation


def send_post(apikey, continuation):
    url = f'https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key={apikey}'
    body = {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20210126.08.02',
                'timeZone': 'Asia/Tokyo',
                'utcOffsetMinutes': 540,
                'mainAppWebInfo': {
                    'graftUrl': 'https://www.youtube.com/live_chat?continuation=',
                },
            },
            'request': {
                'useSsl': True,
            },
        },
        'continuation': continuation,
    }
    response = requests.post(url, json=body)

    return response


def parse_response(response):
    data = response.json()
    temp = data['continuationContents']['liveChatContinuation']
    continuation = temp['continuations'][0]['invalidationContinuationData']['continuation']  # 公式は timedContinuationData?
    chats = []
    for action in temp.get('actions', []):
        if 'liveChatTextMessageRenderer' not in action['addChatItemAction']['item'].keys():
            continue
        temp_a = action['addChatItemAction']['item']['liveChatTextMessageRenderer']
        chats.append({
            'text': temp_a['message']['runs'][0]['text'],
            'name': temp_a['authorName']['simpleText'],
            'channel': temp_a['authorExternalChannelId'],
            'id': temp_a['id'],
            'timestamp': temp_a['timestampUsec'],
            'isOwner': 'authorBadges' in temp_a.keys(),
        })
    return continuation, chats


def main():
    apikey, continuation = get_keys()
    for _ in range(5):
        print(_)
        response = send_post(apikey, continuation)
        continuation, chats = parse_response(response)
        [print(chat['text']) for chat in chats]


if __name__ == '__main__':
    from time import sleep
    apikey, continuation = get_keys()
    for _ in range(5):
        sleep(3)
        response = send_post(apikey, continuation)
        continuation, chats = parse_response(response)
        [print(chat['text']) for chat in chats]
