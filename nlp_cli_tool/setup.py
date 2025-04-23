from setuptools import setup, find_packages

setup(
    name="easyshell",  # Your package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
    ],
    license="MIT",
    author="Zaima",
    author_email="mashaitzama@gmail.com",
    description="A command-line tool for various system operations",
    long_description="This project is a Natural Language Processing (NLP)-powered CLI...",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nlp_cli_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
     entry_points={  # Add this section to enable command-line functionality
        'console_scripts': [
            'easyshell=nlp_cli_tool.main:main',  # Modify this to point to your main function
        ],
    },
)
