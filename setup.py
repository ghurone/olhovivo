from setuptools import setup, find_packages

setup(
    name='olhovivo',
    version='0.1.2',
    author='Erick Ghuron',
    author_email='ghuron@usp.br',
    description='API para o OlhoVivo da SPTrans',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
