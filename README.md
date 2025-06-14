# Missing Results Identifier

A simple but effective Python utility that helps you identify which items from a list don't appear in a target file. This is particularly useful for finding "missing results" across files.

## Usage

### Command Line Mode (File-based)

```
python missing_results_finder.py <search_terms_file> <target_file> [show_found] [--debug]
```

Where:
- `<search_terms_file>`: A text file containing search terms, one per line
- `<target_file>`: The file to search against
- `[show_found]`: Optional parameter to display found results instead of missing ones
  (Use 'show_found', 'found', 'true', 'yes', or '1')
- `[--debug]`: Optional flag to show verbose output

### Interactive Mode (Directory-based)

```
python missing_results_finder.py [--debug]
```

When run without file arguments, the script enters interactive mode where you can:
1. **Select source directory** and choose files using flexible selection methods
2. **Select destination directory** and choose comparison method
3. **Compare file lists** directly without creating temporary files

#### File Selection Methods

The interactive mode supports multiple ways to select files:

- **By number**: `1, 5, 10` (select files by their position in the sorted list)
- **By filename**: `myfile.mp3, data.csv` (case-insensitive)
- **By range**: `250606_001.mp3-250612_005.mp3` (all files alphabetically between start and end)
- **Mixed selection**: `1, myfile.mp3, start_file.txt-end_file.txt, 20`
- **Multiple selections**: Use semicolons (`;`) to separate different selections

#### Interactive Workflow Options

**Option 1: Source-based comparison**
1. Select files from source directory
2. Choose destination directory
3. Compare to see which source files are missing from destination

**Option 2: Destination-based comparison**
1. Skip source file selection (press Enter)
2. Specify files you're looking for in destination selection
3. Compare to see which specified files are missing from destination

#### Debug Mode

Use `--debug` flag for verbose output including:
- Full file listings with numbers
- Detailed selection feedback
- Warning and note messages
- Complete file lists in results

Without `--debug`, output is clean and minimal, showing only counts and essential information.

## How It Works

The script:
1. Loads search terms from the first file
2. Reads the content of the target file
3. For each search term, checks if it appears in the target file
   - First tries the full term
   - If not found, extracts just the filename and tries again
4. Prints a summary of found and missing results
5. Lists all the search terms that had no results in the target file (or found results if show_found is specified)

## Example Use Case: Video Editor Timeline Check

This utility was originally created to solve a specific problem: checking which video files hadn't been imported into a video editing timeline.

### The Problem

When working with a video editor (like DaVinci Resolve), it's common to have many source files but be unsure which ones have already been imported into the timeline. Missing a file could mean missing important content.

### The Solution

By using this script:

1. Export the timeline as an XML file (e.g., "Files Timeline.xml")
2. Create a text file listing all source files (e.g., "File List.txt")
3. Run the script to identify which files haven't been imported yet
4. Or run with the show_found option to see which files are already in the timeline

### Results

In my specific case, I discovered that out of 60 video files, 17 hadn't been imported into the timeline yet. The script clearly listed each missing file, making it easy to identify what needed to be added.

## Requirements

- Python 3.x
- No external dependencies

## Example Output

### Command Line Mode

#### Finding missing results (default):
```
Loaded 60 search terms from File List.txt
Loaded target file Files Timeline.xml (844,000 characters)

Processed 60 terms:
- Found: 43 terms
- Missing: 17 terms

The following 17 terms had no results in the target file:
C:\Users\Joseph\Desktop\2025-03-31 03-04-31.mp4
C:\Users\Joseph\Desktop\2025-04-01 00-16-16.mp4
...
```

#### Finding items with results (using show_found):
```
Loaded 60 search terms from File List.txt
Loaded target file Files Timeline.xml (844,000 characters)

Processed 60 terms:
- Found: 43 terms
- Missing: 17 terms

The following 43 terms had results in the target file:
C:\Users\Joseph\Desktop\2025-03-22 02-09-19.mp4
C:\Users\Joseph\Desktop\2025-03-23 03-40-35.mp4
...
```

### Interactive Mode

#### Example session (normal output):
```
=== Source Directory Selection ===
Enter source directory path: C:\Videos\Source

Found 150 files. Use --debug to see full list.

File selection format:
- Single files by number: 1, 5, 10
- Single files by name: filename.txt, data.csv
- Ranges by filename: 250606_001-250612_005
- Mixed: 1, filename.txt, start_file-end_file, 20
- Use semicolons (;) to separate multiple selections
- Ranges include all files alphabetically between start and end filenames

Enter source file selection: 250606_001.mp3-250612_005.mp3; missing_file.mp3

Selected 25 source files (use --debug to see list)

=== Destination Directory Selection ===
Enter destination directory path: C:\Videos\Timeline

Found 120 files. Use --debug to see full list.

Use all destination files for comparison? (Y/n): y
Using all 120 destination files for comparison.

=== Comparison Options ===
Show found files instead of missing? (y/N): 

=== Comparing Files ===
Source: 25 files from 'C:\Videos\Source'
Target: 120 files from 'C:\Videos\Timeline'

Comparing 25 search terms against 120 target terms

Processed 25 terms:
- Found: 20 terms
- Missing: 5 terms

The following 5 terms had no results in the target:
250607_003.mp3
250610_001.mp3
missing_file.mp3
250611_005.mp3
250612_002.mp3
```

## Other Potential Use Cases

This utility can be used in many scenarios:
- Finding which dependencies aren't imported in a codebase
- Checking which references aren't cited in a document
- Identifying which items from a checklist aren't mentioned in a report
- Verifying which customers haven't been contacted from a list 