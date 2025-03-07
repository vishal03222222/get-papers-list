import argparse
from get_papers_list.fetch_papers import fetch_papers
from get_papers_list.filter_papers import filter_papers
from get_papers_list.utils import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch and filter research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results as CSV.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information.")
    
    args = parser.parse_args()
    
    if args.debug:
        print("Fetching papers...")
    
    papers = fetch_papers(args.query)
    
    if args.debug:
        print(f"Fetched {len(papers)} papers.")
        print("Filtering papers...")
    
    filtered_papers = filter_papers(papers)
    
    if args.debug:
        print(f"Filtered {len(filtered_papers)} papers.")
    
    if args.file:
        save_to_csv(filtered_papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in filtered_papers:
            print(paper)

if __name__ == "__main__":
    main()