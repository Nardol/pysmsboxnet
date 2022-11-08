"""The setup script."""
from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="pysmsboxnet",
    version="1.0A1",
    description="Client to send SMS using www.smsbox.net API",
    author="Patrick ZAJDA",
    author_email="patrick@zajda.fr",
    packages=find_packages(include=["pysmsboxnet"]),
    install_requires=[
        "aiohttp>=3.8.0,<4.0",
    ],
    license="MIT license",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Framework :: AsyncIO",
        "Framework :: aiohttp",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Communications",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["smsbox", "api", "sms"],
    long_description_content_type="text/markdown",
    long_description=readme,
    python_requires=">=3.8.0",
    url="https://github.com/Nardol/pysmsboxnet",
)
