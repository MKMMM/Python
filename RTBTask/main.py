from lxml import etree
from lxml.builder import E
import json
from datetime import datetime
import pytz
from tqdm import tqdm
import psutil


# Pretty colors for global use :)
# Adding these tags around output strings changes console colors
CEND = '\33[0m'
CRED = '\33[31m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'


# Boolean check if the offer is active based on the requirements
def is_offer_active(opening_times_json):

    # Parse the JSON content
    opening_times = json.loads(opening_times_json)

    # Get current UTC time and convert to the timezone specified in the JSON
    utc_now = datetime.utcnow()
    timezone = pytz.timezone(opening_times.get("timezone", "UTC"))
    local_now = utc_now.astimezone(timezone)

    # Get today's weekday (1 - Monday, 7 - Sunday)
    weekday = local_now.isoweekday()

    # Check if there are opening times for today (Tricky :PPPP)
    if str(weekday) in opening_times:
        for period in opening_times[str(weekday)]:
            opening_time = datetime.strptime(period['opening'], '%H:%M').time()
            closing_time = datetime.strptime(period['closing'], '%H:%M').time()

            # Checking if offer is considered 'active'
            if opening_time <= local_now.time() <= closing_time:
                return True
    return False


# Custom serializer
def cdata_serialize(elem):

    # Wraps text in CDATA for all tags
    for subelement in elem.iter():
        if subelement.text:
            subelement.text = etree.CDATA(subelement.text)
    return etree.tostring(elem, encoding='utf-8')


def process_xml_file(input_data, output_data):

    # Define context for the stream
    context = etree.iterparse(input_data, events=('end',), tag='offer')

    active_counter = 0
    paused_counter = 0

    with open(output_data, 'wb') as output:
        output.write(b'<root>')

        # Start the process using tqdm for progress
        for event, offer in tqdm(context, desc="Processing Offers"):

            # Parsing JSON for opening times
            opening_times_json = offer.find('opening_times').text
            active_status = is_offer_active(opening_times_json)

            # Add is_active child node
            is_active = E('is_active', str(active_status).lower())

            # Add the is_active element to the offer
            offer.append(is_active)

            # Update counters
            if active_status:
                active_counter += 1
            else:
                paused_counter += 1

            # Serialize the offer with CDATA sections and write to file
            offer_xml = cdata_serialize(offer)
            output.write(offer_xml)

            # Clear the offer element to free memory
            offer.clear()
            while offer.getprevious() is not None:
                del offer.getparent()[0]

        output.write(b'\n</root>')

    return active_counter, paused_counter


# Define file paths
input_file = "C:\\dev\\Data\\RTB\\feed.xml"
output_file = "C:\\dev\\Data\\RTB\\feed_out.xml"

# Start processing data
print(CYELLOW + "Starting..." + CEND)

# Start the timer and get the initial memory usage
start_time = datetime.now()
process = psutil.Process()
initial_memory = process.memory_info().rss / (1024 * 1024)  # Convert to Megabytes

active_count, paused_count = process_xml_file(input_file, output_file)

# End the timer and get the final memory usage
end_time = datetime.now()
final_memory = process.memory_info().rss / (1024 * 1024)  # Convert to Megabytes
elapsed_time = end_time - start_time
memory_used = final_memory - initial_memory

# Output some neat information
print("Active Offers: " + CGREEN + f"{active_count}" + CEND)
print("Paused Offers: " + CGREEN + f"{paused_count}" + CEND)
print("Processing completed in: " + CBLUE + f"{elapsed_time}" + CEND)
print("Approximate memory used: " + CBLUE + f"{memory_used}" + "MB" + CEND)
print("Modified XML file saved to: " + CVIOLET + f"{output_file}" + CEND)
