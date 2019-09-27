<!-- ![alt text](http://image.png) -->

# AWS CDK in Python
This project uses the [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html) (Cloud Development Kit), an Amazon Toolkit to define IaC (Infrastructure as Code) by using some of the most common languages. AWS CDK converts the implemented code to CloudFormation (which uses an AWS syntax to describe and provision all the infrastructure resources in AWS).

Most of the documentation about AWS CDK is focused on typescript. As *Python* is one of the most used languages, we have opted to use the Python CDK SDK. This project will be helpful for other projects implemented in Python.

## Description

In this project we have implemented a project that uses AWS CDK to deploy a simple AWS serverless infrastructure. It deploys the following AWS services:
* API Gateway
* Lambda
* DynamoDB
* S3

The goal is define a simple infrastructure we can use in other projects as well as introduce specific aspects (which might not necessarily be needed in this project but might be useful in other more complex projects or with a specific purpose). 

Even if we have opted for a serverless infrastructure, the project can be easily adapted to a non-serverless architecture. 


## Installation

We show below not only the commands needed to deploy this project but also additional instructions to start a project from stratch.

### Create a project from scratch
In order to create a project from scratch, use the following command:
```
$ cdk init --language python app
```
Install python libraries:
```
$ pip install -r requirements.txt
```

### Set up

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

### Generate CloudFormation templates

You can synthesize the CloudFormation template for this code.

```
$ cdk synth
```

### Deploy Stack

As shown in [this page](https://cdkworkshop.com/30-python/20-create-project/500-deploy.html), the first time you deploy an AWS CDK app into an environment (account/region), you’ll need to install a `bootstrap stack`. This stack includes resources that are needed for the toolkit’s operation. For example, the stack includes an S3 bucket that is used to store templates and assets during the deployment process.

0. Verify you have correctly configured your ~/.aws/credentials and ~/.aws/config files.

  NOTE: In case  you need to assume a role in another account, you must follow the following procedure:
  * 0.1 Install the aws-mfa tool
```
$ pip install aws-mfa
```

  * 0.2 Define a profile (e.g. cdk) and update your ~/.aws/config file by including the profile options
```
[profile default]
...

[profile cdk]
region = eu-west-1
output = json
```

  * 0.3 Update your credentials file, by creating a tag profile by appending 'long-term' to the profile name:
```
[cdk-long-term]
aws_access_key_id = YOURACCESSKEYID
aws_secret_access_key = YOURSECRETACCESSKEY
```

  * 0.4 Run the aws-mfa command to set the credentials with the profile
```
aws-mfa --duration 1800 --device arn:aws:iam::<source_account_id>:mfa/<username> --profile <profile-e.g.-cdk> --assume-role arn:aws:iam::<target_account>:role/<role-to-be-assumed> --role-session-name <a-session-name>
```

1. Bootstrap the environment  
```
$ cdk bootstrap
```

2. Run the deployment
```
$ cdk deploy [--profile <profile-e.g.-cdk>]
```

NOTE: You must execute ```cdk synth```  every time before doing the deployment in order to have the CloudFormation generated scripts updated.

### Other useful commands

 * `cdk ls`: List all stacks in the app
 * `cdk destroy`: Destroyed the stack deployed
 * `cdk diff`: Compare deployed stack with current state
 * `cdk docs`: Open CDK documentation


## Structure

The relevant files for this project as the following:

* `app.py`: The main for the application
* `cdk.json`: A configuration file that defines how to execute the application.
* `README.md`: This README file.
* `requirements.txt`: Dependencies needed for the project.
* `setup.py`: It defines how the package is constructed .
* `cdk.out/*`: When `cdk synth` is executed, CloudFormation templates are placed under this directory. Those files are used for deploying the insfrastrure with `cdk deploy` 
* `serverless/*`: The project itself, where source code is placed.
    * `serverless/params/*`: Configuration file, where we define the infrastructure parameters
    * `serverless/lib/*`: Library files, i.e. custom constructors.
    * `serverless/serverless_stack.py`: Main stack file where we define which resources to build.

