# test
from setuptools import find_namespace_packages, setup

setup(
    name="lms_book",
    use_scm_version=True,
    description="Computational Imaging Documentation Book",
    package_dir={"": "lib"},
    packages=find_namespace_packages(where="lib"),
    setup_requires=["setuptools >= 40.0.0"],
    install_requires=[],
    package_data={"": ["*.conf", "*.yml", ".md"]},
    entry_points={
        'console_scripts': ['lms-book = lms_book.cli:main']
    },
)
