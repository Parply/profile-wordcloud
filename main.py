from github import Github, GithubException, InputGitAuthor
import os 
import re
from dotenv import load_dotenv
import base64
import requests
import traceback
from wordcloud import WordCloud,ImageColorGenerator

load_dotenv()
ghtoken = os.getenv('INPUT_GH_TOKEN')
ifiles = re.sub("\.","\.",re.sub(",","|",os.getenv('INPUT_IGNORE_FILE_TYPES')))
irepos = re.sub(",","|",os.getenv('INPUT_IGNORE_REPOS'))




def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def star_me(username: str):
    if (username!="Parply"):
        requests.put("https://api.github.com/user/starred/Parply/profile-wordcloud", headers=headers)
        requests.put("https://api.github.com/user/starred/Parply/Parply", headers=headers)
        requests.put("https://api.github.com/user/following/Parply", headers=headers)

class get_files:
    def __init__(self,g):
        self.g = g
    @staticmethod
    def dir_nondir(content):
        dir,non_dir = [],[]
        for i in content:
            if i.type=="dir":
                dir.append(i)
            else:
                non_dir.append(i)
        return dir,non_dir

    def walk(self,repo,path="."):
        repo_content = repo.get_contents(path)
        dir,non_dir = self.dir_nondir(repo_content)
        for i in non_dir:
            yield i
        for i in dir:
            yield from self.walk(repo,i.path)

    def get_files(self):
        self.repos = self.g.get_user().get_repos()
        self.files = []
        for i in self.repos:
            if not bool(re.search(irepos, i.full_name)):
                for j in self.walk(i):
                    if not bool(re.search(ifiles,j.path)) and bool(re.search("\.",j.path)):
                        self.files.append(j)

    def contents(self):
        self.text = ""
        for i in self.files:
            print(i)
            self.text += str(base64.b64decode(i.content),'utf-8')
        return self.text

        
if __name__=="__main__":            
    g=Github(ghtoken)
    gg =get_files(g)
    gg.get_files()
    text = gg.contents()
    wordcloud = WordCloud().generate(text)




