# lms-book

This repo contains all the documentations (markdown, notebooks, images etc) inside `doc` directory, and `lms-book` tool
to create, publish and sync contents (inside `lib` directory, installation guide in below). `_toc.yml` specifies the 
structure of the book with reference to each documentation path. `pull_repo_readmes` is a shell script to pull
all readmes from other github repos (or you could use `lms-book sync` command in CLI after installation). 

## lms-book tool
To make it easier to create, sync and publish documentations, we created `lms-book` tool,
that you can run in command line.

### Installation
```
cd {lms-book_dir}
pip install -r requirements.txt
python setup.py develop
```

Noted that make sure `python` is python3.5+. If you have both python 2 and 3 install. Try `python3 setup.py develop`
instead.
### commands
lms-book contains the following commands:
```
lms-book sync
lms-book create part {part_name}
lms-book create chapter {part_name} {file_path}
lms-book pull {url} {file_dir}
lms-book publish {message}
```

After installation, you can run these command using bash shell, command prompt or git bash anywhere.

  - `sync`
  
    This sync your local book with remote book in github. It is equivalent to 
    ```
    git pull
    bash ./pull_repo_readmes (or cmd < pull_repo_readmes in windows)
    ```
    Please remember to always do this first before you make changes and publish to remote.
  
    ```
    lms-book sync
    ```     
  - `create`
    
    This is used to create a new `part` or `chapter`.
    
    - To create a new part:
  
        ```
        lms-book create part {part_name}
        ```
    
    - To create a new chapter, we have 3 option: from url, from an existed local file, from a new file:
  
        ```
        lms-book create chapter {part_name} {file_path}
        
        part_name can be an existed part or a new part.
        file_path can be an url to github raw content or a local file (relative to repo dir).
        ```
    
        - To create a new chapter from url, simply use the url as input to the above command, such as
            ```
            lms-book create chapter AutoFD https://raw.githubusercontent.com/UK-Digital-Heart-Project/AutoFD/master/README.md
          
            ```
            
            This will do 4 things:
            ```
            1. create a new part AutoFD if not exist in _toc.yml
            2. use wget to pull remote readme and save to {repo_name}/{file_path}. In this case, ./AutoFD/README.md
            3. save the wget command to pull_repo_readmes
            4. add the new chapter AutoFD/README.md to _toc.yml
            ```
        - To create a new chapter from a existed file
          
          Make sure that the file is inside the repo. Then simply run the above command.
          ```
          lms-book create chapter AutoFD AutoFD/README.md
          ```
        
        - To create a new chapter and a new file (`new_file.md`)
          ```
          lms-book create chapter AutoFD AutoFD/new_file.md
          ```
          
          A new empty file will be created. Now you need to navigate to that file path, make your changes,
          then use `lms-book publish {msg}` to commit and publish your new file.
          
  - `pull`
    
    This pull a file from url using `wget`, and store the `wget` command in `pull_repo_readmes`
    
    ```
    lms-book pull {url} {file_dir}
    file_dir is relative to local repo dir.
    ```
  - `publish`
    ```
    lms-book publish {message}
    ```
    This commit your changes, and publish to remote. It is equivalent to 
    ```
    git add .
    git commit -m "{message}"
    git push
    ```


## _toc.yml
This file specify the table of content of our book. 

Please do not run `jupyter-book toc .` at any time as this will overwrite `_toc.yml`.

## pull_repo_readmes
Bash script `./pull_repo_readmes` shows two example of how to use `wget` to download README and images used in README from github 
public repo, and place it under desired directory. `-N` option makes sure that only newer file in remote repo
will overwrite the existed local file. 

Notice that, in each README, it must have only one title (prefix with #).


## Netfliy deploy command
After you publish your changes, a web service Netlify will automatically deploy the new documentation book.

Below is the deploy command used. 
```
pip install -r requirements.txt && python setup.py develop && lms-book sync && jupyter-book build .
```
    
