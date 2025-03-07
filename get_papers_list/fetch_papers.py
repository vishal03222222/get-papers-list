import requests
from typing import List, Dict
from datetime import datetime

def fetch_papers(query: str) -> List[Dict]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 1000
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch papers from PubMed")
    
    data = response.json()
    id_list = data.get("esearchresult", {}).get("idlist", [])
    
    papers = []
    for paper_id in id_list:
        paper_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        paper_params = {
            "db": "pubmed",
            "id": paper_id,
            "retmode": "json"
        }
        paper_response = requests.get(paper_url, params=paper_params)
        if paper_response.status_code == 200:
            paper_data = paper_response.json()
            papers.append(paper_data.get("result", {}).get(paper_id, {}))
    
    return papers