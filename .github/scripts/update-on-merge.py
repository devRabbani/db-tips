import re

def extract_tips(content):
    pattern = r'\[(.*?)\]\((.*?)\)\s*\n(- .*(?:\n- .*)*)'
    matches = re.findall(pattern, content, re.DOTALL)
    return [
        (author.strip(), link.strip(), [tip.strip()[2:] for tip in tips.strip().split('\n')])
        for author, link, tips in matches
    ]

def update_readme(tips):
    with open('README.md', 'r') as f:
        content = f.read()
    
    all_tips = [tip for _, _, author_tips in tips for tip in author_tips]
    tips_section = "\n".join(f"- {tip}" for tip in all_tips[-10:])  # Last 10 tips
    new_content = re.sub(r'## Latest Tips\n\n.*?(?=\n\n|\Z)', f"## Latest Tips\n\n{tips_section}", content, flags=re.DOTALL)
    
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
    print("Tips extracted:", tips)
    
    # Update README
    update_readme(tips)
    
    # Update contributors
    contributors = set((author, link) for author, link, _ in tips)
    print("Contributors updated:", contributors)
    update_contributors(contributors)

if __name__ == "__main__":
    main()