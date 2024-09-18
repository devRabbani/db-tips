import re

def extract_tips(content):
    pattern = r'---\nauthor:\s*(.*?)\n---\n\n((?:- .*\n)+)'
    matches = re.findall(pattern, content, re.DOTALL)
    return [(author.strip(), [tip.strip()[2:] for tip in tips.strip().split('\n')]) for author, tips in matches]

def update_readme(tips):
    with open('README.md', 'r') as f:
        content = f.read()
    
    latest_tips = "## Latest Tips\n\n"
    for _, author_tips in tips[-10:]:  #the last 10 tips
        for tip in author_tips:
            latest_tips += f"- {tip}\n"
    
    new_content = re.sub(r'## Latest Tips\n\n.*', latest_tips, content, flags=re.DOTALL)
    
     # Print for debugging
    print("New README content:\n", new_content)

    with open('README.md', 'w') as f:
        f.write(new_content)

def update_contributors(contributors):
    with open('contributors.md', 'r') as f:
        content = f.read()
    
    for contributor in contributors:
        if contributor not in content:
            content += f"\n- @{contributor}"
     # Print for debugging
    print("New Contributors content:\n", content)
    
    with open('contributors.md', 'w') as f:
        f.write(content)

def main():
    with open('tips.md', 'r') as f:
        content = f.read()
    
    tips = extract_tips(content)
    
    # Update README
    update_readme(tips)
    
    # Update contributors
    contributors = set(author for author, _ in tips)
    update_contributors(contributors)

if __name__ == "__main__":
    main()