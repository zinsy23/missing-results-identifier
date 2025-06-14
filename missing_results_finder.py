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

def perform_direct_comparison(search_terms, target_terms, show_found=False):
    """Perform comparison directly with in-memory lists instead of files."""
    total_search_terms = len(search_terms)
    print(f"Comparing {total_search_terms} search terms against {len(target_terms)} target terms")
    
    missing_terms = []
    found_terms = []
    
    # Convert target terms to lowercase for case-insensitive comparison
    target_terms_lower = [term.lower() for term in target_terms]
    
    # Check each search term
    for term in search_terms:
        # First try the full term (case-insensitive)
        if term.lower() in target_terms_lower:
            found_terms.append(term)
        else:
            # Try just the filename part
            filename = extract_filename(term)
            if filename.lower() in target_terms_lower:
                found_terms.append(term)
            else:
                missing_terms.append(term)
    
    # Count actual terms in lists
    actual_missing = len(missing_terms)
    actual_found = len(found_terms)
    
    # Print the results with clear counts
    print(f"\nProcessed {total_search_terms} terms:")
    print(f"- Found: {actual_found} terms")
    print(f"- Missing: {actual_missing} terms")
    
    # Display results based on user preference
    if show_found:
        if found_terms:
            print(f"\nThe following {actual_found} terms had results in the target:")
            for term in found_terms:
                print(term)
        else:
            print("\nNo search terms had results in the target.")
    else:
        if missing_terms:
            print(f"\nThe following {actual_missing} terms had no results in the target:")
            for term in missing_terms:
                print(term)
        else:
            print("\nAll search terms had results in the target.")

def file_comparison(debug=False):
    """Interactive file comparison using directory listings and file ranges."""
    
    def get_directory_files(directory_path):
        """Get sorted list of files in a directory."""
        try:
            if not os.path.isdir(directory_path):
                print(f"Error: '{directory_path}' is not a valid directory.")
                return None
            
            # Get all files (not directories) and sort alphabetically
            all_items = os.listdir(directory_path)
            files = [f for f in all_items if os.path.isfile(os.path.join(directory_path, f))]
            files.sort()
            return files
        except Exception as e:
            print(f"Error reading directory '{directory_path}': {str(e)}")
            return None
    
    def display_files_with_numbers(files):
        """Display files with their position numbers."""
        if debug:
            print(f"\nFound {len(files)} files:")
            for i, filename in enumerate(files, 1):
                print(f"{i:3d}: {filename}")
        else:
            print(f"\nFound {len(files)} files. Use --debug to see full list.")
    
    def parse_file_selection(selection_str, files, allow_missing=False):
        """Parse semicolon-separated file selections with range support."""
        selected_indices = set()
        selected_filenames = []  # Track actual filenames for missing file support
        
        # Split by semicolon and process each part
        parts = [part.strip() for part in selection_str.split(';') if part.strip()]
        
        for part in parts:
            if '-' in part:
                # Handle range (e.g., "250606_001-250612_005")
                try:
                    start_filename, end_filename = part.split('-', 1)
                    start_filename = start_filename.strip()
                    end_filename = end_filename.strip()
                    
                    # Find the indices of start and end filenames (case-insensitive)
                    start_idx = None
                    end_idx = None
                    
                    for i, filename in enumerate(files):
                        if filename.lower() == start_filename.lower():
                            start_idx = i + 1  # Convert to 1-based
                        if filename.lower() == end_filename.lower():
                            end_idx = i + 1    # Convert to 1-based
                    
                    if start_idx is None:
                        if allow_missing:
                            selected_filenames.append(start_filename)
                            if debug:
                                print(f"Note: Start filename '{start_filename}' will be checked in comparison")
                        else:
                            if debug:
                                print(f"Warning: Start filename '{start_filename}' not found in directory")
                        continue
                    if end_idx is None:
                        if allow_missing:
                            selected_filenames.append(end_filename)
                            if debug:
                                print(f"Note: End filename '{end_filename}' will be checked in comparison")
                        else:
                            if debug:
                                print(f"Warning: End filename '{end_filename}' not found in directory")
                        continue
                    
                    if start_idx > end_idx:
                        print(f"Warning: Start file '{start_filename}' comes after end file '{end_filename}' in alphabetical order")
                        continue
                    
                    # Add all indices in range (inclusive)
                    selected_indices.update(range(start_idx, end_idx + 1))
                    if debug:
                        print(f"Range '{start_filename}' to '{end_filename}': selected {end_idx - start_idx + 1} files")
                    
                except ValueError:
                    print(f"Warning: Invalid range format '{part}' (expected format: 'start_filename-end_filename')")
                    continue
            else:
                # Handle single filename or number
                part = part.strip()
                
                # Try as filename first (case-insensitive)
                found_as_filename = False
                for i, filename in enumerate(files):
                    if filename.lower() == part.lower():
                        selected_indices.add(i + 1)  # Convert to 1-based
                        found_as_filename = True
                        break
                
                # If not found as filename, try as number
                if not found_as_filename:
                    try:
                        num = int(part)
                        if num < 1 or num > len(files):
                            print(f"Warning: Invalid file number '{num}' (valid range: 1-{len(files)})")
                            continue
                        selected_indices.add(num)
                    except ValueError:
                        if allow_missing:
                            # Treat as a filename that should be checked in comparison
                            selected_filenames.append(part)
                            if debug:
                                print(f"Note: '{part}' will be checked in comparison")
                        else:
                            if debug:
                                print(f"Warning: '{part}' is neither a valid filename nor a valid number")
                        continue
        
        return sorted(selected_indices), selected_filenames
    
    def get_selected_filenames(files, selected_indices):
        """Get actual filenames based on selected indices."""
        return [files[i-1] for i in selected_indices]  # Convert to 0-based indexing
    
    # Get source directory
    print("=== Source Directory Selection ===")
    while True:
        source_dir = input("Enter source directory path: ").strip()
        if not source_dir:
            print("Please enter a valid directory path.")
            continue
        
        source_files = get_directory_files(source_dir)
        if source_files is not None:
            break
    
    if not source_files:
        print("No files found in source directory.")
        return
    
    # Display source files and get selection
    display_files_with_numbers(source_files)
    print("\nFile selection format:")
    print("- Single files by number: 1, 5, 10")
    print("- Single files by name: filename.txt, data.csv")
    print("- Ranges by filename: 250606_001-250612_005")
    print("- Mixed: 1, filename.txt, start_file-end_file, 20")
    print("- Use semicolons (;) to separate multiple selections")
    print("- Ranges include all files alphabetically between start and end filenames")
    
    while True:
        source_selection = input("\nEnter source file selection (or press Enter to skip and specify files from destination): ").strip()
        if not source_selection:
            print("Skipping source file selection - you'll specify files from destination instead.")
            source_selected_files = []
            break
        
        source_indices, source_missing_files = parse_file_selection(source_selection, source_files, allow_missing=True)
        if source_indices or source_missing_files:
            source_selected_files = get_selected_filenames(source_files, source_indices)
            # Add any missing files that were specified by name
            source_selected_files.extend(source_missing_files)
            break
        else:
            print("No valid files selected. Please try again.")
    
    if source_selected_files:
        print(f"\nSelected {len(source_selected_files)} source files" + (" (use --debug to see list)" if not debug else ":"))
        if debug:
            for filename in source_selected_files:
                print(f"  - {filename}")
    
    # Get destination directory
    print("\n=== Destination Directory Selection ===")
    while True:
        dest_dir = input("Enter destination directory path: ").strip()
        if not dest_dir:
            print("Please enter a valid directory path.")
            continue
        
        dest_files = get_directory_files(dest_dir)
        if dest_files is not None:
            break
    
    if not dest_files:
        print("No files found in destination directory.")
        return
    
    # Handle destination file selection based on whether source files were selected
    if source_selected_files:
        # Source files were selected, so destination can be all files or specific selection
        print(f"\nDestination directory contains {len(dest_files)} files.")
        use_all_dest = input("Use all destination files for comparison? (Y/n): ").strip().lower()
        
        if use_all_dest in ['', 'y', 'yes', '1', 'true']:
            dest_selected_files = dest_files
            print(f"Using all {len(dest_selected_files)} destination files for comparison.")
        else:
            # Display destination files and get selection
            display_files_with_numbers(dest_files)
            
            while True:
                dest_selection = input("\nEnter destination file selection: ").strip()
                if not dest_selection:
                    print("Please enter a file selection.")
                    continue
                
                dest_indices, dest_missing_files = parse_file_selection(dest_selection, dest_files, allow_missing=False)
                if dest_indices:
                    break
                else:
                    print("No valid files selected. Please try again.")
            
            dest_selected_files = get_selected_filenames(dest_files, dest_indices)
            print(f"\nSelected {len(dest_selected_files)} destination files" + (" (use --debug to see list)" if not debug else ":"))
            if debug:
                for filename in dest_selected_files:
                    print(f"  - {filename}")
    else:
        # No source files selected, so we need to specify what we're looking for from destination
        print(f"\nDestination directory contains {len(dest_files)} files.")
        print("Since no source files were selected, specify the files you're looking for:")
        display_files_with_numbers(dest_files)
        
        while True:
            dest_selection = input("\nEnter files to search for (can include files not in destination): ").strip()
            if not dest_selection:
                print("Please enter a file selection.")
                continue
            
            dest_indices, dest_missing_files = parse_file_selection(dest_selection, dest_files, allow_missing=True)
            if dest_indices or dest_missing_files:
                break
            else:
                print("No valid files selected. Please try again.")
        
        # In this case, the "search terms" are what we specified, and "target" is all dest files
        source_selected_files = get_selected_filenames(dest_files, dest_indices)
        source_selected_files.extend(dest_missing_files)
        dest_selected_files = dest_files
        
        print(f"\nLooking for {len(source_selected_files)} files in destination" + (" (use --debug to see list)" if not debug else ":"))
        if debug:
            for filename in source_selected_files:
                print(f"  - {filename}")
        print(f"Searching within all {len(dest_selected_files)} destination files.")
    
    # Ask user if they want to see found or missing results
    print("\n=== Comparison Options ===")
    show_found_input = input("Show found files instead of missing? (y/N): ").strip().lower()
    show_found = show_found_input in ['y', 'yes', '1', 'true']
    
    print(f"\n=== Comparing Files ===")
    print(f"Source: {len(source_selected_files)} files from '{source_dir}'")
    print(f"Target: {len(dest_selected_files)} files from '{dest_dir}'")
    
    # Perform comparison directly with in-memory lists
    perform_direct_comparison(source_selected_files, dest_selected_files, show_found)

if __name__ == "__main__":
    # Check for debug flag
    debug = '--debug' in sys.argv
    if debug:
        sys.argv.remove('--debug')  # Remove it so it doesn't interfere with other argument parsing
    
    if len(sys.argv) > 4:
        print("Usage: python missing_results_finder.py <search_terms_file> <target_file> [show_found] [--debug]")
        print("  Add 'show_found' as a third argument to display found results instead of missing ones")
        print("  Add '--debug' to show verbose output during file selection")
        sys.exit(1)

    if len(sys.argv) < 3:
        file_comparison(debug)
        sys.exit(0)  # Exit after interactive comparison
    
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