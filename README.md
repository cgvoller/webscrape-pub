# webscrape-trials
A script to web scrape clinical trials 

# How to use
Edit the py to include the search URLs, excel file name at the bottom and run the script to output an excel file which contains studies/papers relating to your search terms.

## BRAR_n.py 

- Add base URL (e.g., pubmed)
- add query (e.g., bayesian response adaptive)
- Enter number of pages to search
- Results per page (set to 200, this is the max)
- Change name of excel at bottom
- Run = Happy days

# Example queries

Very generic:

query = 'bayesian response adaptive randomisation'

For more specific queries:

query = '"response adaptive randomisation" OR "response-adaptive randomization" OR "response adaptive randomization"'
