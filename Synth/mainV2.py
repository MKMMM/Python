import csv
import subprocess
import tkinter as tk
from tkinter import filedialog

# Define the path to the espeak-ng executable
ESPEAK_PATH = "espeak-ng"

# Define the path to the directory where you want to save the .wav files
OUTPUT_DIR = "C:/dev/Python/Synth/Out/"

# Define the function to generate the ESPEAK_COMMAND based on the selected options
def generate_espeak_command(voice, speed, output_file, phrase):
    espeak_command = [ESPEAK_PATH, "-v", voice, "-s", str(speed), "-w", output_file, str(phrase)]
    return espeak_command

# Define the function to execute when the button is clicked
def run_script():
    # Get the path to the input CSV file
    input_path = input_path_var.get()

    # Get the selected voice and speed options
    voice = voice_var.get()
    speed = speed_var.get()

    # Loop over each row in the input CSV file
    with open(input_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Get the string from the current row
            phrase = row[0]

            # Generate the filename for the current phrase
            filename = phrase.replace(" ", "_") + ".wav"
            output_file = OUTPUT_DIR + filename

            # Generate the espeak command based on the selected options
            espeak_command = generate_espeak_command(voice, speed, output_file, phrase)

            # Generate the .wav file using espeak-ng
            print("Running: ", espeak_command)
            subprocess.run(espeak_command )

    print("Done!")

# Create the TKinter window
window = tk.Tk()
window.title("CSV to WAV Converter")
window.geometry("800x600")
# Create the input file path label and entry
input_path_label = tk.Label(window, text="Input CSV File Path:")
input_path_label.pack()

input_path_var = tk.StringVar()
input_path_entry = tk.Entry(window, textvariable=input_path_var)
input_path_entry.pack()

# Create the file dialog button
def select_input_file():
    input_path_var.set(filedialog.askopenfilename())

select_file_button = tk.Button(window, text="Select File", command=select_input_file)
select_file_button.pack()

# Create the voice options label and radio buttons
voice_label = tk.Label(window, text="Select Voice:")
voice_label.pack()

voice_var = tk.StringVar()
voice_var.set("en-gb+f3")

voice_options = [
    ("British Male", "en-gb+m1"),
    ("British Female", "en-gb+f1"),
    ("American Female", "en-us+f1"),
    ("American Male", "en-us+m1"),
    ("Polish Female", "pl+f1"),
    ("Polish Male", "pl+m1"),
    ("Embrola British Female", "mb-en1"),
    ("Embrola US Female", "mb-us2")
]

for voice_option_text, voice_option_value in voice_options:
    voice_option_radio = tk.Radiobutton(window, text=voice_option_text, variable=voice_var, value=voice_option_value)
    voice_option_radio.pack()

# Create the speed options label and radio buttons
speed_label = tk.Label(window, text="Select Speed:")
speed_label.pack()

speed_var = tk.IntVar()
speed_var.set(140)

speed_options = [
    ("100 words per minute", 100),
    ("120 words per minute", 120),
    ("140 words per minute", 140)
]

for speed_option_text, speed_option_value in speed_options:
    speed_option_radio = tk.Radiobutton(window, text=speed_option_text, variable=speed_var, value=speed_option_value)
    speed_option_radio.pack()

# Create the start button
start_button = tk.Button(window, text="Start", command=run_script)
start_button.pack()

# Start the TKinter event loop
window.mainloop()