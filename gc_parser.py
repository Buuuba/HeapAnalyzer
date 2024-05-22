import re
import json
import sys

def parse_gc_log(input_file, output_file):
    gc_data = []

    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Regex pattern to extract relevant information
    log_pattern = re.compile(
        r'(?P<timestamp>[\d\-T\:\.\+\d]+).*?GC pause \((?P<GC_name>.*?)\).*?'
        r'\[Eden: (?P<eden_before>\d+\.\d+)M.*?\->(?P<eden_after>\d+\.\d+)M.*?'
        r'Survivors: (?P<survivors_before>\d+\.\d+)K.*?\->(?P<survivors_after>\d+\.\d+)K.*?'
        r'Heap: (?P<heap_before>\d+\.\d+)M.*?\->(?P<heap_after>\d+\.\d+)M'
    )

    for line in lines:
        match = log_pattern.search(line)
        if match:
            timestamp = match.group('timestamp')
            GC_name = match.group('GC_name')
            eden_before = float(match.group('eden_before'))
            eden_after = float(match.group('eden_after'))
            survivors_before = float(match.group('survivors_before')) / 1024  # Convert KB to MB
            survivors_after = float(match.group('survivors_after')) / 1024  # Convert KB to MB
            heap_before = float(match.group('heap_before'))
            heap_after = float(match.group('heap_after'))

            gc_data.append({
                "timestamp": timestamp,
                "eden_size": eden_before,
                "survivors_size": survivors_before,
                "heap_size": heap_before,
                "GC_name": GC_name,
                "phase": "before"
            })

            gc_data.append({
                "timestamp": timestamp,
                "eden_size": eden_after,
                "survivors_size": survivors_after,
                "heap_size": heap_after,
                "GC_name": GC_name,
                "phase": "after"
            })

    if not gc_data:
        print("No matching entries found in the log file.")

    with open(output_file, 'w') as outfile:
        for entry in gc_data:
            json.dump(entry, outfile)
            outfile.write('\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gc_parser.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    parse_gc_log(input_file, output_file)
