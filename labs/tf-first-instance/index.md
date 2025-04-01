# Create your first Terraform resource

## Overview

This lab walks through setting up Terraform and creating your first resources.

## Setup

These instructions assume that you are using Visual Studio Code.

### Create a Working Directory

1. Open **Visual Studio Code**.
2. Click on **File** > **Open Folder...** and create a new folder in your Documents folder named with today's date (e.g., 20240329).
3. Inside the opened folder, right-click in the **Explorer** pane and choose **New Folder**.
4. Name the new folder `terraform` and double-click to enter it.

## Create Terraform Configuration

### Create the Lab Directory

1. Right-click inside the **Explorer** pane again and select **New Folder**.
2. Name this folder `tf-lab1` and enter it.

### Create the `main.tf` File

1. Right-click inside `tf-lab1`, select **New File**, and name it `main.tf`.
2. Open `main.tf` and paste the following Terraform configuration:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region  = "us-west-1"
}

resource "aws_instance" "lab1-tf-example" {
  ami           = "ami-06e4ca05d431835e9"
  instance_type = "t2.micro"

  tags = {
    Name = "Lab1-TF-example"
  }
}
```

This configuration is ready to be applied. We'll review each section in detail below.

## Providers

Each Terraform module must declare required providers so that Terraform can install and use them. The `provider` block configures Terraform to use the AWS provider.

### Security Note

**Never hard-code credentials** into `*.tf` files. Instead, use stored AWS credentials configured in your AWS CLI or environment variables.

## Initialize the Directory

1. In **Visual Studio Code**, right-click on the `tf-lab1` folder in the **Explorer** pane.
2. Select **Open in Integrated Terminal** to ensure that all Terraform commands run in the correct directory.
3. Run the following command to initialize Terraform and download the required providers:
   ```sh
   terraform init
   ```
4. You should see Terraform downloading the necessary plugins and initializing the environment.

## Format and Validate Configuration

1. Run the following in the terminal 
   ```hcl
   terraform fmt
   ```

   * This command formats the file to meet HCL standards

   ```hcl
   terraform validate
   ```

   * This command runs syntax checks and confirms all variables are declared.

## Create Infrastructure

1. Open **Command Palette** and type **Terraform: Plan**, then select it.
   - Review the planned changes before applying them.
2. Apply the configuration:
   - In the terminal, type:
     ```sh
     terraform apply
     ```
   - Terraform will prompt for confirmation. Type **yes** when prompted.

Terraform will create an AWS EC2 instance as specified in your configuration.

## Cleanup

To delete the resources created:

1. Destroy the instance:
   - In the terminal, type:
     ```
     terraform destroy
     ```
   - Terraform will prompt for confirmation. Type **yes** when prompted.

## Congratulations!

You've successfully created and destroyed your first Terraform-managed infrastructure.

