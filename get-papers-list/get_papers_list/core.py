import requests
import pandas as pd
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

def fetch_papers(query: str) -> List[Dict]:
  
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=json"
    response = requests.get(search_url)
    response.raise_for_status()
    paper_ids = response.json()["esearchresult"]["idlist"]
    print(f"Fetched {len(paper_ids)} paper IDs.")
    
   
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(paper_ids)}&retmode=xml"
    response = requests.get(fetch_url)
    response.raise_for_status() 
    try:
        root = ET.fromstring(response.text)
        papers = []
        for article in root.findall(".//PubmedArticle"):
            paper = {
                "id": article.findtext(".//PMID"),
                "title": article.findtext(".//ArticleTitle"),
                "pubdate": article.findtext(".//PubDate/Year"),
                "authors": [
                    {
                        "name": author.findtext(".//LastName", "") + " " + author.findtext(".//ForeName", ""),
                        "affiliations": [aff.text for aff in author.findall(".//Affiliation")]
                    }
                    for author in article.findall(".//Author")
                ],
                "corresponding_author_email": article.findtext(".//Author[@ValidYN='Y']//Email")
            }
            papers.append(paper)
        print(f"Fetched {len(papers)} papers.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    
    return papers

def filter_papers(papers: List[Dict]) -> List[Dict]:

 
    filtered = []
    for paper in papers:
        authors = paper.get("authors", [])
        non_academic_authors = []
        company_affiliations = []
        

        for author in authors:
            affiliations = author.get("affiliations", [])
            for aff in affiliations:
     
                if not any(word in aff.lower() for word in ["university", "college", "lab"]):
                    non_academic_authors.append(author["name"])
                
        
                if any(word in aff.lower() for word in ["pharma", "biotech", "inc", "ltd"]):
                    company_affiliations.append(aff)
        
      
        if non_academic_authors and company_affiliations:
            filtered.append({
                "PubmedID": paper["id"],
                "Title": paper["title"],
                "Publication Date": paper["pubdate"],
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": paper.get("corresponding_author_email", "")
            })
    
    print(f"Filtered {len(filtered)} papers.")
    return filtered

def save_to_csv(data: List[Dict], filename: str) -> None:
 
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)