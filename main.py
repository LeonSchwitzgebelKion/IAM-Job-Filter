'''
Requirements:
pip install pandas
pip install re
pip install datetime
pip install py
'''

import pandas as pd
import re
import os
from datetime import datetime

# Lade die Patterns aus der Datei patterns.txt
patterns_file_path = 'patterns.txt'
with open(patterns_file_path, 'r') as file:
    patterns = [line.strip().replace('*', "([^']*)") for line in file if line.strip()]

# Verzeichnis mit den Eingabedateien
input_dir = 'input'

# Liste zum Speichern der Ergebnisse
results = []

# Gehe durch alle Dateien im Eingabeverzeichnis
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(file_path, quotechar='"', sep=';')

        for index, row in df.iterrows():
            description = row['description']
            for pattern in patterns:
                if re.match(pattern, description):
                    results.append((row['Job_ID'], row['Task_ID']))
                    break

results_df = pd.DataFrame(results, columns=["Job_ID", "Task_ID"])

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

output_path = f"output/filtered_{timestamp}"

results_df.to_excel(output_path + ".xlsx", index=False)
results_df.to_csv(output_path + ".csv", index=False)