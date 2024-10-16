import pandas as pd
import requests
from pathlib import Path
from tqdm import tqdm
import os

def download_pdfs(pdf_links, target_folder):
    """
    Downloads each PDF from a list of PDF links into a specified folder.
    
    Args:
    pdf_links (list): A list of URLs pointing to the PDF files.
    target_folder (str): The directory where PDFs should be saved.
    """
    # Create a directory to save the PDFs if it doesn't exist
    Path(target_folder).mkdir(parents=True, exist_ok=True)
    
    # Download each PDF
    for url in tqdm(pdf_links):
        # Extract filename from URL
        filename = url.split('/')[-1]
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(Path(target_folder) / filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {url}")

def rename_pdfs(df, pdf_directory):
    unmatched_files = []

    count = 1
    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        print(f"Processing link: {count}")
        # Extract the designation and the corresponding link (to match with the filename)
        title = row['Title']
        link = row['Link']
        
        # Extract the PDF filename from the link (assuming it's the last part of the URL)
        pdf_filename_from_link = link.split('/')[-1]
        
        match_found = False
        
        # Find the corresponding PDF file in the directory
        for filename in os.listdir(pdf_directory):
            if pdf_filename_from_link in filename:
                # Construct the new filename
                new_filename = f"{title}.pdf"
                
                # Rename the file
                old_file_path = os.path.join(pdf_directory, filename)
                new_file_path = os.path.join(pdf_directory, new_filename)
                os.rename(old_file_path, new_file_path)
                
                print(f"Renamed '{filename}' to '{new_filename}'")
                match_found = True
                break
        if not match_found:
            unmatched_files.append(pdf_filename_from_link)

        count += 1

    if unmatched_files:
        print("\nThe following files were not matched and renamed:")
        for unmatched in unmatched_files:
            print(unmatched)
    else:
        print("\nAll files were matched and renamed successfully.")

def process_pdfs(df):
    # Filter and prepare links
    links = df["Link"].to_list()
    links = [link.lower() for link in links if isinstance(link, str)]
    links = [link for link in links if (link.endswith('.pdf') and "filenotavailable" not in link)]

    # Download PDFs
    target_folder = 'data/gtmo_pdfs'
    download_pdfs(links, target_folder)

    # Rename PDFs
    rename_pdfs(df, target_folder)

if __name__ == "__main__":
    df = pd.read_csv("data/mc_docket.csv")
    process_pdfs(df)