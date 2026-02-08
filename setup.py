from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emerald-shadows",
    version="1.0.0",
    author="Red4Golf",
    description="A detective text adventure game set in 1947 post-war Seattle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/red4golf/emerald-shadows",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
            "mypy>=1.5.1",
            "black>=23.7.0",
            "isort>=5.12.0",
            "flake8>=6.1.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "emerald-shadows=emerald_shadows.main:main",
        ],
    },
)