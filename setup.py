#!/usr/bin/python
# -*- coding: utf-8 -*-
import setuptools
import sys
import metexpy


def main():
    
    setuptools.setup(name="metexpy",
        version=metexpy.__version__,
        description="Python package to search, extract and rename metabolite and lipid names using regular expression.",
        long_description=open('README.rst').read(),
        author="Ralf Weber",
        author_email="r.j.weber@bham.ac.uk",
        url="https://github.com/computational-metabolomics/metexpy",
        license="GPLv3",
        platforms=['Windows, UNIX'],
        keywords=['Metabolomics', 'Lipidomics', 'Metabolites', 'Lipids', 'Annotation', 'Identification'],
        packages=setuptools.find_packages(),
        test_suite='tests.suite',
        python_requires='>=3.7',
        install_requires=open('requirements.txt').read().splitlines(),
        include_package_data=True,
        classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Topic :: Scientific/Engineering :: Bio-Informatics",
          "Topic :: Scientific/Engineering :: Chemistry",
          "Topic :: Utilities",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
        ],
        entry_points={
         'console_scripts': [
             'metexpy = metexpy.__main__:main'
         ]
        }
    )


if __name__ == "__main__":
    main()
