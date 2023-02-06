"""Setup module"""

from setuptools import setup

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='pycbzhelper',
    version='3.0.1',
    description='Python library to create a cbz file with metadata.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/hyugogirubato/pycbzhelper',
    author='hyugogirubato',
    author_email='hyugogirubato@gmail.com',
    license='GNU GPLv3',
    packages=['pycbzhelper'],
    install_requires=['json2xml', 'langcodes', 'pillow'],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
    ]
)
