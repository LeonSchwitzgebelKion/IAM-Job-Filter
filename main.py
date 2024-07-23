import subprocess
import os
import sys

# Pfad zum `bin` Ordner und `requirements_checker.py`
#bin_folder = os.path.join(os.path.dirname(__file__), 'bin')
#requirements_checker_path = os.path.join(bin_folder, 'requirements.py')

# Führe das `requirements_checker.py` Skript aus
subprocess.check_call([sys.executable, requirements_checker_path])

# Der Rest des Hauptskripts
import pandas as pd
import re
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk

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
        
        # Update progress
        progress = int((i + 1) / total_files * 100)
        progress_var.set(progress)
        root.update_idletasks()

    return results

# Load patterns from the file
patterns_file_path = 'patterns.txt'
patterns = load_patterns(patterns_file_path)

# Set up the GUI
root = tk.Tk()
root.title("Progress")
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, expand=1, padx=20, pady=20)

# Process files and update progress bar
input_dir = 'input'
results = process_files(input_dir, patterns)

# Create a DataFrame from the results
results_df = pd.DataFrame(results, columns=["Job_ID", "Task_ID"])

# Create a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Generate the name for the output file with timestamp
output_filename = f"output_{timestamp}.xlsx"

# Save the results to the output file
results_df.to_excel(output_filename, index=False)

# Show completion message and close GUI after a short delay
completion_label = tk.Label(root, text=f"Completed! Results saved to {output_filename}")
completion_label.pack(pady=10)
root.update_idletasks()
root.after(3000, root.destroy)  # Close the window after 3 seconds

root.mainloop()
