#!/usr/bin/env python
import os, errno, shutil, stat, git

repo_a_url = 'https://github.com/rrmavani/repo_a.git'
repo_b_url = 'https://github.com/rrmavani/repo_b.git'

repo_a_path = "../repo_a/"
repo_b_path = "../repo_b/"

#Some functions
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
    os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
    func(path)
  else:
    raise

def remove_repo(repo_path):
  mydir = repo_path
  if os.path.isdir(mydir):
    try:
        shutil.rmtree(mydir, ignore_errors=False, onerror=handleRemoveReadonly)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

#Main Function
def main():
  #Some variables definations
  repo_dict = { "repo_a_path": repo_a_path, "repo_a_url": repo_a_url, "repo_b_path": repo_b_path, "repo_b_url": repo_b_url }
  repo_commits = {"repo_a_commits": [], "repo_b_commits": []}
  repo_commits_details = {"repo_a_commits": {}, "repo_b_commits": {}}

  #Remove and Clone repositories
  for repo_iter in ("repo_a", "repo_b"):
    remove_repo(repo_dict[f"{repo_iter}_path"])
    repo = git.Repo.clone_from(repo_dict[f"{repo_iter}_url"], repo_dict[f"{repo_iter}_path"])
    commits = repo.iter_commits('main', max_count=50)
    #Fetch the commit details and populate to empty variables
    for commit in commits:
      repo_commits[f"{repo_iter}_commits"].append(commit.hexsha) 
      repo_commits_details[f"{repo_iter}_commits"][commit.hexsha] = {"hexsha": commit.hexsha, "message": commit.message.strip(), "author": commit.author, "committer": commit.committer, "datetime": commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")}
    repo.close

  print ("")
  print (f"Below commits not found in {repo_b_url}")
  print ("")

  #Compare the differences and Print
  for hex in repo_commits["repo_a_commits"]:
    if not hex in repo_commits["repo_b_commits"]:
      print(f'{repo_commits_details["repo_a_commits"][hex]["hexsha"]} - {repo_commits_details["repo_a_commits"][hex]["message"]} - {repo_commits_details["repo_a_commits"][hex]["datetime"]} - {repo_commits_details["repo_a_commits"][hex]["author"]} - {repo_commits_details["repo_a_commits"][hex]["committer"]}')
  
  print ("")
  print ("")

if __name__ == "__main__":
  main()
