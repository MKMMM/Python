import csv
import subprocess
import tkinter as tk
from tkinter import filedialog

# Define the path to the espeak-ng executable
ESPEAK_PATH = "espeak-ng"

# Define the path to the directory where you want to save the .wav files
OUTPUT_DIR = ".\output"

# Define the command to generate a .wav file from text using espeak-ng
ESPEAK_COMMAND = [ESPEAK_PATH, "-v", "en-gb+f3", "-s", "140", "-w", None, None]

# Define the function to execute when the button is clicked
def run_script():
    # Get the path to the input CSV file
    input_path = input_path_var.get()

    # Open the input CSV file
    with open(input_path, "r") as csv_file:
        reader = csv.reader(csv_file)

        # Loop over each row in the input CSV file
        for row in reader:
            # Get the string from the current row
            phrase = row[0]

            # Generate the filename for the current phrase
            filename = phrase.replace(" ", "_") + ".wav"

            # Update the output file path in the espeak-ng command
            ESPEAK_COMMAND[-1] = OUTPUT_DIR + filename

            # Generate the .wav file using espeak-ng
            subprocess.run(ESPEAK_COMMAND + [phrase])

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

# Create the start button
start_button = tk.Button(window, text="Start", command=run_script)
start_button.pack()

# Start the TKinter event loop
window.mainloop()