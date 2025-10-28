from setuptools import setup, find_packages

setup(
    name="pssgplot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # Ensures non-code files like fonts are included
    install_requires=[
        # Add dependencies from requirements.txt or list them here, e.g.,
        # "matplotlib>=3.4.0",
        # "numpy>=1.21.0"
    ],
    package_data={
        "pssgplot": ["../fonts/*.ttf"],  # Include the fonts in the package
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python plotting library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
