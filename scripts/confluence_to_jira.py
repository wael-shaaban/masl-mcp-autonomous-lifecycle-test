# Template: Confluence -> Jira ticket composer
# Requires: requests
# Fill in: CONFLUENCE_BASE, CONFLUENCE_API_TOKEN, JIRA_BASE, JIRA_API_TOKEN, JIRA_PROJECT_KEY
import requests, os, sys, json

CONFLUENCE_BASE = os.getenv('CONFLUENCE_BASE') or 'https://your-confluence.atlassian.net'
CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN') or '<CONFLUENCE_API_TOKEN>'
CONFLUENCE_USER = os.getenv('CONFLUENCE_USER') or 'email@example.com'
JIRA_BASE = os.getenv('JIRA_BASE') or 'https://your-domain.atlassian.net'
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN') or '<JIRA_API_TOKEN>'
JIRA_USER = os.getenv('JIRA_USER') or 'email@example.com'
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY') or 'PROJ'

def get_confluence_page(page_id):
    url = f"{CONFLUENCE_BASE}/wiki/rest/api/content/{page_id}?expand=body.storage,version,metadata.labels"
    r = requests.get(url, auth=(CONFLUENCE_USER, CONFLUENCE_API_TOKEN))
    r.raise_for_status()
    return r.json()

def extract_action_items(html_body):
    # VERY naive extractor: looks for lines starting with - [ ] or 'Action Item:'
    lines = html_body.splitlines()
    items = []
    for line in lines:
        ln = line.strip()
        if ln.startswith('- [ ]') or 'Action Item' in ln:
            items.append(ln)
    return items

def create_jira_issue(summary, description):
    url = f"{JIRA_BASE}/rest/api/2/issue"
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"}
        }
    }
    r = requests.post(url, auth=(JIRA_USER, JIRA_API_TOKEN), json=payload, headers={'Content-Type':'application/json'})
    r.raise_for_status()
    return r.json()

def main(page_id):
    page = get_confluence_page(page_id)
    html = page['body']['storage']['value']
    items = extract_action_items(html)
    print(f"Found {len(items)} candidate action items.")
    for i, it in enumerate(items,1):
        summary = f"Auto: {it[:80]}"
        desc = f"Auto-generated from Confluence page {page_id}\n\nOriginal:\n{it}"
        issue = create_jira_issue(summary, desc)
        print('Created', issue.get('key'))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: confluence_to_jira.py <confluence-page-id>')
        sys.exit(1)
    main(sys.argv[1])
