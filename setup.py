from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='warehouse-client',
    packages=['warehouse'],
    version='1.0.4',
    license='MIT',
    description='Client library to interact with levinsen software warehouse artifact management system.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='levinsen software',
    author_email='opensource@levinsen.software',
    url='https://gitlab.com/levinsen-software/warehouse-python',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
