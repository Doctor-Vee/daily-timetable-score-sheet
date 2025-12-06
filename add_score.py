#!/usr/bin/env python3
from datetime import datetime, timedelta
import re
import subprocess

def parse_last_entry(line):
    """Extract date from last entry line."""
    match = re.search(r'(\d{2})/(\d{2})', line)
    if match:
        day, month = map(int, match.groups())
        return datetime(2025, month, day)
    return None

def get_next_date(readme_path):
    """Find the last date entry and calculate next date."""
    with open(readme_path, 'r') as f:
        lines = f.readlines()
    
    for line in reversed(lines):
        if re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', line):
            last_date = parse_last_entry(line)
            if last_date:
                return last_date + timedelta(days=1)
    return datetime.now()

def format_entry(date, completed, total):
    """Format the daily entry line."""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_name = days[date.weekday()]
    percentage = round((completed / total) * 100)
    return f"{day_name} - {date.strftime('%d/%m')} - Tasks ({completed}/{total}) = {percentage}%  \n"

def add_entry(score):
    """Add new entry to README."""
    readme_path = 'README.md'
    
    # Parse score
    completed, total = map(int, score.split('/'))
    
    # Get next date
    next_date = get_next_date(readme_path)
    
    # Create entry
    entry = format_entry(next_date, completed, total)
    
    # Append to file
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Find insertion point (before the git command section)
    insert_pos = content.rfind('\n---\ngit add')
    if insert_pos == -1:
        insert_pos = len(content)
    
    new_content = content[:insert_pos] + entry + content[insert_pos:]
    
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Added: {entry.strip()}")
    
    # Run git commands
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', ':sparkles: add score for the day'])
    subprocess.run(['git', 'push'])

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python add_score.py <score>")
        print("Example: python add_score.py 10/12")
        sys.exit(1)
    
    add_entry(sys.argv[1])
