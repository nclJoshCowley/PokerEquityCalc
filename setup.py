"""
Poker Equity Calculator, work in progress.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pokerequitycalc",
    version="0.0.1",
    author="Josh Cowley",
    author_email="josh.cowley@hotmail.com",
    description="Equity calculator for Poker hands.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="local",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)