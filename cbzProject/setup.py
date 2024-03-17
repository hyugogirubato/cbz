from setuptools import setup, find_packages

setup(
    name='cbz',
    version='3.2.0',
    author='hyugogirubato',
    author_email='hyugogirubato@gmail.com',
    description='CBZ is a Python package designed to facilitate the creation, manipulation, and extraction of comic book archive files in the CBZ format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hyugogirubato/cbz',
    packages=find_packages(),
    license='GPL-3.0-only',
    keywords=[
        'metadata',
        'manga',
        'comics',
        'ebooks',
        'cbz',
        'webtoons'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ],
    install_requires=[
        'requests',
        'xmltodict',
        'langcodes',
        'Pillow'
    ],
    python_requires='>=3.7'
)
