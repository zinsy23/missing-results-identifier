import sys
import os
import re

def extract_filename(path):
    """Extract just the filename from the full path."""
    return os.path.basename(path.strip())

def check_missing_results(search_terms_file, target_file, show_found=False):
    # Read search terms from the first file
    with open(search_terms_file, 'r') as f:
        search_terms = [line.strip() for line in f.readlines() if line.strip()]
    
    total_search_terms = len(search_terms)
    print(f"Loaded {total_search_terms} search terms from {search_terms_file}")
    
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
    
    # Count actual terms in lists to ensure no duplication
    actual_missing = len(missing_terms)
    actual_found = len(found_terms)
    total_processed = actual_missing + actual_found
    
    # Print the results with clear counts
    print(f"\nProcessed {total_search_terms} terms:")
    print(f"- Found: {actual_found} terms")
    print(f"- Missing: {actual_missing} terms")
    
    # Detailed verification for count discrepancies
    if total_processed != total_search_terms:
        print(f"\nWARNING: Count discrepancy detected!")
        print(f"Total processed ({total_processed}) doesn't match input terms ({total_search_terms})")
        
        # Check for duplicate entries in search_terms
        unique_search_terms = set(search_terms)
        if len(unique_search_terms) != total_search_terms:
            print(f"Duplicate entries found in search terms: {total_search_terms - len(unique_search_terms)}")
        
        # Check for duplicate entries in result lists
        unique_missing = set(missing_terms)
        unique_found = set(found_terms)
        if len(unique_missing) != actual_missing:
            print(f"Duplicate entries found in missing terms: {actual_missing - len(unique_missing)}")
        if len(unique_found) != actual_found:
            print(f"Duplicate entries found in found terms: {actual_found - len(unique_found)}")
    
    # Display results based on user preference
    if show_found:
        if found_terms:
            print(f"\nThe following {actual_found} terms had results in the target file:")
            for term in found_terms:
                print(term)
        else:
            print("\nNo search terms had results in the target file.")
    else:
        if missing_terms:
            print(f"\nThe following {actual_missing} terms had no results in the target file:")
            for term in missing_terms:
                print(term)
        else:
            print("\nAll search terms had results in the target file.")

def file_comparison():
    source_dir = str(input("Enter the source directory for comparison: "))
    source_files = str(input("Enter the range of files to compare (ascending order): "))
    source_files = source_files.split(';')
    source_dir_files = []
    source_comparison = []
    destination_comparison = []

    try:
        for file in os.listdir(source_dir):
            source_dir_files.append(file)
            check_missing_results(search_terms_file, target_file, show_found)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    for file in source_files:
        file_range = file.split('-')
        start, end = 0
        if(len(file_range) == 2):
            start = source_dir_files.index(file_range[0])
            end = source_dir_files.index(file_range[1])
            for i in (end - start):
                source_comparison.append(source_dir_files[start:end])
        
        for file in source_dir_files[start:end]:
            pass

if __name__ == "__main__":
    if len(sys.argv) > 4:
        print("Usage: python missing_results_finder.py <search_terms_file> <target_file> [show_found]")
        print("  Add 'show_found' as a third argument to display found results instead of missing ones")
        sys.exit(1)

    if len(sys.argv) < 3:
        file_comparison()
    
    search_terms_file = sys.argv[1]
    target_file = sys.argv[2]
    show_found = False
    
    if len(sys.argv) == 4 and sys.argv[3].lower() in ['show_found', 'found', 'true', 'yes', '1']:
        show_found = True
    
    try:
        check_missing_results(search_terms_file, target_file, show_found)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 