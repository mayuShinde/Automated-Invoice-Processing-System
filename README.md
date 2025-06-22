
# 📄 Automated Invoice Processing System

##  Project Summary
This is a Python project that helps businesses **automatically read invoice PDFs**, get important details like **invoice number, date, amount, and vendor name**, and **save them into Excel or a small database**.

It makes invoice work faster and reduces mistakes that happen when doing everything manually.


##  What Problem Does It Solve?
Businesses often receive **hundreds or thousands of invoice PDFs**. Manually typing their details into Excel or another system takes a lot of time.

This project:
- Automatically reads those PDFs.
- Picks out important details.
- Stores the data in an easy-to-use Excel sheet or a database.
- Helps users keep track of all invoices in one place.


##  Tools and Libraries Used
- **Python** – Main programming language
- **pdfplumber / PyPDF2** – To read PDF files
- **re (Regular Expressions)** – To find invoice number, date, etc.
- **pandas** and **openpyxl** – To handle Excel files
- **SQLite** – To store data in a small database (optional)
- **Tkinter** – To create a simple window for uploading files (optional)
- 

##  Key Features
- Automatically reads and processes invoice PDFs.
- Saves data in Excel or a small database.
- Simple user interface (optional).
- Creates reports to show totals and summaries.
- Helps avoid duplicate or incorrect entries.

---

##  What I Learned
- How to work with PDF files in Python.
- How to use **regex** (regular expressions) to pull out important text.
- How to use **Excel and databases** with Python.
- How to build a **basic user interface**.
- How to organize a full project step-by-step.

---

##  Future Ideas
- Connect directly to email to fetch invoices.
- Support scanned image invoices using OCR.
- Build a web version of this app using **FastAPI**.
- Add login for different users.

---

##  How to Run This Project

1. Put your invoice PDFs into the `invoices` folder.
2. Run the Python script (`main.py`) to process them.
3. Check the output in `extracted_data.xlsx`.
4. (Optional) Use the GUI to upload files and track them.

---

##  Folder Structure
invoice_project/
├── invoices/ # Where you keep your PDFs
├── extracted_data.xlsx # Excel file with results
├── main.py # Main program
├── gui.py # User interface (optional)
├── database.db # Small database (optional)
├── README.md # Project explanation
└── requirements.txt # List of required Python packages

