from setuptools import setup, find_packages
# 
#  pip install -e .
# test: python -c "import common.data_fetching; print('Setup successful!')"
# sudo apt install libcairo2-dev pkg-config python3-dev
setup(
    name="NOCOS",  # Project name
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        line.strip() for line in open("requirements.txt") if line.strip() and not line.startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "run_miz=scripts.run_miz:main",
            "run_msp=scripts.run_msp:main",
            "run_rio=scripts.run_rio:main",
            "run_all=scripts.run_all:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="NOCOS project for multi-application data fetching and processing.",
    url="https://github.com/CSCfi/NOCOS",  # Change if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Adjust based on your Python version
)
