from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prc_sdk",
    version="0.1.0",
    author="zenturocloud",
    author_email="info@zenturo.cloud",
    description="A Python SDK for interacting with the PRC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zenturocloud/prc-roblox-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/zenturocloud/prc-roblox-sdk-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={"": "prc_sdk"},  # Updated: Changed from "src" to "prc_sdk"
    packages=find_packages(where="prc_sdk"),  # Updated: Changed from "src" to "prc_sdk"
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="prc, roblox, api, sdk",
)
