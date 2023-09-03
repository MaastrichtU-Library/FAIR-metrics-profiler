from setuptools import setup, find_packages

setup(
    name='fair_metrics_profiler',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'xlwt'
    ],
    url='https://github.com/yourusername/fair_metrics_profiler',
    license='MIT',
    author='Pedro V Hernandez Serrano',
    author_email='p.hernandezserrano@maastrichtuniversity.nl',
    description='A Python package to evaluate and generate reports on FAIR metrics for DOIs'
)
