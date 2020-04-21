import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "H2OLogFileAnalyzer",
    version = "1.0",
    author = "Jasmine Parekh",
    author_email = "jparekh2@terpmail.umd.edu",
    description = ("This CLI takes in a log file to analyze and graph with annotations"),
    long_description=read('README.md'),
    install_requires=['click',  'matplotlib', 'pandas', 'numpy']
)