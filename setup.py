"""
Setup script for Code Quality Assessment Tool.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-quality-assessment",
    version="1.0.0",
    author="Your Name",
    description="Tool for automatic assessment of Python code quality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=3.0.0",
        "flake8>=4.0.0",
        "black>=22.0.0",
    ],
    entry_points={
        "console_scripts": [
            "code-quality=src.main:main",
        ],
    },
)

