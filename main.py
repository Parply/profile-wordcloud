from github import Github, GithubException, InputGitAuthor
import os 
import re
from dotenv import load_dotenv
import base64
import requests
import traceback
from wordcloud import WordCloud,ImageColorGenerator
from matplotlib import pyplot as plt

load_dotenv()
ghtoken = os.getenv('INPUT_GH_TOKEN')
ifiles = re.sub("\.","\.",re.sub(",","|",os.getenv('INPUT_IGNORE_FILE_TYPES')))
irepos = re.sub(",","|",os.getenv('INPUT_IGNORE_REPOS'))
WIDTH = os.getenv('INPUT_WIDTH')

START_COMMENT = '<!--START_SECTION:wordcloud-->'
END_COMMENT = '<!--END_SECTION:wordcloud-->'
listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"

userInfoQuery = """
{
    viewer {
      login
      id
    }
  }
"""

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
def decode_readme(data: str):
    '''Decode the contents of old readme'''
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, 'utf-8')
def generate_new_readme(readme: str,username : str):
    '''Generate a new Readme.md'''
    r1 = f"<p align='center'><img src='https://raw.githubusercontent.com/{username}/{username}/master/wordcloud/wordcloud.png' alt='Maths and Programming Addict' width='{WIDTH}'/></p>"
    r = f"{START_COMMENT}\n {r1} \n {END_COMMENT}"
    return re.sub(listReg,r,readme)  
if __name__=="__main__":            
    try:
        g=Github(ghtoken)
        gg =get_files(g)
        gg.get_files()
        text = gg.contents()
        wordcloud = WordCloud(background_color=None,mode="RGBA").generate(text)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud,interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud.png")
        user_data = run_query(userInfoQuery) 
        username = user_data["data"]["viewer"]["login"]
        id = user_data["data"]["viewer"]["id"]
        print(username)
        star_me(username)
        repo = g.get_repo(f"{username}/{username}")
    
        committer = InputGitAuthor('wordcloud bot', 'wordcloud-bot@example.com')
        with open('wordcloud.png', 'rb') as input_file:
            data = input_file.read()
        try:
            contents = repo.get_contents("wordcloud/wordcloud.png")    
            repo.update_file(contents.path, "WordCloud Updated", data, contents.sha, committer=committer)
        except Exception as e:
            repo.create_file("wordcloud/wordcloud.png", "WordCloud Added", data, committer=committer)


        contents = repo.get_readme(ref=branch)
        rdmd =decode_readme(contents.content)
        new_readme = generate_new_readme(rdmd, username)
        if new_readme != rdmd:
            repo.update_file(path=contents.path, message="Added Wordcloud",
                             content=new_readme, sha=contents.sha, branch=branch,
                             committer=committer)
            print("Readme updated")
    
    except Exception as e:
        traceback.print_exc()
        print("Exception Occurred " + str(e))

