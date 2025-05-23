import httpx

def send_notification(judul):
    token = "azy34pcfkef4pr489wq5d4w7nyfe8z"
    user_key = "u52wtnz8ouv4k446v1dpgq42jz2ygo"
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": token,
        "user": user_key,
        "message": judul
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = httpx.post(url, data=payload, headers=headers)
    print(f"Notif status: {response.status_code}, Respon: {response.text}")
    return response.status_code
