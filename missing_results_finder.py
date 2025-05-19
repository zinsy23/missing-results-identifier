import sys
import os
import re

def extract_filename(path):
    """Extract just the filename from the full path."""
    return os.path.basename(path.strip())

def check_missing_results(search_terms_file, target_file):
    # Read search terms from the first file
    with open(search_terms_file, 'r') as f:
        search_terms = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"Loaded {len(search_terms)} search terms from {search_terms_file}")
    
    # Read the content of the target file
    with open(target_file, 'r', encoding='utf-8') as f:
        target_content = f.read()
    
    print(f"Loaded target file {target_file} ({len(target_content):,} characters)")
    
    missing_terms = []
    found_terms = []
    
    # Check each search term
    for term in search_terms:
        # First try the full path (with escaped special characters for paths)
        escaped_term = re.escape(term)
        if not re.search(escaped_term, target_content, re.IGNORECASE):
            # Try just the filename
            filename = extract_filename(term)
            escaped_filename = re.escape(filename)
            if not re.search(escaped_filename, target_content, re.IGNORECASE):
                missing_terms.append(term)
            else:
                found_terms.append(term)
        else:
            found_terms.append(term)
    
    # Print the results
    print(f"\nSummary: {len(found_terms)} results found, {len(missing_terms)} results missing")
    
    if missing_terms:
        print(f"\nThe following {len(missing_terms)} search terms had no results in the target file:")
        for term in missing_terms:
            print(term)
    else:
        print("\nAll search terms had results in the target file.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python missing_results_finder.py <search_terms_file> <target_file>")
        sys.exit(1)
    
    search_terms_file = sys.argv[1]
    target_file = sys.argv[2]
    
    try:
        check_missing_results(search_terms_file, target_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 