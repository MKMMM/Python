# Offer Processing Script

## Overview
This script is designed to process XML files containing offer data. It evaluates whether each offer is currently active based on its opening times and timezones. 
The script then modifies and saves XML data by appending the activity status of each offer and outputs the modified file. 
Additionally, it provides console outputs with color-coded messages for better readability.

## Features
- **Efficient XML Processing:** Uses `lxml` for parsing and modifying XML files.
- **Memory Efficiency:** The script optimizes memory usage by explicitly clearing processed XML elements from memory during the parsing process. This technique prevents memory bloating, especially useful when dealing with large XML files.
- **Timezone Aware:** Parses opening times in different timezones and calculates offer activity accordingly.
- **Progress Tracking:** Utilizes `tqdm` for tracking the progress of file processing.
- **Performance Metrics:** Reports memory usage and processing time upon completion.
- **Color-Coded Console Outputs:** Enhances readability of outputs using predefined color codes.

## Prerequisites
- Python 3

## Installation
1. Copy the script to a folder on your local machine.
2. Navigate to the script's directory.
3. Set up a Python virtual environment:
  ```
  python -m venv venv
  ```
4. Activate the virtual environment:
- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  source venv/bin/activate
  ```
5. Install the required dependencies:
  ```	
  pip install -r requirements.txt
  ```

## Usage
1. Ensure the XML file to be processed is in the same directory as the script. The default input file name is `feed.xml`. Output is provided in the same folder.
2. Run the script:
  ```
  python task.py
  ```
3. The processed file will be saved as `feed_out.xml` in the same directory.

## Functions Description

### `is_offer_active(opening_times_json)`
- **Purpose:** Determines if an offer is active based on its opening times and the current local time in the specified timezone.
- **Parameters:**
  - `opening_times_json`: A JSON string containing the opening times and timezone information for an offer.
- **Returns:** A boolean value (`True` or `False`) indicating whether the offer is currently active.

### `cdata_serialize(elem)`
- **Purpose:** Serializes XML elements, wrapping text nodes in CDATA sections. This is particularly useful for preserving character data in XML documents.
- **Parameters:**
  - `elem`: An XML element to be serialized with CDATA sections.
- **Returns:** A byte string of the serialized XML element.

### `process_xml_file(input_data, output_data)`
- **Purpose:** Processes each 'offer' element in the input XML file, appends its active status, and writes the modified XML to an output file. It also counts and displays the number of active and paused offers.
- **Parameters:**
  - `input_data`: The file path of the input XML file containing offers.
  - `output_data`: The file path where the modified XML file will be saved.
- **Process:**
  - Iterates over each 'offer' element in the input XML file.
  - Determines the activity status of each offer using `is_offer_active`.
  - Appends the 'is_active' element to each offer.
  - Serializes the modified offer using `cdata_serialize`.
  - Writes the serialized offer to the output file.
  - Keeps track of and displays the number of active and paused offers.
- **Returns:** A tuple containing counts of active and paused offers.

## Output
The script outputs the following information:
- Number of active offers.
- Number of paused offers.
- Time taken for processing.
- Approximate memory used during processing.
- Location of the modified XML file.

## Color Codes
The script uses the following color codes in console outputs:
- **Red:** Error messages.
- **Green:** Success messages.
- **Yellow:** Warning or initial messages.
- **Blue:** Informational messages.
- **Violet:** File path information.
