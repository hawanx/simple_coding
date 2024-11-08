from datetime import datetime, timedelta
import re


# Function to adjust the time by a given timedelta
def adjust_time(timestamp, adjustment):
    time_format = "%H:%M:%S,%f"
    original_time = datetime.strptime(timestamp, time_format)
    adjusted_time = original_time - adjustment
    # Check if the adjusted time is negative (less than midnight)
    if adjusted_time < datetime.strptime("00:00:00,000", time_format):
        return None  # Return None for timestamps that should be removed
    return adjusted_time.strftime(time_format)[:-3]  # Remove last 3 characters to match SRT format


# Specify the adjustment time
time_adjustment = timedelta(minutes=55, seconds=4.5)


# Function to process the SRT file
def process_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    section_pattern = re.compile(r"^\d+$")
    time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

    skip_block = False
    for i, line in enumerate(lines):
        if section_pattern.match(line.strip()):
            skip_block = False  # Reset skip flag for new block
            section_number = line.strip()
        elif time_pattern.match(line.strip()):
            match = time_pattern.match(line.strip())
            start_time = adjust_time(match.group(1), time_adjustment)
            end_time = adjust_time(match.group(2), time_adjustment)

            # Set skip flag if either timestamp is invalid
            if not start_time or not end_time:
                skip_block = True
            else:
                new_lines.append(f"{section_number}\n")
                new_line = f"{start_time} --> {end_time}\n"
                new_lines.append(new_line)
        elif not skip_block:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


# Path to the SRT file
file_path = "gg.srt"
process_srt(file_path)

print("Time adjustment completed.")
