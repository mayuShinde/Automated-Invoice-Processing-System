import os
import re
import pandas as pd
from PyPDF2 import PdfReader

PDF_FOLDER = "attachments"

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_key_value_pairs(text):
    pairs = {}
    lines = [line.strip() for line in text.split("\n") if ":" in line]

    for line in lines:
        if re.match(r".+?:\s?.+", line):
            key, value = line.split(":", 1)
            key_clean = re.sub(r"[^A-Za-z0-9 ]+", "", key).strip()
            value_clean = value.strip()
            if key_clean:
                pairs[key_clean] = value_clean

    return pairs


def main():
    data = []

    for filename in os.listdir(PDF_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, filename)
            print(f"Processing: {pdf_path}")

            text = extract_text_from_pdf(pdf_path)
            kv_pairs = extract_key_value_pairs(text)
            data.append(kv_pairs)

    df = pd.DataFrame(data)
    print(df)
    df.to_csv("extracted_data.csv", index=False)

if __name__ == "__main__":
    main()
