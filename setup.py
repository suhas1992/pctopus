# setup.py
from setuptools import setup, find_packages

setup(
    name="pctopus",
    version="0.1.0",
    packages=find_packages(),
    author="Suhas Suresha",
    author_email="suhas17@stanford.edu",
    description="A package for building AI agents that can understand and control your PC",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/suhas1992/pctopus",
    classifiers=[],
    python_requires=">=3.11",
)