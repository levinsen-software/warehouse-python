from distutils.core import setup
setup(
    name = 'warehouse-client',
    packages = ['warehouse'],
    version = '1.0',
    license='MIT',
    description = 'Client library to interact with levinsen software warehouse artifact management system.',
    maintainer = 'levinsen software',
    maintainer_email = 'opensource@levinsen.software',
    url = 'https://gitlab.com/levinsen-software/warehouse-python',
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