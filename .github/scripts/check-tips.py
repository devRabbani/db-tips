import re
import os
import json
from github import Github

def extract_tips(content):
    pattern = r'\[(.*?)\]$$(.*?)$$\s*\n((?:- .*\n)+)'
    matches = re.findall(pattern, content, re.DOTALL)
    return [(author.strip(), link.strip(), [tip.strip()[2:] for tip in tips.strip().split('\n')]) for author, link, tips in matches]

def is_valid_tip(tip):
    return len(tip) <= 280

def check_duplicates(new_tips, existing_tips):
    duplicates = []
    for new_tip in new_tips:
        if new_tip in existing_tips:
            duplicates.append(new_tip)
    return duplicates

def main():
    # Read the PR event
    with open(os.environ['GITHUB_EVENT_PATH']) as f:
        event = json.load(f)
    
    pr_number = event['pull_request']['number']
    repo_name = event['repository']['full_name']
    
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    files = pr.get_files()
    tips_file = next((file for file in files if file.filename == 'tips.md'), None)
    
    if not tips_file:
        pr.create_issue_comment("No changes to tips.md found in this PR.")
        return
    
    new_content = tips_file.patch
    
    # Extract new tips
    new_tips = extract_tips(new_content)
    
    # Check format and length
    format_errors = []
    for author, link, tips in new_tips:
        if not author or not link:
            format_errors.append("Author name or link is missing")
        for tip in tips:
            if not is_valid_tip(tip):
                format_errors.append(f"Tip by {author} exceeds 280 characters: {tip}")
    
    # Check for duplicates
    with open('tips.md', 'r') as f:
        existing_content = f.read()
    existing_tips = extract_tips(existing_content)
    all_existing_tips = [tip for _, _, tips in existing_tips for tip in tips]
    
    duplicates = check_duplicates([tip for _, _, tips in new_tips for tip in tips], all_existing_tips)
    
    # Create comment
    comment = "## Tips Check Results\n\n"
    if format_errors:
        comment += "### Format Errors\n"
        for error in format_errors:
            comment += f"- {error}\n"
    
    if duplicates:
        comment += "\n### Duplicate Tips\n"
        for tip in duplicates:
            comment += f"- {tip}\n"
    
    if not format_errors and not duplicates:
        comment += "All tips are correctly formatted and unique. Good job!"
    
    pr.create_issue_comment(comment)

if __name__ == "__main__":
    main()