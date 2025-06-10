import pandas as pd
import json
import os
import math

INPUT_CSV = os.path.join("data", "cleaned_airbnb_listings.csv")
OUTPUT_JSON = os.path.join("data", "cleaned_airbnb_listings.json")

def convert_nan_to_none(obj):
    """
    Recursively convert NaN values to None in dictionaries.
    """
    if isinstance(obj, dict):
        return {k: convert_nan_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

def convert_csv_to_jsonl():
    df = pd.read_csv(INPUT_CSV)

    # Drop rows with missing neighbourhood and price
    df = df.dropna(subset=["neighbourhood", "price"])

    with open(OUTPUT_JSON, "w") as f:
        for _, row in df.iterrows():
            cleaned = convert_nan_to_none(row.to_dict())
            json.dump(cleaned, f)
            f.write("\n")

    print(f"Conversion complete. JSONL saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    convert_csv_to_jsonl()
