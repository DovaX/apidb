import setuptools
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='apidb',
    version='0.2.0',
    author='DovaX',
    author_email='dovax.ai@gmail.com',
    description='Autogenerate API based on DB structure directly from Python using ORM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DovaX/apidb',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'fastapi','flask','dbhydra'
     ],
    python_requires='>=3.6',
)
    