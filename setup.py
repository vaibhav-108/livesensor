from setuptools import setup,find_packages
from typing import List

hypen_e= '-e .'


# def get_requirements()->List[str]:
#     """
#     This function will return list of requirements
#     """
#     requirement_list:List[str] = []

#     """
#     Write a code to read requirements.txt file and append each requirements in requirement_list variable.
#     """
#     return requirement_list

def get_requirements(file_path:str)->List[str]:
    
    requirement=[]
    with open(file_path, 'r') as f:
        requirement=f.readlines()
        requirement= [file.replace('\n','') for file in requirement]
        
    requirement_list=[f for f in requirement if f!=hypen_e]
    print (requirement_list)
    
    return requirement_list
    




setup(
    name='sensor',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'), 
    description='My custom Python package',
    author='vaibhav',
    author_email='vaibhav.b108@gmail.com',
    url='https://github.com/vaibhav-108/livesensor',
    # license='MIT',
    # classifiers=[
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9',
    
)