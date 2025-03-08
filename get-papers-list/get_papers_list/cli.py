import argparse
from .core import fetch_papers, filter_papers, save_to_csv

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

if __name__ == "__main__":
    main()