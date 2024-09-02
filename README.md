
# Flow Log Tagging Script

This script processes network flow logs, maps them to predefined tags based on the destination port and protocol, and generates a summary of the occurrences of each tag as well as the occurrences of each port/protocol combination.

## Features

- **Flow Log Parsing**: Reads and parses flow logs from a text file.
- **Tag Mapping**: Maps parsed flow logs to tags using a lookup table.
- **Summary Generation**: Counts the occurrences of each tag and port/protocol combination.
- **Logging**: Provides detailed logging of the script’s execution for easy debugging and monitoring.

## Prerequisites

- Python 3.x
- `scapy` (optional, for extended protocol mapping)

### Installation

1. Clone the repository or download the script.
2. Ensure you have Python 3.x installed.
3. (Optional) Install `scapy` if you need extended protocol mapping:
   ```sh
   pip install scapy
   ```

## Usage

### Files

- **`flow_logs.txt`**: Input file containing flow logs.
- **`lookup_table.csv`**: CSV file containing the lookup table for mapping destination ports and protocols to tags.
- **`output_combined_counts.csv`**: Output file where the results (tag counts and port/protocol combination counts) are written.

### Running the Script

1. Place your `flow_logs.txt` and `lookup_table.csv` files in the directory `data/input`.
2. Run the script:

   ```sh
   python flow_log_tagging.py
   ```

3. The script will generate an `output_combined_counts.csv` file in the `data/output` directory with the following information:
   - **Tag Counts**: The number of times each tag appears in the flow logs.
   - **Port/Protocol Combination Counts**: The number of times each port/protocol combination appears.

### Script Structure

- **`read_lookup_table(lookup_file)`**: Reads the lookup table from the CSV file and returns a dictionary with destination port and protocol as keys.
- **`parse_flow_logs(log_file)`**: Parses the flow logs from the text file and returns a list of dictionaries, each representing a log entry.
- **`map_tags(flow_logs, lookup_dict)`**: Maps flow logs to tags using the lookup dictionary and counts occurrences of each tag and port/protocol combination.
- **`write_output(tag_counts, port_protocol_counts, output_file)`**: Writes the tag counts and port/protocol combination counts to the output file.
- **`main()`**: The main function that orchestrates the flow of the script.

### Logging

The script uses Python's built-in `logging` module to provide detailed logs of its execution. Logs include information on the progress of the script, any errors encountered, and the completion of tasks. Logs are output to the console.

## Example

**Example `flow_logs.txt`**:
```
2 123456789012 eni-12345 192.0.2.1 198.51.100.1 12345 80 6 10 500 1622471182 1622471242 ACCEPT OK
```

**Example `lookup_table.csv`**:
```csv
dstport,protocol,tag
80,tcp,web
443,tcp,secure-web
53,udp,dns
```

**Generated `output_combined_counts.csv`**:
```
Tag Counts:
web,1

Port/Protocol Combination Counts:
80,tcp,1
```

## Contact

For any questions or suggestions, please contact [Vaibhav Jain](mailto:vaibhavj2074@gmail.com).
