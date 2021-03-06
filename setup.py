import setuptools

# This file has been generated with the command 'cdk init'
# However, it has been slightly adapted 
with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="serverless",
    version="0.0.1",

    description="Serverless Application for a PoC to test CDK",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Ronald T. Fernandez (Ronald Teijeira Fernandez)",

    package_dir={"": "serverless"},
    packages=setuptools.find_packages(where="serverless"),

    install_requires=[
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
