import csv
import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_lookup_table(lookup_file):
    """Read the lookup table into a dictionary with (dstport, protocol) as keys."""
    logging.info(f'Reading lookup table from {lookup_file}')
    lookup_dict = {}
    try:
        with open(lookup_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = (row['dstport'], row['protocol'])
                lookup_dict[key] = row['tag']
        logging.info('Lookup table successfully read')
    except Exception as e:
        logging.error(f'Error reading lookup table: {e}')
    return lookup_dict

def parse_flow_logs(log_file):
    """Parse flow logs and return a list of dictionaries."""
    logging.info(f'Parsing flow logs from {log_file}')
    protocol_mapping = {
        '6': 'tcp',
        '17': 'udp',
        '1': 'icmp'
    }

    data = []
    
    try:
        with open(log_file, 'r') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                if row:  # Skip empty lines
                    row[7] = protocol_mapping.get(row[7], row[7])  # Map protocol number to name
                    data.append({
                        'version': row[0],
                        'account_id': row[1],
                        'eni': row[2],
                        'srcaddr': row[3],
                        'dstaddr': row[4],
                        'srcport': row[5],
                        'dstport': row[6],
                        'protocol': row[7],
                        'packets': row[8],
                        'bytes': row[9],
                        'start': row[10],
                        'end': row[11],
                        'action': row[12],
                        'log_status': row[13]
                    })
        logging.info('Flow logs successfully parsed')
    except Exception as e:
        logging.error(f'Error parsing flow logs: {e}')
    
    return data

def map_tags(flow_logs, lookup_dict):
    """Map flow logs to tags using a lookup dictionary and count occurrences."""
    logging.info('Mapping tags and counting occurrences')
    tag_counts = Counter()
    port_protocol_counts = Counter()
    
    for log in flow_logs:
        key = (log['dstport'], log['protocol'])
        tag = lookup_dict.get(key, 'Untagged')
        tag_counts[tag] += 1
        port_protocol_counts[key] += 1
    
    logging.info('Tag mapping and counting completed')
    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    """Write tag counts and port/protocol combination counts to the output file."""
    logging.info(f'Writing output to {output_file}')
    try:
        with open(output_file, 'w') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag, count in tag_counts.items():
                file.write(f"{tag},{count}\n")
            
            file.write("\nPort/Protocol Combination Counts:\n")
            file.write("Dstport,Protocol,Count\n")
            for (dstport, protocol), count in port_protocol_counts.items():
                file.write(f"{dstport},{protocol},{count}\n")
        logging.info('Output successfully written')
    except Exception as e:
        logging.error(f'Error writing output: {e}')

def main(flow_log_file, lookup_table_file, output_file):
    """Main function to orchestrate the flow."""
    logging.info('Starting main process')
    
    # Read and prepare data
    flow_logs = parse_flow_logs(flow_log_file)
    lookup_dict = read_lookup_table(lookup_table_file)
    
    # Map tags and count occurrences
    tag_counts, port_protocol_counts = map_tags(flow_logs, lookup_dict)
    
    # Write results to file
    write_output(tag_counts, port_protocol_counts, output_file)
    
    logging.info('Main process completed')

if __name__ == "__main__":
    flow_log_file = "data/input/flow_logs.txt"  # Input flow log file
    lookup_table_file = "data/input/lookup_table.csv"  # Lookup table CSV
    output_file = "data/output/output_combined_counts.csv"  # Output file
    
    main(flow_log_file, lookup_table_file, output_file)