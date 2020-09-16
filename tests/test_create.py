import unittest
from lms_book import create_part, create_chapter
from tests import TEST_INPUT_DIR, TEST_OUTPUT_DIR
import shutil


class CreateCommandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_toc_yml_path = TEST_INPUT_DIR.joinpath("test_toc.yml")
        TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    def test_create_chapter(self):
        yml_path = TEST_OUTPUT_DIR.joinpath("test_toc.yml")
        if yml_path.exists():
            yml_path.unlink()
        shutil.copy(str(self.test_toc_yml_path), str(yml_path))
        # test if part name exists
        create_chapter("AutoFD", "file/readme.md", yml_path)
        with open(str(self.test_toc_yml_path)) as f:
            original_yml = f.read()
            original_yml += "    - file: file/readme.md\n"
        with open(str(yml_path)) as f:
            output_yml = f.read()
        self.assertEqual(original_yml, output_yml)
        yml_path.unlink()
        # test if part name not exists
        shutil.copy(str(self.test_toc_yml_path), str(yml_path))
        create_chapter("test_part", "file/readme.md", yml_path)
        with open(str(self.test_toc_yml_path)) as f:
            original_yml = f.read()
            original_yml += "- part: test_part\n  chapters:\n    - file: file/readme.md\n"
        with open(str(yml_path)) as f:
            output_yml = f.read()
        self.assertEqual(original_yml, output_yml)
        yml_path.unlink()
        # test if file_path is url
        shutil.copy(str(self.test_toc_yml_path), str(yml_path))
        create_chapter(
            part_name="test_part",
            file_path="https://raw.githubusercontent.com/UK-Digital-Heart-Project/4Dsurvival/master/data/DAE3.png",
            toc_yml_path=yml_path,
            save_to_pull_script=False,
        )
        img_path = TEST_OUTPUT_DIR.joinpath("4Dsurvival", "data", "DAE3.png")
        self.assertTrue(img_path.exists())
        with open(str(self.test_toc_yml_path)) as f:
            original_yml = f.read()
            original_yml += "- part: test_part\n  chapters:\n    - file: 4Dsurvival/data/DAE3.png\n"
        with open(str(yml_path)) as f:
            output_yml = f.read()
        self.assertEqual(original_yml, output_yml)
        img_path.unlink()
        yml_path.unlink()

    def test_create_part(self):
        yml_path = TEST_OUTPUT_DIR.joinpath("test_toc.yml")
        if yml_path.exists():
            yml_path.unlink()
        shutil.copy(str(self.test_toc_yml_path), str(yml_path))
        create_part("test_part", yml_path)
        with open(str(self.test_toc_yml_path)) as f:
            original_yml = f.read()
            original_yml += "- part: test_part\n"
        with open(str(yml_path)) as f:
            output_yml = f.read()
        self.assertEqual(original_yml, output_yml)
        yml_path.unlink()

    def tearDown(self) -> None:
        shutil.rmtree(str(TEST_OUTPUT_DIR), ignore_errors=True)
