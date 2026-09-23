from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent

setup(
    name="phantom-osint",
    version="1.0.1",
    description="A command-line OSINT research helper for usernames, emails, phones, and IP addresses",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="f1shnc1ps",
    url="https://github.com/f1shnc1ps/stalker",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "httpx>=0.23.0",
        "pydantic>=1.10.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "pyyaml>=6.0",
    ],
    entry_points={"console_scripts": ["phantom=phantom.cli:main"]},
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
