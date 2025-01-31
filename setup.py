from setuptools import setup,find_packages
from typing import List



setup(
    name='sensor',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'joblib',
        ],
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