# JSON to HTML Converter for IMO25 Solution Files

This tool converts the large JSON solution files to readable HTML format, making it easier to analyze the solutions and verification results.

## Files Created

- `code/json_to_html_converter.py` - Main converter script
- `code/convert_all_json.py` - Batch converter for all JSON files
- `JSON_CONVERTER_README.md` - This documentation file

## Features

The HTML output includes:

1. **Problem Information Section**
   - Problem statement
   - Timestamp
   - Model name used

2. **Statistics Summary**
   - Total runs
   - Successful vs failed runs
   - Total iterations
   - Correct vs error counts

3. **Interactive Solution Attempts**
   - Collapsible run sections
   - Iteration details with verification results
   - Toggle-able solution text
   - Bug reports and verification details

4. **Modern UI**
   - Responsive design
   - Color-coded status indicators
   - Interactive elements
   - Mobile-friendly layout

## Usage

### From the code directory (recommended)

```bash
cd code

# Convert a single file
python3 json_to_html_converter.py ../run_logs/solution_01.json

# Convert all files at once
python3 convert_all_json.py

# Specify custom output directory
python3 json_to_html_converter.py ../run_logs/solution_01.json ../output_folder/
```

### From the root directory

```bash
# Convert a single file
python3 code/json_to_html_converter.py run_logs/solution_01.json

# Convert all files at once
python3 code/convert_all_json.py
```

## Output

The converter creates HTML files in the same directory as the input JSON files (unless specified otherwise) with the naming pattern:
- `solution_01.json` → `solution_01_converted.html`
- `solution_02.json` → `solution_02_converted.html`
- etc.

**Note**: When running from the `code` directory, HTML files are automatically placed in the `run_logs` directory alongside the original JSON files.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## How It Works

1. **Parses JSON Structure**: Reads the JSON file and extracts metadata, runs, iterations, and verification results
2. **Generates HTML**: Creates a structured HTML document with CSS styling
3. **Interactive Features**: Adds JavaScript for collapsible sections and toggle buttons
4. **Responsive Design**: Uses CSS Grid and Flexbox for modern layout
5. **Smart Path Handling**: Automatically detects current working directory and adjusts paths accordingly

## Benefits

- **Readable Format**: Much easier to read than raw JSON
- **Interactive**: Click to expand/collapse sections
- **Searchable**: Can use browser search functionality
- **Portable**: HTML files can be shared and viewed on any device
- **Analysis**: Better visualization of solution attempts and verification results

## Example Output Structure

```
IMO25 Solution Analysis - Solution 01
├── Problem Information
│   ├── Problem Statement
│   ├── Timestamp
│   └── Model
├── Statistics Summary
│   ├── Total Runs
│   ├── Successful Runs
│   ├── Failed Runs
│   ├── Total Iterations
│   ├── Total Correct
│   └── Total Errors
└── Solution Attempts
    ├── Run 1 (Success/Failed)
    │   └── Iterations
    │       ├── Iteration 1
    │       │   ├── Solution Text (toggle-able)
    │       │   └── Verification Results
    │       └── Iteration 2
    └── Run 2 (Success/Failed)
        └── Iterations
```

## Troubleshooting

- **File Not Found**: Ensure the JSON file path is correct relative to your current directory
- **Permission Errors**: Make sure you have read/write permissions
- **Large Files**: The converter handles large JSON files efficiently by processing them in chunks
- **Path Issues**: If running from the code directory, use `../run_logs/` to reference JSON files

## Customization

You can modify the CSS styling in the `create_html_header()` function to change colors, fonts, or layout. The JavaScript functionality can also be customized in the `create_html_footer()` function.

## Directory Structure

```
IMO25/
├── code/
│   ├── json_to_html_converter.py
│   ├── convert_all_json.py
│   └── ... (other code files)
├── run_logs/
│   ├── solution_01.json
│   ├── solution_01_converted.html (generated)
│   └── ... (other solution files)
└── JSON_CONVERTER_README.md
```
