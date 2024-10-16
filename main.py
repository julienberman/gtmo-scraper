from src.scraper import scrape_cases
from src.processor import process_pdfs

def main():
    # Scrape cases
    df = scrape_cases()
    df.to_csv("data/gtmo_docket.csv", index=False)
    print("Case information scraped and saved to data/gtmo_docket.csv")

    # Process PDFs
    process_pdfs(df)
    print("PDFs downloaded and processed")

if __name__ == "__main__":
    main()