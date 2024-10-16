# GTMO Case Scraper and Processor
This project scrapes case information from the Military Commissions website and processes the associated PDF files.

## Setup

Clone this repository:
https://github.com/julien/gtmo_docket.git

Create a virtual environment and activate it.

Install the required packages:
Copypip install -r requirements.txt


## Usage

Run the main script, main.py. This will scrape the case information, download the PDFs, and process them.


## Project Structure

src/scraper.py: Contains the web scraping logic
src/processor.py: Contains the PDF processing logic
data/gtmo_pdfs/: Directory where PDFs are stored
main.py: Main script to run the scraper and processor

Notes
1) Ensure you have Chrome installed, as the scraper uses Chrome WebDriver.
2) The scraper may take some time to run, depending on the number of cases and your internet connection.