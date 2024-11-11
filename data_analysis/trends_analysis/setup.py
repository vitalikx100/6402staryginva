from setuptools import setup, find_packages

setup(
    name='analysis_trends_package',
    version='0.1',
    packages=find_packages(where="trends_analysis/analysis_trends_package"),
    package_dir={'': 'trends_analysis/analysis_trends_package'},
    install_requires=['pytrends', 'pandas', 'matplotlib'],
    description='Time series analysis of search trends',
    author='Vitaliy Starygin',
)
