import vonage


client = vonage.Client(key="06ae635e", secret="Y1LF72QkECaTOTbE")
sms = vonage.Sms(client)

def send(string):
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "918111817156",
            "text": string,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
