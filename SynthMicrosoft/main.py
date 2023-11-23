import requests

subscription_key = ''


def get_token(subscription_key):
    fetch_token_url = 'https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token

# get_token(subscription_key)

# Set up the API endpoint and headers
endpoint = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
headers = {
    "Content-Type": "application/ssml+xml",
    "Authorization": "Bearer " + str(get_token(subscription_key)),
    "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm"
}

# Set up the text you want to convert to speech
text = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='en-US-JessaRUS'>Hello world!</voice></speak>"

# Make the API request and save the response to a file
response = requests.post(endpoint, headers=headers, data=text)
with open("output.wav", "wb") as f:
    f.write(response.content)



