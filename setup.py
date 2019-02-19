from setuptools import setup

description = 'Requests-based Python client to Portability Integration API'

try:
    with open('README.md') as f:
        long_description = f.read()
except IOError:
    long_description = description

setup(
    name = 'requests_portability',
    version = '0.1',
    description = description,
    author = 'Antonio Ognio',
    author_email = 'aognio@rcp.pe',
    url = 'https://git.yachay.pe/devteam/requests-portability',
    long_description = long_description,
    packages = ['requests_portability'],
    install_requires = ['requests >= 2.3.0', 'uritemplate >= 0.6'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
