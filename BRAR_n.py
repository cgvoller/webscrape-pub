from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
from tqdm import tqdm

# Search parameters
base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
query = 'bayesian response adaptive randomisation'
num_pages = 5  # Number of pages to search
results_per_page = 200  # max is 200

# URL-encode the query
from urllib.parse import quote_plus
encoded_query = quote_plus(query)

# Collect all PMIDs
all_pmids = []
for page in range(1, num_pages + 1):
    search_url = (
        f'{base_url}?term={encoded_query}'
        f'&filter=simsearch1.fha&filter=lang.english'
        f'&size={results_per_page}&page={page}'
    )

    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pmids = soup.find_all('span', {'class': 'docsum-pmid'})

    for p in pmids:
        p = p.get_text(strip=True)
        if p not in all_pmids:
            all_pmids.append(p)
        else:
            print('PMID already in list, skipping')

    time.sleep(1)  # Be polite to the server

# Scrape individual paper details
out = []
for pmid in tqdm(all_pmids):
    article_url = base_url + pmid
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract fields
    try:
        year = soup.select_one('span.cit').text.strip()
    except:
        year = None

    try:
        title = soup.select_one('h1.heading-title').text.strip()
    except:
        title = None

    try:
        authors = soup.select_one('div.authors-list').text.strip()
        authors = ''.join([i for i in authors if not i.isdigit()])
        authors = ' '.join(authors.split())
    except:
        authors = None

    try:
        abstract = soup.select_one('div#abstract.abstract').text.strip()
        abstract = ' '.join(abstract.split())
    except:
        abstract = None

    if any([year, title, authors, abstract]):
        out.append({
            'Authors': authors,
            'Year': year,
            'Title': title,
            'pmid': pmid,
            'url': article_url,
            'Abstract': abstract
        })

    time.sleep(1)

# Save to Excel
df = pd.DataFrame(out)
df.to_excel('pubmed_extract_results_BRAR25.xlsx', index=False)