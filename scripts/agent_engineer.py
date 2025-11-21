# Template: Agent-Engineer -> create branch and PR on GitHub
# Requires: PyGithub (pip install PyGithub)
import os, sys
from github import Github

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') or '<GITHUB_TOKEN>'
REPO_NAME = os.getenv('GITHUB_REPO') or 'your-org/your-repo'

def create_branch_and_pr(branch_name, file_changes, pr_title, pr_body):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    main = repo.get_branch(repo.default_branch)
    # create ref
    repo.create_git_ref(ref='refs/heads/' + branch_name, sha=main.commit.sha)
    # create a file or update - here we create a sample file
    for path, content in file_changes.items():
        repo.create_file(path, f'Auto: add {path}', content, branch=branch_name)
    pr = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base=repo.default_branch)
    return pr

if __name__ == '__main__':
    branch = 'feature/auto-implementation-demo'
    files = {'AUTO.md': '# Auto changes\nThis file was created by Agent-Engineer demo.'}
    pr = create_branch_and_pr(branch, files, 'Auto: Demo PR', 'This PR was created by Agent-Engineer template.')
    print('PR created:', pr.html_url)
