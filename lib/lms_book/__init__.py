import os
import yaml
import logging
from git import Repo
from enum import Enum
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("lms-book")
LOGGER.setLevel("INFO")


class LMSBookCommand(Enum):
    create = "create"
    pull = "pull"
    publish = "publish"
    sync = "sync"

    @classmethod
    def from_str(cls, command: str):
        command = command.lower()
        return LMSBookCommand[command]


default_toc_yml_path = Path(__file__).parent.parent.parent.joinpath("_toc.yml")


def save_toc(toc: List[Dict], toc_yml_path: Path):
    output_str = ""
    output_str += "- {key}: {value}\n".format(key="file", value=toc[0]["file"])
    for part in toc[1:]:
        print(part)
        output_str += "- {key}: {value}\n".format(key="part", value=part["part"])
        if "chapters" in part:
            output_str += "  chapters:\n"
            for file in part["chapters"]:
                output_str += "    - {key}: {value}\n".format(key="file", value=file["file"])
    with open(str(toc_yml_path), "w") as f:
        f.write(output_str)
    LOGGER.info("toc saved to: {}".format(str(toc_yml_path)))


def read_toc(toc_yml_path: Path = None) -> List[Dict]:
    toc_yml_path = default_toc_yml_path if toc_yml_path is None else toc_yml_path
    LOGGER.info(" Reading toc from: {}".format(str(toc_yml_path)))
    with open(str(toc_yml_path)) as f:
        toc = yaml.load(f, Loader=yaml.FullLoader)
    return toc


def create_part(part_name: str, toc_yml_path: Path = None):
    toc = read_toc(toc_yml_path)
    LOGGER.info(" Creating part: {}".format(part_name))
    toc.append({"part": part_name})
    save_toc(toc, toc_yml_path)


def create_chapter(part_name: str, file_path: str, toc_yml_path: Path = None, save_to_pull_script: bool = False):
    LOGGER.info(" Creating chapter for part: {}".format(part_name))

    toc = read_toc(toc_yml_path)
    part_index = 0
    for i, part in enumerate(toc):
        if i == 0:
            continue
        if part["part"] == part_name:
            part_index = i

    # if not part in toc has the part_name, then create a new part
    if part_index == 0:
        create_part(part_name, toc_yml_path)
        toc = read_toc(toc_yml_path)
        part_index = len(toc) - 1
    part = toc[part_index]
    if "chapters" not in part:
        part["chapters"] = []
    if file_path.startswith("http"):
        file_path = pull(file_path, toc_dir=toc_yml_path.parent, save_to_pull_script=save_to_pull_script)
    else:
        # touch a file at file_path, and notifying user to go there for further edit
        if not default_toc_yml_path.parent.joinpath(file_path).exists():
            default_toc_yml_path.parent.joinpath(file_path).touch()
            LOGGER.info(" Created a new empty file at: {}".format(str(default_toc_yml_path.parent.joinpath(file_path))))
            LOGGER.info(" Please navigate to that location to edit. "
                        "Afterwards use lms-book publish to publish your new chapter")

    part["chapters"].append({"file": file_path})
    save_toc(toc, toc_yml_path)


def pull(url: str, file_dir: str = None, toc_dir: Path = None, save_to_pull_script: bool = True):
    """
    file_dir is relative to root repo dir (toc dir), i.e. 4Dsurvival/data. If is None, then will interpret from url.
    We assume url follow the following structure:
     http://xxx.com/{user_name/project_name}/{repo_name}/{branch}/{file_dir}/{file_name}
    """
    url_path = urlparse(url).path
    url_parts = url_path.split("/")
    if file_dir is None:
        repo_name = url_parts[2]
        file_dir = [repo_name]
        file_dir.extend(url_parts[4:-1])
        file_dir = "/".join(file_dir)
    file_name = url_parts[-1]
    file_path = "/".join([file_dir, file_name])
    toc_dir = default_toc_yml_path.parent if toc_dir is None else toc_dir
    abs_file_dir = str(toc_dir.joinpath(file_dir))
    wget_command = "wget {url} -P {file_dir} -N --no-check-certificate".format(url=url, file_dir=abs_file_dir)
    LOGGER.info(" Executing wget: {}".format(wget_command))
    os.system(wget_command)
    # add wget command to pull repo readmes
    if save_to_pull_script:
        with open(str(toc_dir.joinpath("pull_repo_readmes")), "r") as f:
            script = f.read()
        with open(str(toc_dir.joinpath("pull_repo_readmes")), "w") as f:
            wget_command = "wget {url} -P {file_dir} -N --no-check-certificate".format(url=url, file_dir=file_dir)

            script += wget_command + "\n"
            f.write(script)
    return file_path


def publish(message: str):
    repo = Repo(str(default_toc_yml_path.parent))
    if len(repo.index.diff(None)) > 0 or len(repo.untracked_files) > 0:
        change_files = []
        for diff in repo.index.diff(None):
            LOGGER.info(" Adding unstaged file: {}".format(diff.a_path))
            change_files.append(diff.a_path)
        for file in repo.untracked_files:
            LOGGER.info(" Adding untracked file: {}".format(file))
            change_files.append(file)
        repo.index.add(change_files)
        repo.index.commit(message)
        LOGGER.info(" Commit message: {}".format(message))
        LOGGER.info(" Pushing to remote...")
        repo.remotes.origin.push()


def sync():
    LOGGER.info(" Pulling from remote...")
    repo = Repo(str(default_toc_yml_path.parent))
    repo.remotes.origin.pull()
    LOGGER.info(" Pulling READMEs from other repos using pull_repo_readmes script...")
    os.system("bash {}".format(str(default_toc_yml_path.parent.joinpath("pull_repo_readmes"))))
