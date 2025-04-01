# Terraform Refactor codebase

## Overview 
In this lab, you will refactor a monolithic Terraform configuration into a modular design. 

You will provision two instances of a web application hosted in an S3 bucket that represent production and development environments. The configuration you use to deploy the application will start as a monolith. You will modify it to step through the common phases of evolution for a Terraform project, until each environment has its own independent configuration and state.

## Start with a monolith configuration
### Create the Lab Directory

1. In **Visual Studio Code**, open the working directory created in the previous lab (`YYYYMMDD/terraform`).
2. Right-click in the **Explorer** pane and select **New Folder**.
3. Name the folder `tf-refactor`.
4. Open `tf-refactor` in the **Integrated Terminal**.

Clone the GitHub repository.
```sh
git clone https://github.com/jruels/learn-terraform-code-organization
```

Enter the directory.
```sh
cd learn-terraform-code-organization
```

Your root directory contains four files and an "assets" folder. The root directory files compose the configuration as well as the inputs and outputs of your deployment.

`main.tf` - configures the resources that make up your infrastructure.

`variables.tf` - declares input variables for your `dev` and `prod` environment prefixes, and the AWS region to deploy to.

`terraform.tfvars.example` - defines your region and environment prefixes.

`outputs.tf` - specifies the website endpoints for your dev and prod buckets.

`assets` - houses your webapp HTML file.

Review the `main.tf` file. The file consists of a few different resources:

- The `random_pet` resource creates a string to be used as part of the unique name of your S3 bucket.
- Two `aws_s3_bucket` resources designated `prod` and `dev`, which each create an S3 bucket. Notice that the `bucket` argument defines the S3 bucket name by interpolating the environment prefix and the `random_pet` resource name.
- Two `aws_s3_bucket_acl` resources designated `prod` and `dev`, which set a `public-read` ACL for your buckets.
- Two `aws_s3_bucket_website_configuration` resources designated `prod` and `dev`, which configure your buckets to host websites.
- Two `aws_s3_bucket_policy` resources designated `prod` and `dev`, which allow anyone to read the objects in the corresponding bucket.
- Two `aws_s3_object` resources designated `prod` and `dev`, which load the file in the local `assets` directory using the [built in `file()`function](https://developer.hashicorp.com/terraform/language/functions/file) and upload it to your S3 buckets.

Terraform requires unique identifiers - in this case `prod` or `dev` for each `s3` resource - to create separate resources of the same type.

Open the `terraform.tfvars.example` file in your repository and edit it with your own variable definitions. Confirm the region is `us-west-1`

```hcl
region = "us-west-1"
prod_prefix = "prod"
dev_prefix = "dev"
```

Save your changes and rename the file to `terraform.tfvars`. Terraform automatically loads variable values from any files that end in `.tfvars`.

```sh
mv terraform.tfvars.example terraform.tfvars
```
In your terminal, initialize your Terraform project, and apply the configuration.

Navigate to the web address from the Terraform output to display the deployment in a browser. Your directory now contains a state file, `terraform.tfstate`.

## Separate the configuration

Defining multiple environments in the same `main.tf` file may become hard to manage as you add more resources. HCL is meant to be human-readable and supports using multiple configuration files to help organize your infrastructure.

You will organize your current configuration by separating the configurations into two separate files — one root module for each environment. To split the configuration, copy `main.tf` and name it `dev.tf`, then rename `main.tf` to `prod.tf`

Now you have two identical files. Remove any references to the production environment in `dev.tf` by deleting the resource blocks with the `prod` ID. Repeat the process for `prod.tf` by removing any resource blocks with the `dev` ID.

Your directory structure will look similar to: 
```
.
├── README.md
├── assets
│   └── index.html
├── dev.tf
├── outputs.tf
├── prod.tf
├── terraform.tfstate
├── terraform.tfvars
└── variables.tf
```

Although your resources are organized in environment-specific files, your `variables.tf` and `terraform.tfvars` files contain the variable declarations and definitions for both environments.

Terraform loads all configuration files within a directory and appends them together, so any resources or providers with the same name in the same directory will cause a validation error. If you were to run a `terraform` command now, your `random_pet` resource and `provider` block would cause errors since they are duplicated across the two files.

Edit the `prod.tf` file by commenting out the `terraform` block, the `provider` block, and the `random_pet` resource. You can comment out the configuration by adding a `/*` at the beginning of the commented out block and a `*/` at the end, as shown below.

```hcl
/*
 terraform {
   required_providers {
     aws = {
       source = "hashicorp/aws"
       version = "~> 4.0.0"
     }
     random = {
       source  = "hashicorp/random"
       version = "~> 3.1.0"
     }
   }
 }

 provider "aws" {
   region = var.region
 }

 resource "random_pet" "petname" {
   length    = 3
   separator = "-"
 }
*/
```

With your `prod.tf` shared resources commented out, your production environment will still inherit the value of the `random_pet` resource in your `dev.tf` file.

## Simulate a hidden dependency

You may want your development and production environments to share bucket names, but the current configuration is particularly dangerous because of the hidden resource dependency built into it. Imagine that you want to test a random pet name with four words in development. In `dev.tf`, update your `random_pet` resource's length attribute to `4`.

You might think you are only updating the development environment because you only changed `dev.tf`, but remember, this value is referenced by both `prod` and `dev` resources.

Apply the changes. 

Note that the message stating your resources have changed. In this scenario, you encountered a hidden resource dependency because both bucket names rely on the same resource.

Carefully review Terraform execution plans before applying them. If an operator does not carefully review the plan output or if CI/CD pipelines automatically apply changes, you may accidentally apply breaking changes to your resources.

Destroy your resources before continuing the lab.

```sh
terraform destroy
```

## Separate states

The previous operation destroyed both the development and production environment resources. When working with monolithic configuration, you can use the `terraform apply` command with the `-target` flag to scope the resources to operate on, but that approach can be risky and is not a sustainable way to manage distinct environments. For safer operations, you need to separate your development and production state.

State separation signals more mature usage of Terraform; with additional maturity comes additional complexity. There are two primary methods to separate state between environments: directories and workspaces.

To separate environments with potential configuration differences, use a directory structure. Use workspaces for environments that do not greatly deviate from one another, to avoid duplicating your configurations. Try both methods below to understand which will serve your infrastructure best.

## Directories 
By creating separate directories for each environment, you can shrink the blast radius of your Terraform operations and ensure you will only modify intended infrastructure. Terraform stores your state files on disk in their corresponding configuration directories. Terraform operates only on the state and configuration in the working directory by default.

Directory-separated environments rely on duplicate Terraform code. This may be useful if you want to test changes in a development environment before promoting them to production. However, the directory structure runs the risk of creating drift between the environments over time. If you want to reconfigure a project with a single state file into directory-separated states, you must perform advanced state operations to move the resources.


### Create `prod` and `dev` directories
1. Create directories named `prod` and `dev`.

```sh
mkdir prod && mkdir dev
```

2. Move the `dev.tf` file to the `dev` directory, and rename it to `main.tf`.

3. Copy the `variables.tf`, `terraform.tfvars`, and `outputs.tf` files to the `dev` directory.

Your environment directories are now one step removed from the `assets` folder where your webapp lives. Open the `dev/main.tf` file in your text editor and edit the file to reflect this change by editing the file path in the `content` argument of the `aws_s3_bucket_object` resource with a `/..` before the assets subdirectory.

```hcl
resource "aws_s3_bucket_object" "dev" {
  acl          = "public-read"
  key          = "index.html"
  bucket       = aws_s3_bucket.dev.id
-  content      = file("${path.module}/assets/index.html")
+  content      = file("${path.module}/../assets/index.html")
  content_type = "text/html"
}
```

You will need to remove the references to the `prod` environment from your `dev` configuration files.

First, open `dev/outputs.tf` in your text editor and remove the reference to the `prod` environment, then remove 

Remove all references to `prod` in `dev/outputs.tf`, `dev/variables.tf`, and `dev/terraform.tfvars`.

### Update `prod` configuration

1. Rename `prod.tf` to `main.tf` and move it to your `prod` directory.`

2. Move `variables.tf`, `terraform.tfvars`, and `outputs.tf` to the `prod` directory.

First, open `prod/main.tf` and edit it to reflect new directory structure by adding `/..` to the file path in the content argument of the `aws_s3_bucket_object`, before the `assets` subdirectory.

Next, remove the references to the `dev` environment from `prod/variables.tf`, `prod/outputs.tf`, and `prod/terraform.tfvars`.

Finally, uncomment the `terraform` block, the `provider` block, and the `random_pet` resource in `prod/main.tf`.

After reorganizing your environments into directories, your file structure should look like the one below.

```
.
├── assets
│   ├── index.html
├── prod
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfstate
│   └── terraform.tfvars
└── dev
    ├── main.tf
    ├── variables.tf
    ├── terraform.tfstate
    └── terraform.tfvars
```


### Deploy environments 
To deploy the `dev` environment, change to the `dev` directory, initialize Terraform, and apply the configuration.

You now have only one output from this deployment. Check your website endpoint in a browser.

Repeat these steps for your production environment.


After completing this lab, you should have a `dev` and `prod` environment successfully deployed. 

Your development and production environments are in separate directories, each with its configuration files and state.


### Cleanup
```sh
terraform destroy
```

## Congrats!

