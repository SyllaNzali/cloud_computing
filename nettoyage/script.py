import json
import pandas as pd
import glob
import os

# Path to your JSON files
data_path = "data/*.json"

# Get all JSON files
files = glob.glob(data_path)

print(f"Found {len(files)} files")

all_records = []

for file in files:
    print(f"Processing {file}...")

    with open(file) as f:
        data = json.load(f)

        for report in data.get("results", []):
            report_id = report.get("safetyreportid")
            report_date = report.get("receiptdate")
            country = report.get("primarysourcecountry", "unknown")
            severity = report.get("serious", 0)

            drugs = report.get("patient", {}).get("drug", [])
            reactions = report.get("patient", {}).get("reaction", [])

            for drug in drugs:
                drug_name = drug.get("medicinalproduct", "unknown")

                for reaction in reactions:
                    adverse_event = reaction.get("reactionmeddrapt", "unknown")

                    all_records.append({
                        "report_id": report_id,
                        "report_date": report_date,
                        "drug_name": drug_name,
                        "adverse_event": adverse_event,
                        "severity": severity,
                        "country": country
                    })

# Convert to DataFrame
df = pd.DataFrame(all_records)

print("Total rows:", len(df))

# Create result folder if not exists
os.makedirs("result", exist_ok=True)

# Save CSV
output_path = "result/clean_data.csv"
df.to_csv(output_path, index=False)

print(f"✅ CSV saved at {output_path}")


