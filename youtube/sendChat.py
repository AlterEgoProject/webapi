from youtube import getOAuth

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def send(chatId, msg):
    youtube = getOAuth.get_oauth(scopes)
    request = youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "type": "textMessageEvent",
                "liveChatId": chatId,
                "textMessageDetails": {
                    "messageText": msg
                }
            }
        }
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    chatId = ""
    msg = "APIテスト"
    send(chatId, msg)