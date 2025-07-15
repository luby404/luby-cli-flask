from setuptools import setup, find_packages

setup(
    name='luby',
    version='0.0.1',
    author='Ricardo Cayoca',
    description='Gerador de projetos Flask',
    py_modules=['luby'],
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'luby = luby:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
