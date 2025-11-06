from setuptools import setup,find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-PROJECT-1",
    version = "0.1",
    author="Dilara Isikli",
    packages=find_packages(),  # we have utils,src and config as a package, it will find them automatically
    install_requires = requirements
)

#to run setup file, use pip install -e .
# it will run your dependicises utils,src and config packages and requirement.txt
#then there will be another folder created, ---1.egg-info - all packages information you will have