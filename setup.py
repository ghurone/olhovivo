from setuptools import setup, find_packages
import olhovivo

setup(
name='olhovivo',
version=olhovivo.__version__,
author='Erick Ghuron',
author_email='ghuron@usp.br',
description='API para o OlhoVivo da SPTrans',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'Operating System :: OS Independent',
],
python_requires='>=3.7',
)
