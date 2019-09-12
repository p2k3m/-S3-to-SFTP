# -S3-to-SFTP
AWS lambda python 3.6 code to transfer file from AWS S3 to SFTP Server
λ S3 to SFTP
============

Deployment
----------

1. `make package`
3. Upload `package.zip` to AWS Lambda (on [console](http://docs.aws.amazon.com/lambda/latest/dg/get-started-create-function.html) or [command line](http://docs.aws.amazon.com/lambda/latest/dg/vpc-ec-upload-deployment-pkg.html))

Configuration in AWS Lambda
---------------------------
 * Select Python 3.6 as the runtime environment.
 * In AWS Lambda, you can define a trigger. Select S3 and then PUT. you can limit the triggers to a particular folder there.
 * Set the handler name to "main.lambda_handler"
 * Make sure you give Lambda permission to read from S3

 Architecture
 ------------


 ![alt text](https://pictures142857.s3.ap-south-1.amazonaws.com/arch.png)



Supported Events
----------------

* S3 PUT

Function Environment Vars (**This is encrypted using KMS Keys**) 


![alt text](https://pictures142857.s3.ap-south-1.amazonaws.com/config.png)

-------------------------

| Name             | Description                                                           | Required                                                                                 |
|------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| SSH_HOST         | SSH server name or ip address                                         | Yes                                                                                      |
| SSH_PORT         | SSH server port                                                       | Not (default: 22)                                                                        |
| SSH_DIR          | Directory where the uploaded files should be placed in the SSH server | No (default: SFTP home folder)                                                           |
| SSH_USERNAME     | SSH username for the connection                                       | Yes                                                                                      |
| SSH_PASSWORD     | SSH server password                                                   | Not (default: `None`)                                                                    |


Caveats
-------

This function does not replicates the S3 directory structure, it just copies every file uploaded to S3 to the `SSH_DIR` in the `SSH_HOST`.
If the file already exists, it will over-write



