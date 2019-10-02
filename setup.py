from setuptools import setup

setup(
    name='Snapshot Analyser',
    version='0.1',
    author= "Kavitha Raja",
    author_email = "raja.kavi@gmail.com",
    Description = "snapshot analyser is a tool to manage EC2 instances, Volumes and Snapshot",
    license ="GPLv3+",
    packages=['shotty'],
    url= "https://github.com/kaviraja81/snapshot-analyser",
    install_requires = [
    'click',
    'boto3'],
    entry_points ='''
     [console_scripts]
     shotty=shotty.shotty:cli
     '''


)
