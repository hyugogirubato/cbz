from setuptools import setup, find_packages

setup(
    name="pycbzhelper",
    version="3.1.1",
    author="hyugogirubato",
    author_email="hyugogirubato@gmail.com",
    description="Python library for creating CBZ files with metadata.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hyugogirubato/pycbzhelper",
    packages=find_packages(),
    license="GPL-3.0-only",
    keywords=[
        "metadata",
        "manga",
        "comics",
        "ebooks",
        "cbz"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities"
    ],
    install_requires=[
        "requests",
        "json2xml",
        "langcodes",
        "Pillow"
    ],
    python_requires=">=3.7"
)
