<!-- ![alt text](http://image.png) -->

# The Project
This project uses the [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html), an Amazon Toolkit to define IaC (Infrastructure as Code) by using some of the most common languages. AWS CDK converts the implemented code to CloudFormation (which uses an AWS syntax to describe and provision all the infrastructure resources in AWS).

Most of the documentation about AWS CDK is focused on typescript. As *Python* is one of the most used languages, we have opted to use the Python CDK SDK. This project will be helpful for other projects implemented in Python.

In this project we have focused on the deployment of a simple serverless infrastructure. It deploys the following AWS services:
* API Gateway
* Lambda
* DynamoDB
* S3

The goal is not only deploying a simple infrastructure we can use in other projects but also using specific aspects not necessarily need in this project but might be useful in other more complex projects or with a specific purpose. Even if we have opted for a serverless infrastructure, the project can be easily adapted to a non-serverless architecture. 


# Howto

We show below not only the commands needed to deploy this project but also additional instructions to start a project from stratch.

## Create a project from scratch
In order to create a project from scratch, use the following command:
```
$ cdk init --language python app
```
Install python libraries:
```
$ pip install -r requirements.txt
```

## Set up

This project is set up like a standard Python project. 

The CDK initialization process shown above creates a virtualenv within this project, stored under the .env directory.  To create the virtualenv it assumes that there is a `python3` (or `python` for Windows) executable in your path with access to the `venv` package. 

If, for any reason, the automatic creation of the virtualenv fails, you can create the virtualenv manually, as shown below.

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

## Generate CloudFormation templates

You can synthesize the CloudFormation template for this code.

```
$ cdk synth
```

## Deploy Stack

As shown in [this page](https://cdkworkshop.com/30-python/20-create-project/500-deploy.html), the first time you deploy an AWS CDK app into an environment (account/region), you’ll need to install a `bootstrap stack`. This stack includes resources that are needed for the toolkit’s operation. For example, the stack includes an S3 bucket that is used to store templates and assets during the deployment process.

```
$ cdk bootstrap
```

To deploy the infrastructure in AWS, once the templates have been generated, use the following command:

```
$ cdk deploy
```

## Other useful commands

 * `cdk ls`: List all stacks in the app
 * `cdk destroy`: Destroyed the stack deployed
 * `cdk diff`: Compare deployed stack with current state
 * `cdk docs`: Open CDK documentation


# Structure

The relevant files for this project as the following:

* `app.py`: The main for the application
* `cdk.json`: A configuration file that defines how to execute the application.
* `README.md`: This README file.
* `requirements.txt`: It tells pip to install the requirements specified in setup.py.
* `setup.py`: It defines how the package is constructed and its dependencies.
* `cdk.out/*`: When `cdk synth` is executed, CloudFormation templates are placed under this directory. Those files are used for deploying the insfrastrure with `cdk deploy` 
* `serverless/*`: The project itself, where source code is placed.
    * `serverless/params/*`: Configuration file, where we define the infrastructure parameters
    * `serverless/lib/*`: Library files, i.e. custom constructors.
    * `serverless/serverless_stack.py`: Main stack file where we define which resources to build.

