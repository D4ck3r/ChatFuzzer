import git

def get_git_info(repo_path='.'):
    repo = git.Repo(repo_path, search_parent_directories=True)
    branch = repo.active_branch.name
    last_commit = repo.head.commit
    return {
        'branch': branch,
        'last_commit': {
            'hexsha': last_commit.hexsha,
            'author': last_commit.author.name,
            'summary': last_commit.summary,
            'date': last_commit.authored_datetime
        }
    }

# 使用当前目录作为仓库路径
git_info = get_git_info()
print("Current Branch:", git_info['branch'])
print("Last Commit:")
print("  SHA:", git_info['last_commit']['hexsha'])
print("  Author:", git_info['last_commit']['author'])
print("  Summary:", git_info['last_commit']['summary'])
print("  Date:", git_info['last_commit']['date'])
