import re

def extract_tips(content):
    pattern = r'\[(.*?)\]\((.*?)\)\s*\n- (.*?)(?=\n\[\w+\]\(.*?\)|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    return [(author.strip(), link.strip(), tip.strip()) for author, link, tip in matches]

def update_readme(tips):
    with open('README.md', 'r') as f:
        content = f.read()
    
 
    tips_section = "\n".join(f"- {tip}" for _, _, tip in tips[-10:])  # Last 10 tips
    new_content = re.sub(r'## Latest Tips\n\n.*', f"## Latest Tips\n\n{tips_section}", content, flags=re.DOTALL)
    
    with open('README.md', 'w') as f:
        f.write(new_content)

def update_contributors(contributors):
    with open('contributors.md', 'r') as f:
        content = f.read()
    
    for author, link in contributors:
        entry = f"- [{author}]({link})"
        if entry not in content:
            content += f"\n{entry}"
    
    with open('contributors.md', 'w') as f:
        f.write(content)

def main():
    with open('tips.md', 'r') as f:
        content = f.read()
    
    tips = extract_tips(content)
    print("Tips extracted",tips)
    # Update README
    update_readme(tips)
    
    # Update contributors
    contributors = [(author, link) for author, link, _ in tips]
    print("Contributors updated",contributors)
    update_contributors(contributors)

if __name__ == "__main__":
    main()
