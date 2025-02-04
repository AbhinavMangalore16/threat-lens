from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function would fetch the project requirements from the requirements.txt file
    """
    try: 
        with open('requirements.txt') as f:
            lines = f.readlines()
            req_list = []
            for l in lines: 
                req = l.strip()
                if req and req != '-e .':
                    req_list.append(req)
    except FileNotFoundError:
        print("Requirements.txt not found!")
    
    return req_list

setup(
    name= "threat-lens",
    version= "0.1",
    author = "Abhinav Mangalore",
    author_email="abhinavm16104@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)
