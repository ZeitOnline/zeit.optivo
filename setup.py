from setuptools import setup, find_packages

setup(
    name='zeit.optivo',
    version='1.0.0b2.dev0',
    author='gocept',
    author_email='mail@gocept.com',
    url='https://bitbucket.org/gocept/zeit.optivo',
    description="Optivo SOAP-API client for sending emails",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='gocept proprietary',
    namespace_packages=['zeit'],
    install_requires=[
        'setuptools',
        'suds',
        'zope.cachedescriptors',
        'zope.component',
        'zope.interface',
    ],
)
