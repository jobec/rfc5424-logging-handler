from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()
with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

setup(
    name='rfc5424-logging-handler',
    version='1.1.2',
    packages=find_packages(),
    author='Joris Beckers',
    author_email='joris.beckers@gmail.com',
    url="https://github.com/jobec/rfc5424-logging-handler",
    download_url="https://pypi.python.org/pypi/rfc5424-logging-handler",
    description='An up-to-date, RFC5424-Compliant syslog handler for the Python logging framework',
    long_description=readme + '\n\n' + changelog,
    license="BSD",
    keywords='python logging handler syslog rfc5424',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Development Status :: 5 - Production/Stable',
    ],
    install_requires=[
        'tzlocal',
        'pytz',
    ],
    tests_require=[
        'pytest',
        'mock',
    ],
    zip_safe=False,
)
