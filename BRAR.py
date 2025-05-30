from bs4 import BeautifulSoup
import csv
import time
import requests
import pandas as pd
from tqdm import tqdm

# Create empty data
all_pmids = []
out = []
# Define URL's to be searched
search_urls = [
    'https://pubmed.ncbi.nlm.nih.gov/?term=bayesian+response+adaptive+randomisation&filter=simsearch1.fha&filter=lang.english&size=200',
    'https://pubmed.ncbi.nlm.nih.gov/?term=bayesian%20response%20adaptive%20randomisation&filter=simsearch1.fha&filter=lang.english&size=200&page=2']

# For each URL, get the pmid so that we can search each paper
for search_url in search_urls:
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    pmids = soup.find_all('span', {'class': 'docsum-pmid'})
    for p in pmids:
        p = p.get_text()
        all_pmids.append(p) if p not in all_pmids else print('Project already in list, skipping')

# For each paper, get details to be scraped into Excel
for pmid in tqdm(all_pmids):
    url = 'https://pubmed.ncbi.nlm.nih.gov/' + pmid
    response2 = requests.get(url)
    soup2 = BeautifulSoup(response2.content, 'html.parser')

    # Initialize data fields
    year = title = authors = abstract = None

    try:
        year = soup2.select('span.cit')[0].text.strip()
    except IndexError:
        print(f"Year not found for PMID: {pmid}")
    try:
        title = soup2.select('h1.heading-title')[0].text.strip()
    except IndexError:
        print(f"Title not found for PMID: {pmid}")

    try:
        authors = soup2.select('div.authors-list')[0].text.strip()
        # Remove numbers and make author string neater
        authors = ''.join([i for i in authors if not i.isdigit()])
        authors = ' '.join(authors.split())
    except IndexError:
        print(f"Authors not found for PMID: {pmid}")

    try:
        abstract = soup2.select('div#abstract.abstract')[0].text.strip()
        # Make abstract string neater
        abstract = ' '.join(abstract.split())
    except IndexError:
        print(f"Abstract not found for PMID: {pmid}")

    # Add to results only if key fields exist
    if any([year, title, authors, abstract]):
        data = {'Authors': authors, 'Year': year, 'Title': title, 'pmid': pmid, 'url': url, 'Abstract': abstract}
        out.append(data)

    time.sleep(1)  # To avoid hitting server too quickly

# Create DataFrame and write to Excel
df = pd.DataFrame(out)
df.to_excel('pubmed_extract_results_BRAR25.xlsx')
