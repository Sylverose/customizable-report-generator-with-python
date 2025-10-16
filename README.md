# Custom Dynamic Report Generator with Python and MySQL

This is a report on product sales, sorted descending by latest purchase. They present a join between 2 tables. 
- The rows are split dynamically on the pages
- All colors are fully customizable
- Report date is generation date
- Alternative row coloring, so you are welcome to edit those too
- Custom font you can replace with your own
- Stamp (overlay) with logo, which can also be adjusted by coordinate, size and opacity into watermark

It runs a script to generate the report, then you run another one to stamp the logo over.

## Challenges and solutions

1. Joining the orders and products tables in order to extract product names and prices.
2. Printing rows to PDF has to include a dynamic splitting of rows by page, else any adjustments of coordinates will push the remaining rows on a last page. This poses a problem for other dynamic operations, such as adding a logo on all pages (the final one will not be counted as a page.)
3. I made a separate script that you must run, in order to stamp (overlay) a graphic file, with the intention that this will be a logo or a watermark. It is entirely adjustable in page positioning, size and opacity. The file can be replaced in the logo folder.
4. A lot of debugging was necessary for the logo placement, as well as correct rows display. Do consider to add a red stroke around your graphic element, and enlarge it, in case it doesn't show at all on the report. 
5. Finally, I enjoyed working together with GitHub Copilot. This is my favorite AI tool for pair programming. If you want to use it expertly, make sure to review all lines of code, think critically, and constantly optimize your code. I have made a minimum of 8 formatting checks according to the PEP8 standard, cleaned my code of unnecessary elements, comments and optimized the structure after every single implementation. 
6. The file structure is something that I considered from my experience with financial reporting: connecting to the database, managing database CRUD, report generating, stamping the generated report. This ensures that the product is entirely customizable, while avoiding conflicts, such as logo or watermark display issues.
7. Always remember to add a personal touch, with your target group in mind.

## Setup

1. Clone the repository
2. Create a virtual environment (already done):
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```powershell
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```
4. Install required dependencies (all needed for full functionality):
   ```bash
   pip install mysql-connector-python pandas python-dotenv matplotlib PyPDF2 reportlab
   ```
5. Create a `.env` file in the project root with your MySQL credentials:
   ```env
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_NAME=shop
   ```

## Project Structure

```
├── .venv/              # Virtual environment (not in git)
├── data/              # CSV data files
│   ├── customers.csv  # Customer information
│   ├── products.csv   # Product catalog
│   └── orders.csv     # Order records
├── reports/           # Generated PDF reports
├── logo/              # Company logo for PDF stamping
│   └── company_logo.png  # PNG format required (default); can be replaced with your own logo
├── fonts/             # Custom fonts for PDF reports
│   └── playfair-display.italic.ttf
├── src/               # Source code directory
│   ├── connect.py     # Database connection handling
│   ├── db_manager.py  # DatabaseManager class
│   ├── main.py        # Main application logic
│   ├── generate_report.py  # PDF report generation
│   └── stamp_logo_on_pdf.py  # Logo stamping utility
├── .env              # Environment variables (not in git)
├── .gitignore        # Git ignore file
└── README.md         # This file
```


## DatabaseManager Class

The core logic is encapsulated in the `DatabaseManager` class (`src/db_manager.py`). This class provides a clean interface for all database operations:

- `test_connection()`: Tests the MySQL connection and logs the result.
- `create_tables()`: Drops and recreates the `customers`, `products`, and `orders` tables with the correct schema and foreign keys.
- `import_csv_data()`: Reads the CSV files, removes rows with null values, and imports the data into the database. Handles duplicate keys and data type conversions.
- `verify_data()`: Prints a sample of data from each table to verify successful import.

The class is initialized with the database config, the data directory, and a logger. All database logic is now object-oriented and easy to extend.

## Usage

The project provides functionality to:
1. Connect to MySQL database securely using environment variables
2. Import data from CSV files into existing MySQL tables (the script expects `customers.csv`, `products.csv`, and `orders.csv` in the `data/` folder)
3. Handle data with proper error checking and logging

To run the data import:
```bash
python src/main.py
```

The script will:
1. Test the database connection
2. Import data from CSV files into their respective tables:
   - customers.csv → customers table
   - products.csv → products table
   - orders.csv → orders table

All operations are logged to both console and a `cpy-errors.log` file.

## Generating Reports

To generate a PDF report of product purchases:

```bash
python src/generate_report.py
```


This script will:
- Connect to the MySQL database
- Join the `products` and `orders` tables
- Extract `product_name`, `date_time` (purchase date), and `price`
- Order the results by `date_time` (descending)
- Generate a formatted PDF table in A4 landscape format in the `reports/` folder
- Apply custom styling:
   - Title: "Total purchases report" in #D741A7 color with Playfair Display Italic font
   - Report date in top right corner in #3A1772 color
   - Header row with #3A1772 background and white text
   - Alternate row colors (#ffe6f0 for even rows)
   - Right-aligned prices with 2 decimal places
   - Automatic pagination to fit table rows on each page
- Display a cyan-colored success message with instructions for logo stamping

The report will be saved as `reports/product_purchases_report.pdf`.


**Success Message:**
After generating the report, you'll see a cyan-colored message in the terminal (using ANSI color codes):

```
\033[96mThe report has been generated. You can now run python src/stamp_logo_on_pdf.py to add your company logo or watermark to your report.\033[0m
```


**Requirements:** Make sure `matplotlib` is installed:
```bash
pip install matplotlib
```

## Stamping Logo on Reports

To add the company logo to an existing PDF report:

```bash
python src/stamp_logo_on_pdf.py
```

This script will:
1. Read the existing PDF report (`reports/product_purchases_report.pdf`)
2. Create an overlay with the company logo from `logo/company_logo.png`
3. Stamp the logo on all pages at the top left corner
4. Add a white background behind the logo to cover transparency
5. Save the stamped version as `reports/product_purchases_report_stamped.pdf`
6. Display a cyan-colored success message

**Logo Settings:**
- Size: 60x60 pixels
- Position: 20pt from left edge, 140pt from top edge (to avoid clipping)
- Format: PNG (default, as required by the script) with white background overlay
- Appears on all pages in A4 landscape format


**Success Message:**
After stamping the logo, you'll see a cyan-colored message in the terminal (using ANSI color codes):

```
\033[96mThe report has been stamped. Check the final result in your "reports" folder\033[0m
```


**Requirements:** Make sure `PyPDF2` and `reportlab` are installed:
```bash
pip install PyPDF2 reportlab
```

You can customize logo placement by editing the `LOGO_WIDTH`, `LOGO_HEIGHT`, and position values in `stamp_logo_on_pdf.py`.

**Note:** If you use a different logo file name or format, update the `LOGO_PATH` in `stamp_logo_on_pdf.py` accordingly.

## Code Quality

All Python files in this project follow **PEP8 style guidelines**:
- Proper import ordering (standard library, third-party, local)
- 4 spaces for indentation
- Descriptive variable and function names
- Comprehensive docstrings
- ANSI color codes for terminal output (cyan for success messages)

## Database Schema

The script automatically creates the following table structure in your MySQL database (no need to pre-create tables):

**customers**
- customer_id (INT, Primary Key)
- name (VARCHAR)
- email (VARCHAR)

**products**
- product_id (INT, Primary Key)
- product_name (VARCHAR)
- price (DECIMAL)

**orders**
- order_id (INT, Primary Key)
- date_time (DATETIME)
- customer_id (INT, Foreign Key to customers.customer_id)
- product_id (INT, Foreign Key to products.product_id)

## Error Handling

- Connection issues are automatically retried with exponential backoff
- All errors are logged to both console and file
- Duplicate records are handled with `ON DUPLICATE KEY UPDATE`
- Data type conversions (e.g., timestamps) are handled automatically

## Dependencies

- mysql-connector-python
- pandas
- python-dotenv
- matplotlib (for PDF report generation)
- PyPDF2 (for logo stamping)
- reportlab (for logo stamping)


## Author & Credits

**Author:** Andy Sylvia Rosenvold

**Credits:**
- GitHub Copilot (AI pair programmer)
- MySQL with Python documentation (https://dev.mysql.com/doc/connector-python/en/ and https://pandas.pydata.org/docs/)

## License

GPL-3.0 license

## Notes

- Uses MySQL 8.0.20+ alias syntax for `ON DUPLICATE KEY UPDATE` (future-proof, no deprecation warnings)

- Tables can be created from Python using the included `create_tables()` function in `main.py` (run the script to drop, create, and import in one go)
