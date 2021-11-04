from setuptools import setup, find_packages

setup(
    name='hoopscrapper',
    version='1.0.0',
    url='https://github.com/raihan0824/hoopscrapper',
    author='Raihan Afiandi',
    author_email='mraihanafiandi@gmail.com',
    description='Get any desired NBA data!',
    packages=find_packages(),    
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
)
