# Missing Results Identifier

A simple but effective Python utility that helps you identify which items from a list don't appear in a target file. This is particularly useful for finding "missing results" across files.

## Usage

```
python missing_results_finder.py <search_terms_file> <target_file> [show_found]
```

Where:
- `<search_terms_file>`: A text file containing search terms, one per line
- `<target_file>`: The file to search against
- `[show_found]`: Optional parameter to display found results instead of missing ones
  (Use 'show_found', 'found', 'true', 'yes', or '1')

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

### Finding missing results (default):
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

### Finding items with results (using show_found):
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

## Other Potential Use Cases

This utility can be used in many scenarios:
- Finding which dependencies aren't imported in a codebase
- Checking which references aren't cited in a document
- Identifying which items from a checklist aren't mentioned in a report
- Verifying which customers haven't been contacted from a list 