# Profile Wordcloud ☁️

<p align="center">
<a href="https://github.com/Parply/Parply"><img src="https://github.com/Parply/readme-badge-colouriser/blob/master/.github/wordcloud.png?raw=true" alt="Example" width="100%"/></a>
</p>

---

<p align="center">
   <img src="https://img.shields.io/badge/language-python-blue?style"/>
   <img src="https://img.shields.io/github/license/Parply/profile-wordcloud"/>
   <img src="https://img.shields.io/github/stars/Parply/profile-wordcloud"/>
   <img src="https://img.shields.io/github/forks/Parply/profile-wordcloud"/>
   <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
</p>

<p align="center">
    <a href="https://github.com/Parply/readme-badge-colouriser/issues">Report Bug</a>
    ·
    <a href="https://github.com/Parply/readme-badge-colouriser/issues">Request Feature</a>
  </p>

## Prep Work

1. You need to update the markdown file(.md) with 2 comments. You can refer [here](#update-your-readme) for updating it.
2. You'll need a GitHub API Token with `repo` and `user` scope from [here](https://github.com/settings/tokens)
   > enabling the `repo` scope seems **DANGEROUS**<br/>
   > but this GitHub Action only will allow committing the updated readme.
   - You can use [this](#profile-repository) example to work it out
3. You need to save the GitHub API Token in the repository secrets. You can find that in the Settings of your repository. Be sure to save those as the following.
    - GitHub Personal Access Token as `GH_TOKEN=<your github access token>`
4. You can enable and disable feature flags based on requirements [here](#additional-flags). The only required flag is the GitHub API token.

This Action is best run on every push but dont worry it will only commit when colours are updated.

## Update your Readme

Add a comment to your `README.md` like this:

```md
<!--START_SECTION:wordcloud-->
<!--END_SECTION:wordcloud-->
```

These lines will be our entry-points for where the wordcloud will be placed. An example can be seen <a href="https://github.com/Parply/Parply/blob/master/README.md">here</a>.

### Profile Repository

You'll need to get a [GitHub Access Token](https://docs.github.com/en/actions/configuring-and-managing-workflows/authenticating-with-the-github_token) with a `repo` and `user` scope and save it in the Repo Secrets `GH_TOKEN = <Your GitHub Access Token>`

Here is Sample Workflow File for running it:

```yml
name: WordCloud

# everday at 00:00 UTC.
on: 
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'

jobs:
  update-readme:
    name: Update Readme with WordCloud
    runs-on: ubuntu-latest
    steps:
      - uses: Parply/profile-wordcloud@master
        with:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

## Extras

If you want to ignore certain file or repos or other options, you can add multiple `FLAGS` in your workflow file.

```yml
- uses: Parply/readme-badge-colouriser@master
      with:
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
        CMAP: "flag"
        AUTHOR: "Parply"
```

### Additional Flags

---

- `IGNORE_FILE_TYPES` 	Comma seperated string of file types to ignore.  Defaults to `".pdf,.o,.csv"`

- `IGNORE_REPOS` 		Comma seperated string of repositories to ignore. Defaults to `""`

- `WIDTH` 	Width to set image. Defaults to `"100%"`

- `CMAP` 		Colourmap to use for colouring words. Uses [matplotlib's colormaps](https://matplotlib.org/3.3.1/tutorials/colors/colormaps.html). Defaults to `"hsv"` 

- `AUTHOR` 	Name of the author committing to the readme. Defaults to `wordcloud bot`

- `BRANCH` 	Branch to commit to. Defaults to `master`



----

Made with Python 🐍.

