from typing import List, Dict

def filter_papers(papers: List[Dict]) -> List[Dict]:
    filtered_papers = []
    for paper in papers:
        authors = paper.get("authors", [])
        non_academic_authors = []
        company_affiliations = []
        
        for author in authors:
            affiliations = author.get("affiliations", [])
            for affiliation in affiliations:
                if "pharmaceutical" in affiliation.lower() or "biotech" in affiliation.lower():
                    non_academic_authors.append(author.get("name", ""))
                    company_affiliations.append(affiliation)
        
        if non_academic_authors:
            filtered_paper = {
                "PubmedID": paper.get("uid", ""),
                "Title": paper.get("title", ""),
                "Publication Date": paper.get("pubdate", ""),
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": paper.get("corresponding_author_email", "")
            }
            filtered_papers.append(filtered_paper)
    
    return filtered_papers