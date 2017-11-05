from setuptools import setup, find_packages

setup(
    description='Download Easy German videos and transcripts',
    name='easygerman',
    packages=find_packages(),
    install_requires=[
        'requests==2.18.1',
        'google-api-python-client==1.6.2',
        'youtube-dl==2017.6.18',
        'pytest==3.2.3',
    ],
    url='https://github.com/family-guy/easy-german',
    author='Guy King',
    author_email='guy@zorncapital.com',
    version='0.1.2'
)
