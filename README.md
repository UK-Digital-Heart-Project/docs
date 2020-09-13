# How to use Jupyter book

### _toc.yml
This file specify the table of content of our book. 

Please do not run `jupyter-book toc .` at any time as this will overwrite `_toc.yml`.

### How READMEs are pulled from other repos
Bash script `./pull_repo_readmes` shows two example of how to use `wget` to download README and images used in README from github 
public repo, and place it under desired directory. `-N` option makes sure that only newer file in remote repo
will overwrite the existed local file. 

Notice that, in each README, it must have only one title (prefix with #).


### Netfliy deploy command
```
pip install -r requirements.txt && bash ./pull_repo_readmes && jupyter-book build .
```