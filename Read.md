# Data Scraping from Government Phone Directory Website

## Overview
This project demonstrates how to scrape data from a government phone directory website using Python. The scraped data includes details such as names, phone numbers, email addresses, designations, and office names, and it is saved into an Excel file using the `openpyxl` library.

## Tools and Libraries Used
- **BeautifulSoup**: For parsing HTML and extracting data from the website.
- **Requests**: For sending HTTP requests to fetch the webpage content.
- **openpyxl**: For creating and saving data into Excel files.
- **Python**: Version 3.7 or above is recommended.

## Prerequisites
1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Install the required libraries using `pip`:
   ```bash
   pip install beautifulsoup4 requests openpyxl
   ```

## How It Works
1. **Send HTTP Request**: The script uses the `requests` library to fetch the HTML content of the target website.
2. **Parse HTML Content**: The `BeautifulSoup` library is used to parse and navigate the HTML structure.
3. **Extract Data**: Relevant data fields such as name, phone number, email, etc., are extracted using appropriate CSS selectors or tags.
4. **Save Data to Excel**: The extracted data is saved into an Excel file using the `openpyxl` library.

## Script Details
Below is the structure of the Python script:

### Import Libraries
```python
import requests
from bs4 import BeautifulSoup
import openpyxl
```

### Define Constants
- **Base URL**: The target website's URL.
- **Output File**: Name of the Excel file to save the data.

### Fetch and Parse Data
The script fetches the HTML content using the `requests` library and parses it with `BeautifulSoup`.

### Save Data to Excel
Using `openpyxl`, the extracted data is written to an Excel file with properly formatted headers and rows.

## Example Script
Here is a simplified version of the script:

```python
import requests
from bs4 import BeautifulSoup
import openpyxl

def scrape_phone_directory(base_url, output_file="phone_directory.xlsx"):
    # Create an Excel workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Phone Directory"

    # Define headers
    headers = ["Name", "Mobile", "Email", "Office Phone", "Designation", "Office Name"]
    worksheet.append(headers)

    page = 1

    while True:
        # Fetch the HTML content
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Stopping.")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Find data rows (customize selector based on site structure)
        rows = soup.find_all("div", class_="directory-item")
        if not rows:
            print("No more data found. Stopping.")
            break

        for row in rows:
            name = row.find("h2").text.strip() if row.find("h2") else "N/A"
            mobile = row.find("span", class_="mobile").text.strip() if row.find("span", class_="mobile") else "N/A"
            email = row.find("span", class_="email").text.strip() if row.find("span", class_="email") else "N/A"
            office_phone = row.find("span", class_="office-phone").text.strip() if row.find("span", class_="office-phone") else "N/A"
            designation = row.find("span", class_="designation").text.strip() if row.find("span", class_="designation") else "N/A"
            office_name = row.find("span", class_="office-name").text.strip() if row.find("span", class_="office-name") else "N/A"

            worksheet.append([name, mobile, email, office_phone, designation, office_name])

        page += 1

    # Save the workbook
    workbook.save(output_file)
    print(f"Data successfully saved to {output_file}")

# Run the scraper
scrape_phone_directory("https://example.com/directory")
```

## Usage
1. Update the `base_url` with the URL of the government phone directory website.
2. Customize the CSS selectors (`find` or `find_all`) based on the HTML structure of the website.
3. Run the script using:
   ```bash
   python scraper.py
   ```
4. The extracted data will be saved in `phone_directory.xlsx` in the current directory.

## Important Notes
- **Ethical Scraping**: Ensure you have permission to scrape the website, and comply with its terms of service.
- **Error Handling**: Add error handling for unexpected HTML structures or network issues.
- **Respect Rate Limits**: Use `time.sleep()` between requests to avoid overloading the server.

## License
This project is open-source and available under the MIT License. Use it responsibly!

