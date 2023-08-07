import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
import csv
import requests
from time import sleep

subscription_key = '276d33ba6a1c4bfaaa4d5cad5d65c51c'

def get_token(subscription_key):
    fetch_token_url = 'https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token

def convert_text_to_speech(text):
    # Set up the API endpoint and headers
    endpoint = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Content-Type": "application/ssml+xml",
        "Authorization": "Bearer " + str(get_token(subscription_key)),
        "X-Microsoft-OutputFormat": output_formats.get()
    }

    # Make the API request and return the content
    response = requests.post(endpoint, headers=headers, data=text)
    return response.content

def convert_csv_to_speech(csv_file):
    # Open the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Iterate through each row and convert the text to speech
        for row in reader:
            text = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='" + str(voices.get()) + "'>" + row[0] + "</voice></speak>"
            content = convert_text_to_speech(text)
            # Save the speech as a WAV file with the same name as the row
            with open(row[0] + ".wav", "wb") as f:
                f.write(content)
                print("Content: ", text)
            sleep(2)

def browse_file():
    # Open a file dialog to select the CSV file
    file_path = filedialog.askopenfilename()
    # Set the text of the file path label to the selected file path
    file_path_label.config(text=file_path)

def run_script():
    # Get the file path from the file path label
    file_path = file_path_label.cget("text")
    # Convert the CSV file to speech
    convert_csv_to_speech(file_path)

# Create the tkinter window
window = tk.Tk()
window.title("CSV to Speech")
window.geometry("600x480")

# Create the dropdown list for output formats
output_formats = ttk.Combobox(window, values=["riff-8khz-8bit-mono-alaw",
                                            "riff-8khz-8bit-mono-mulaw",
                                            "riff-8khz-16bit-mono-pcm",
                                            "riff-22050hz-16bit-mono-pcm",
                                            "riff-24khz-16bit-mono-pcm",
                                            "riff-44100hz-16bit-mono-pcm",
                                            "riff-48khz-16bit-mono-pcm"])
output_formats.current(4)  # Set default value to riff-24khz-16bit-mono-pcm
output_formats.pack()

# Create the dropdown list for Voices
voices = ttk.Combobox(window, values=[
    "en-US-JennyNeural",
    "en-US-JennyMultilingualNeural",
    "en-US-GuyNeural",
    "en-US-AmberNeural",
    "en-US-AnaNeural",
    "en-US-AriaNeural",
    "en-US-SteffanNeural",
    "en-US-TonyNeural",
    "en-US-AIGenerate1Neural",
    "en-US-AIGenerate2Neural",
    "en-US-RogerNeural",
    "en-GB-LibbyNeural",
    "en-GB-AbbiNeural",
    "en-GB-AlfieNeural",
    "en-GB-BellaNeural",
    "en-GB-ElliotNeural",
    "en-GB-EthanNeural",
    "en-GB-HollieNeural",
    "en-GB-MaisieNeural",
    "en-GB-NoahNeural",
    "en-GB-OliverNeural",
    "en-GB-OliviaNeural",
    "en-GB-RyanNeural",
    "en-GB-SoniaNeural",
    "en-GB-ThomasNeural",
    "en-GB-MiaNeural",
    "en-GB-George",
    "en-GB-Susan",
    "pl-PL-AgnieszkaNeural",
    "pl-PL-MarekNeural",
    "pl-PL-ZofiaNeural",
    "pl-PL-PaulinaRUS"
])
voices.current(12)  # Set default value to AbbiNeural
voices.pack()

# Create the file path label and browse button
file_path_label = tk.Label(window, text="")
file_path_label.pack()
browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack()

# Create the run script and exit buttons
run_button = tk.Button(window, text="Run Script", command=run_script)
run_button.pack()
exit_button = tk.Button(window, text="Exit", command=window.destroy)
exit_button.pack()

# Run the tkinter event loop
window.mainloop()
