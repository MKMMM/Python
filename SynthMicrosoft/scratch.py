import requests
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

subscription_key = 'key'


def get_token(subscription_key):
    fetch_token_url = 'https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token


def convert_text_to_speech(text, output_format):
    # Set up the API endpoint and headers
    endpoint = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Content-Type": "application/ssml+xml",
        "Authorization": "Bearer " + str(get_token(subscription_key)),
        "X-Microsoft-OutputFormat": output_format
    }

    # Make the API request and save the response to a file
    response = requests.post(endpoint, headers=headers, data=text)
    with open("output.wav", "wb") as f:
        f.write(response.content)


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            text = f.read()
            output_format = output_formats.get()
            convert_text_to_speech(text, output_format)


# Create the tkinter form
root = tk.Tk()
root.title("Text to Speech Converter")

# Create the dropdown list for output formats
output_formats = ttk.Combobox(root, values=["riff-8khz-8bit-mono-alaw",
                                            "riff-8khz-8bit-mono-mulaw",
                                            "riff-8khz-16bit-mono-pcm",
                                            "riff-22050hz-16bit-mono-pcm",
                                            "riff-24khz-16bit-mono-pcm",
                                            "riff-44100hz-16bit-mono-pcm",
                                            "riff-48khz-16bit-mono-pcm"])
output_formats.current(4)  # Set default value to riff-24khz-16bit-mono-pcm
output_formats.pack()

# Create the "Select File" button
select_file_button = tk.Button(root, text="Select File", command=browse_file)
select_file_button.pack()

# Create the "Exit" button
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

root.mainloop()
