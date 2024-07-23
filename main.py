import os
import pandas as pd
import re
from datetime import datetime

def load_patterns(patterns_file_path):
    with open(patterns_file_path, 'r') as file:
        return [line.strip().replace('*', "([^']*)") for line in file if line.strip()]

def process_files(input_dir, patterns):
    results = []

    # Get all CSV files in the input directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    total_files = len(files)
    
    for i, filename in enumerate(files):
        file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(file_path, quotechar='"', sep=';')

        for index, row in df.iterrows():
            description = row['description']
            for pattern in patterns:
                if re.match(pattern, description):
                    results.append((row['Job_ID'], row['Task_ID']))
                    break
        
        # Print progress to console
        progress = int((i + 1) / total_files * 100)
        print(f"Processing file {i + 1}/{total_files} ({progress}%)")

    return results

# Load patterns from the file
patterns_file_path = 'patterns.txt'
patterns = load_patterns(patterns_file_path)

# Print start time
start_time = datetime.now()
print(f"Start processing at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Process files and update progress in the console
input_dir = 'input'
results = process_files(input_dir, patterns)

# Create a DataFrame from the results
results_df = pd.DataFrame(results, columns=["Job_ID", "Task_ID"])

# Create a timestamp for the output file
timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# Define output file paths
output_path_xlsx = f"output/{timestamp}/filtered_data.xlsx"
output_path_csv = f"output/{timestamp}/filtered_data.csv"

# Save results to Excel and CSV
results_df.to_excel(output_path_xlsx, index=False)
results_df.to_csv(output_path_csv, index=False)

# Print end time and output file locations
end_time = datetime.now()
print(f"Processing completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Results saved to: {output_path_xlsx}")
print(f"Results saved to: {output_path_csv}")

# Wait for user input before closing
input("Press Enter to close...")
