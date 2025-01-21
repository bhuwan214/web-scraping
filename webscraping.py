import requests
from bs4 import BeautifulSoup
import openpyxl

def scrape_table_to_excel_with_pagination(base_url, output_file="scraped_table.xlsx"):
    try:
        # Initialize an Excel workbook and worksheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Scraped Data"

        # Add headers
        headers = ["SN", "Province", "Local Bodies Name", "District", "Website", "Office Email", "Contact Number"]
        worksheet.append(headers)

        page = 1  # Start with the first page
        sn = 1  # Serial number for rows

        while True:
            # Construct the URL
            url = base_url if page == 1 else f"{base_url}?page={page}"
            print(f"Scraping: {url}")

            # Send an HTTP request to the website
            response = requests.get(url)
            response.raise_for_status()

            # Parse the website's HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the table
            table = soup.find("table")
            if not table:
                print("No table found on this page. Ending pagination.")
                break

            # Extract table rows
            rows = table.find_all("tr")
            if len(rows) <= 1:  # If no meaningful rows are found
                print("No rows found or table is empty. Ending pagination.")
                break

            for row in rows[1:]:  # Skip the header row if it exists
                cells = row.find_all("td")
                row_data = []

                # Add Serial Number (SN)
                row_data.append(sn)

                # Loop through table cells
                for i, cell in enumerate(cells):
                    if i == 4:  # If it's the 5th <td> (index 4)
                        span = cell.find("span")
                        link = span.find("a")["href"] if span and span.find("a") else None
                        row_data.append(link or "")  # Append the link or empty string
                    else:
                        row_data.append(cell.get_text(strip=True))  # Append the cell text

                # Fill remaining columns with empty strings if fewer <td>s are present
                while len(row_data) < len(headers):
                    row_data.append("")

                if row_data:  # Only append rows with data
                    worksheet.append(row_data)
                    sn += 1  # Increment the serial number

            # Move to the next page
            page += 1

        # Save the data to an Excel file
        workbook.save(output_file)
        print(f"Table data successfully scraped and saved to '{output_file}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
base_url = "https://mofaga.gov.np/local-contact"  # Replace with the base URL

scrape_table_to_excel_with_pagination(base_url)






