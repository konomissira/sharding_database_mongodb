import pandas as pd
import json
import os

INPUT_CSV = os.path.join("data", "cleaned_airbnb_listings.csv")
OUTPUT_JSON = os.path.join("data", "cleaned_airbnb_listings.json")

def convert_csv_to_jsonl():
    df = pd.read_csv(INPUT_CSV)

    # Drop rows with missing neighbourhood
    df = df.dropna(subset=["neighbourhood", "price"])

    with open(OUTPUT_JSON, "w") as f:
        for _, row in df.iterrows():
            json.dump(row.to_dict(), f)
            f.write("\n")

    print(f"Conversion complete. JSONL saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    convert_csv_to_jsonl()
