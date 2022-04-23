from youtube import getOAuth

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get(liveChatId, pageToken=None):
    youtube = getOAuth.get_oauth(scopes)
    if pageToken is None:
        request = youtube.liveChatMessages().list(
            part="snippet",
            liveChatId=liveChatId
        )
    else:
        request = youtube.liveChatMessages().list(
            part="snippet",
            liveChatId=liveChatId,
            pageToken=pageToken
        )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    get("")
