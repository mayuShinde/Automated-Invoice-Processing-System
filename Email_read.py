import imaplib #connects to email server using IMAP
import email   #parses email massages 
from email.header import decode_header #Decode email headers
import os # for creating and checking files
import getpass # for secure terminal password
import re  # for pattern maching
import pandas as pd  #for creating and saving data in CSV
from PyPDF2 import PdfReader # for reading and extracting text from pdfs

# Configuration
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "mayupawar183@gmail.com"
SUBJECT_KEYWORD = "Invoice"
ATTACHMENT_FOLDER = "attachments"
CSV_OUTPUT_FILE = "extracted_data.csv"

# Connect to Gmail
def connect_to_gmail():
    password = getpass.getpass(f"Enter app password for {EMAIL_ACCOUNT}: ")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER) # create password with IMAP server
    mail.login(EMAIL_ACCOUNT, password) 
    print(" Logged in to Gmail")
    return mail

#Select Inbox Folder
def select_inbox(mail):
    mail.select("inbox")
    print("Inbox selected")

# Search Emails
def search_emails(mail, keyword):
    status, messages = mail.search(None, f'(SUBJECT "{keyword}")') # search email with given keyword
    if status != "OK": 
        print("No messages found.")
        return []
    email_ids = messages[0].split() # get list of email ids from result
    print(f"Found {len(email_ids)} email(s) with subject '{keyword}'")
    return email_ids

# Download PDF Attachments
def download_pdf_attachments(mail, email_ids):
    os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)
    for email_id in email_ids:           # Loop through each email id
        status, data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            print(f"Failed to fetch email {email_id}")
            continue
        msg = email.message_from_bytes(data[0][1]) #convert raw email data into email object 
        print(f"\nProcessing email: {msg['Subject']}") # show mail subject
        for part in msg.walk():              
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()  # Get the attachment’s filename
            if filename and filename.lower().endswith('.pdf'):  # check pdf or not
                filename = decode_header(filename)[0][0]
                if isinstance(filename, bytes):
                    filename = filename.decode()
                    # Clean filename to remove invalid characters
                safe_filename = "".join(c if c.isalnum() or c in (' ', '.', '_') else "_" for c in filename)
                filepath = os.path.join(ATTACHMENT_FOLDER, safe_filename)

                if not os.path.isfile(filepath):   # save pdf
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded: {filepath}")
    print("All attachments downloaded.")

# Extract Text from PDFs
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)  # Open the PDF using PyPDF2
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text  # Return all extracted text
    except Exception as e:
        print(f" Failed to read {pdf_path}: {e}")  # Print error if PDF can’t be read
        return ""  # return empty string

# Extract Key-Value Pairs
def extract_key_value_pairs(text):
    pairs = {}  # Dictionary to store key-value pairs
    lines = [line.strip() for line in text.split("\n") if ":" in line] # this will keep lines with only ":"

    for line in lines:  
        # Check if line matches pattern "key: value"
        if re.match(r".+?:\s?.+", line):  
            key, value = line.split(":", 1) # split on : to seprate key and value
            key_clean = re.sub(r"[^A-Za-z0-9 ]+", "", key).strip() # clean by removing non alphanumeric char
            value_clean = value.strip()  # clean by removing extra spaces
            if key_clean:
                pairs[key_clean] = value_clean 

    return pairs    # Return dictionary of key-value pairs

# Process All PDFs and Save to CSV 
def process_pdfs_and_save():
    # Check if the attachments folder exists
    if not os.path.exists(ATTACHMENT_FOLDER):
        print(f"Folder '{ATTACHMENT_FOLDER}' not found.")
        return

    data = []  # List to store key-value pairs from all PDFs
    for filename in os.listdir(ATTACHMENT_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(ATTACHMENT_FOLDER, filename)
            print(f" Extracting from: {pdf_path}")
            text = extract_text_from_pdf(pdf_path) # Extract text from the PDF
            kv_pairs = extract_key_value_pairs(text)# Extract key-value pairs from the text
            if kv_pairs:   # Add pairs to data list if found
                data.append(kv_pairs)

    if data:
        df = pd.DataFrame(data)  # Convert list of dictionaries to a pandas DataFrame
        df.to_csv(CSV_OUTPUT_FILE, index=False) # Save DataFrame to CSV file
        print(f"\nExtracted data saved to {CSV_OUTPUT_FILE}")
    else:
        print("No data extracted from PDFs.")

# === Main ===
def main():
    mail = connect_to_gmail()
    select_inbox(mail)
    email_ids = search_emails(mail, SUBJECT_KEYWORD)
    if email_ids:
        download_pdf_attachments(mail, email_ids)  # Download PDFs and process them
        process_pdfs_and_save()
    else:
        print(" No matching emails found.")
    mail.logout()
    print(" Logged out of Gmail")

if __name__ == "__main__":
    main()
