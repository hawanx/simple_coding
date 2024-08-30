from datetime import datetime, timedelta
import re

# Function to adjust the time by reducing 55 minutes and 20 seconds
def adjust_time(timestamp, adjustment):
    time_format = "%H:%M:%S,%f"
    original_time = datetime.strptime(timestamp, time_format)
    adjusted_time = original_time - adjustment
    return adjusted_time.strftime(time_format)[:-3]  # Remove last 3 characters to match SRT format

# Adjustment to subtract 55 minutes and 20 seconds
time_adjustment = timedelta(minutes=55, seconds=5)

# Function to process the SRT file
def process_srt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    section_number = 1
    section_pattern = re.compile(r"^\d+$")
    time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
    skip_section = False

    for line in lines:
        if section_pattern.match(line.strip()):
            original_section_number = int(line.strip())
            if original_section_number < 370:
                skip_section = True
            else:
                skip_section = False
                new_lines.append(f"{section_number}\n")
                section_number += 1
        elif time_pattern.match(line.strip()) and not skip_section:
            match = time_pattern.match(line.strip())
            start_time = adjust_time(match.group(1), time_adjustment)
            end_time = adjust_time(match.group(2), time_adjustment)
            new_line = f"{start_time} --> {end_time}\n"
            new_lines.append(new_line)
        elif not skip_section:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Path to the SRT file
file_path = "gg.srt"
process_srt(file_path)

print("Time adjustment and section filtering completed.")
