from setuptools import setup, find_packages


setup(
    name='zeit.optivo',
    version='1.1.3.dev0',
    author='gocept, Zeit Online',
    author_email='zon-backend@zeit.de',
    url='http://www.zeit.de/',
    description="Optivo SOAP-API client for sending emails",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    namespace_packages=['zeit'],
    install_requires=[
        'setuptools',
        'zeep',
        'zope.cachedescriptors',
        'zope.component',
        'zope.interface',
    ],
)
