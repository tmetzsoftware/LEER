import os
import json

def read_lines(filename):
    if not os.path.isfile(filename):
        print(f"Error: {filename} does not exist.")
        return []

    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]

    return lines


def group_strings(lines):
    records = []

    strings = []
    for line in lines:
        if line == "":
            records.append({
                "strings": strings
            })
            strings = []
        else:
            strings.append(line)

    if strings:
        records.append({
            "strings": strings
        })

    return records


def write_output(records, output_file):
    # If the output file exists, load existing data
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file) as file:
            data = json.load(file)
            last_record_number = data[-1]['record_number'] if data else 0
    else:
        data = []
        last_record_number = 0

    # Add a record number to each record
    for i, record in enumerate(records):
        record_number = last_record_number + i + 1
        record['record_number'] = record_number
        record_with_number_first = {"record_number": record_number, "strings": record["strings"]}
        records[i] = record_with_number_first

    # Add the new records to the existing data
    data.extend(records)

    # Write the updated data to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.json"

    lines = read_lines(input_file)
    records = group_strings(lines)
    write_output(records, output_file)
