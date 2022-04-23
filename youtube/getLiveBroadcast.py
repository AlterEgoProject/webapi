from youtube import getOAuth

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get():
    youtube = getOAuth.get_oauth(scopes)
    request = youtube.liveBroadcasts().list(
        part="snippet",
        broadcastStatus="active"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    get()
