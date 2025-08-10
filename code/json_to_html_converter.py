#!/usr/bin/env python3
"""
JSON to HTML Converter for IMO25 Solution Files

This program converts the large JSON solution files to readable HTML format,
making it easier to analyze the solutions and verification results.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_json_file(file_path):
    """Load and parse a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def format_timestamp(timestamp_str):
    """Format timestamp string for display."""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


def create_html_header(title):
    """Create the HTML header with CSS styling."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }}
        h3 {{
            color: #2c3e50;
            margin-top: 25px;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .metadata-item {{
            background-color: white;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }}
        .metadata-label {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        .metadata-value {{
            color: #34495e;
        }}
        .run {{
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            margin: 20px 0;
            overflow: hidden;
        }}
        .run-header {{
            background-color: #34495e;
            color: white;
            padding: 15px;
            cursor: pointer;
            user-select: none;
        }}
        .run-header:hover {{
            background-color: #2c3e50;
        }}
        .run-content {{
            padding: 20px;
            display: none;
        }}
        .run-content.expanded {{
            display: block;
        }}
        .status {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
            margin-left: 15px;
        }}
        .status.failed {{
            background-color: #e74c3c;
            color: white;
        }}
        .status.success {{
            background-color: #27ae60;
            color: white;
        }}
        .iteration {{
            border: 1px solid #ddd;
            border-radius: 6px;
            margin: 15px 0;
            padding: 15px;
        }}
        .iteration-header {{
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }}
        .verification {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
        }}
        .verification-header {{
            font-weight: bold;
            color: #856404;
            margin-bottom: 10px;
        }}
        .bug-report {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 6px;
            padding: 15px;
            margin-top: 10px;
        }}
        .solution-text {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 20px;
            margin: 15px 0;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 400px;
            overflow-y: auto;
        }}
        .toggle-btn {{
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin: 10px 0;
        }}
        .toggle-btn:hover {{
            background-color: #2980b9;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .stat-item {{
            background-color: #e8f4fd;
            padding: 10px 15px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }}
        .stat-label {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .stat-value {{
            color: #34495e;
            font-size: 1.2em;
        }}
        .problem-statement {{
            background-color: #e8f5e8;
            border: 1px solid #c3e6c3;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
            white-space: pre-wrap;
            font-family: 'Georgia', serif;
            line-height: 1.8;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            .metadata-grid {{
                grid-template-columns: 1fr;
            }}
            .stats {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>"""


def create_html_footer():
    """Create the HTML footer with JavaScript."""
    return """
    </div>
    <script>
        // Toggle run content visibility
        document.querySelectorAll('.run-header').forEach(header => {
            header.addEventListener('click', function() {
                const content = this.nextElementSibling;
                content.classList.toggle('expanded');
            });
        });

        // Toggle solution text visibility
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const solutionText = this.nextElementSibling;
                if (solutionText.style.display === 'none') {
                    solutionText.style.display = 'block';
                    this.textContent = 'Hide Solution';
                } else {
                    solutionText.style.display = 'none';
                    this.textContent = 'Show Solution';
                }
            });
            // Initially hide solution text
            const solutionText = btn.nextElementSibling;
            solutionText.style.display = 'none';
        });

        // Add keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                // Close all expanded sections
                document.querySelectorAll('.run-content.expanded').forEach(content => {
                    content.classList.remove('expanded');
                });
            }
        });
    </script>
</body>
</html>"""


def format_problem_statement(statement):
    """Format the problem statement for display."""
    if not statement:
        return "No problem statement provided"

    # Clean up the statement
    cleaned = statement.replace("*** Problem Statement ***\n\n", "")
    return cleaned.strip()


def create_metadata_section(data):
    """Create the metadata section of the HTML."""
    metadata = data.get("metadata", {})

    html = '<div class="metadata">'
    html += "<h2>Problem Information</h2>"
    html += '<div class="metadata-grid">'

    # Problem statement
    if "problem_statement" in metadata:
        html += f"""
        <div class="metadata-item">
            <div class="metadata-label">Problem Statement</div>
            <div class="problem-statement">{format_problem_statement(metadata['problem_statement'])}</div>
        </div>"""

    # Basic metadata
    if "timestamp" in metadata:
        html += f"""
        <div class="metadata-item">
            <div class="metadata-label">Timestamp</div>
            <div class="metadata-value">{format_timestamp(metadata['timestamp'])}</div>
        </div>"""

    if "model_name" in metadata:
        html += f"""
        <div class="metadata-item">
            <div class="metadata-label">Model</div>
            <div class="metadata-value">{metadata['model_name']}</div>
        </div>"""

    html += "</div></div>"
    return html


def create_run_section(run_data, run_index):
    """Create HTML for a single run."""
    run_number = run_data.get("run_number", run_index)
    timestamp = format_timestamp(run_data.get("timestamp", ""))
    status = run_data.get("status", "unknown")
    reason = run_data.get("reason", "")

    status_class = "failed" if status == "failed" else "success"
    status_text = status.upper()

    html = f"""
        <div class="run">
            <div class="run-header">
                <strong>Run {run_number}</strong>
                <span class="status {status_class}">{status_text}</span>
                <small style="float: right;">{timestamp}</small>
            </div>
            <div class="run-content">"""

    if reason:
        html += f"<p><strong>Reason:</strong> {reason}</p>"

    # Iterations
    iterations = run_data.get("iterations", [])
    if iterations:
        html += f"<h3>Iterations ({len(iterations)})</h3>"

        for i, iteration in enumerate(iterations):
            html += create_iteration_section(iteration, i)

    html += "</div></div>"
    return html


def create_iteration_section(iteration, index):
    """Create HTML for a single iteration."""
    iteration_num = iteration.get("iteration", index)
    correct_count = iteration.get("correct_count", 0)
    error_count = iteration.get("error_count", 0)
    verification_result = iteration.get("verification_result", "unknown")
    is_correct = iteration.get("is_correct", False)

    html = f"""
        <div class="iteration">
            <div class="iteration-header">
                <strong>Iteration {iteration_num}</strong>
                <span class="status {"success" if is_correct else "failed"}">
                    {verification_result.upper()}
                </span>
                <small style="margin-left: 15px;">
                    Correct: {correct_count}, Errors: {error_count}
                </small>
            </div>"""

    # Solution text
    if "corrected_solution" in iteration:
        html += """
            <button class="toggle-btn">Show Solution</button>
            <div class="solution-text">"""
        html += iteration["corrected_solution"]
        html += "</div>"

    # Verification details
    if "verification" in iteration:
        verification = iteration["verification"]
        html += '<div class="verification">'
        html += '<div class="verification-header">Verification Results</div>'

        if "bug_report" in verification:
            html += '<div class="bug-report">'
            html += f"<strong>Bug Report:</strong><br>"
            html += verification["bug_report"].replace("\n", "<br>")
            html += "</div>"

        html += "</div>"

    html += "</div>"
    return html


def create_stats_section(data):
    """Create a statistics summary section."""
    runs = data.get("runs", [])
    total_runs = len(runs)
    failed_runs = sum(1 for run in runs if run.get("status") == "failed")
    successful_runs = total_runs - failed_runs

    total_iterations = sum(len(run.get("iterations", [])) for run in runs)
    total_correct = sum(
        sum(iter.get("correct_count", 0) for iter in run.get("iterations", []))
        for run in runs
    )
    total_errors = sum(
        sum(iter.get("error_count", 0) for iter in run.get("iterations", []))
        for run in runs
    )

    html = (
        """
        <div class="stats">
            <div class="stat-item">
                <div class="stat-label">Total Runs</div>
                <div class="stat-value">"""
        + str(total_runs)
        + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Successful Runs</div>
                <div class="stat-value">"""
        + str(successful_runs)
        + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Failed Runs</div>
                <div class="stat-value">"""
        + str(failed_runs)
        + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Iterations</div>
                <div class="stat-value">"""
        + str(total_iterations)
        + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Correct</div>
                <div class="stat-value">"""
        + str(total_correct)
        + """</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Errors</div>
                <div class="stat-value">"""
        + str(total_errors)
        + """</div>
            </div>
        </div>"""
    )

    return html


def convert_json_to_html(json_file_path, output_dir=None):
    """Convert a JSON file to HTML format."""
    # Load JSON data
    data = load_json_file(json_file_path)
    if not data:
        return False

    # Determine output path
    if output_dir is None:
        # If running from code directory, output to run_logs directory
        if Path.cwd().name == "code":
            output_dir = Path("../run_logs")
        else:
            output_dir = Path(json_file_path).parent

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Create output filename
    input_filename = Path(json_file_path).stem
    output_filename = f"{input_filename}_converted.html"
    output_path = output_dir / output_filename

    # Create HTML content
    title = f"IMO25 Solution Analysis - {input_filename.replace('_', ' ').title()}"

    html_content = create_html_header(title)

    # Add metadata section
    html_content += create_metadata_section(data)

    # Add statistics section
    html_content += create_stats_section(data)

    # Add runs section
    runs = data.get("runs", [])
    if runs:
        html_content += "<h2>Solution Attempts</h2>"
        for i, run in enumerate(runs):
            html_content += create_run_section(run, i)

    # Add footer
    html_content += create_html_footer()

    # Write HTML file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Successfully converted {json_file_path} to {output_path}")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python json_to_html_converter.py <json_file> [output_directory]")
        print("Example: python json_to_html_converter.py ../run_logs/solution_01.json")
        return

    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(json_file):
        print(f"Error: File {json_file} not found")
        return

    success = convert_json_to_html(json_file, output_dir)
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")


if __name__ == "__main__":
    main()
