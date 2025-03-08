import requests
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
from typing import List, Dict

# Core Functionality

def fetch_papers(query: str) -> List[Dict]:
    """
    Fetches research papers from PubMed based on a query.
    
    Args:
        query (str): The PubMed query string.
    
    Returns:
        List[Dict]: A list of papers with their details.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # Step 1: Fetch paper IDs using esearch
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=json"
    response = requests.get(search_url)
    response.raise_for_status()
    
    # Extract paper IDs from the response
    paper_ids = response.json()["esearchresult"]["idlist"]
    print(f"Fetched {len(paper_ids)} paper IDs.")
    
    # Step 2: Fetch paper details using efetch (XML format)
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(paper_ids)}&retmode=xml"
    response = requests.get(fetch_url)
    response.raise_for_status()
    
    # Parse the XML response
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
    """
    Filters papers to identify non-academic authors and pharmaceutical/biotech affiliations.
    
    Args:
        papers (List[Dict]): A list of papers with their details.
    
    Returns:
        List[Dict]: A list of filtered papers with relevant information.
    """
    filtered = []
    for paper in papers:
        authors = paper.get("authors", [])
        non_academic_authors = []
        company_affiliations = []
        
        # Parse authors and affiliations
        for author in authors:
            affiliations = author.get("affiliations", [])
            for aff in affiliations:
                # Identify non-academic authors
                if not any(word in aff.lower() for word in ["university", "college", "lab"]):
                    non_academic_authors.append(author["name"])
                
                # Identify pharmaceutical/biotech affiliations
                if any(word in aff.lower() for word in ["pharma", "biotech", "inc", "ltd"]):
                    company_affiliations.append(aff)
        
        # Collect relevant information
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
    """
    Saves the filtered results to a CSV file.
    
    Args:
        data (List[Dict]): The filtered data to save.
        filename (str): The name of the output CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Command-Line Interface

def main():
    """
    Main function to handle command-line arguments and execute the program.
    """
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="PubMed query string")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    args = parser.parse_args()

    # Fetch and filter papers
    papers = fetch_papers(args.query)
    if args.debug:
        print(f"Fetched {len(papers)} papers.")
    
    filtered_papers = filter_papers(papers)
    if args.debug:
        print(f"Filtered {len(filtered_papers)} papers.")
    
    # Save or print results
    if args.file:
        save_to_csv(filtered_papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        print(filtered_papers)

# Entry Point

if __name__ == "__main__":
    main()