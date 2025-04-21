from setuptools import setup, find_packages

setup(
    name="ml-pipeline-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "xgboost>=1.5.0",
        "imbalanced-learn>=0.8.0",
    ],
    entry_points={
        'console_scripts': [
            'mlpipeline=cli:cli',
        ],
    },
) 