# Terraform Refactor codebase

## Overview 
In this lab, you will refactor a monolithic Terraform configuration into a modular design. 

You will provision two instances of a web application hosted in an S3 bucket that represent production and development environments. The configuration you use to deploy the application will start as a monolith. You will modify it to step through the common phases of evolution for a Terraform project, until each environment has its own independent configuration and state.

## Start with a monolith configuration
Create a working directory
```sh
mkdir tf-refactor
cd $_
```
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
To deploy the `dev` environment change to the `dev` directory, initialize Terraform, and apply the configuration.

You now have only one output from this deployment. Check your website endpoint in a browser.

Repeat these steps for your production environment.


After completing this lab you should have a `dev` and `prod` environment successfully deployed. 

Now your development and production environments are in separate directories, each with their own configuration files and state.


### Cleanup
```sh
terraform destroy
```

## Terraform workspaces
Workspace-separated environments use the same Terraform code but have different state files, which is useful if you want your environments to stay as similar to each other as possible, for example if you are providing development infrastructure to a team that wants to simulate running in production.

However, you must manage your workspaces in the CLI and be aware of the workspace you are working in to avoid accidentally performing operations on the wrong environment.

### Update your Terraform directory
Remove your environment directories with `rm -rf dev/ prod/`. Then, switch branches by running `git checkout file-separation`.

All Terraform configurations start out in the `default` workspace. Type `terraform workspace list` to have Terraform print out the list of your workspaces with the currently selected one denoted by a `*`.

You should see something like: 
```sh
$ terraform workspace list
   * default
```

Before you create a new workspace, you need to update your configuration files so that both environments can use the same one. In your root directory, remove the `prod.tf` file.

```sh
rm prod.tf`
```

Update your variable input file to remove references to the individual environments.

Remove the environment references in `variables.tf`
```hcl
variable "region" {
  description = "This is the cloud hosting region where your webapp will be deployed."
}

- variable "dev_prefix" {
+ variable "prefix" {
  description = "This is the environment where your webapp is deployed. qa, prod, or dev"
}

- variable "prod_prefix" {
-   description = "This is the environment where your webapp is deployed. qa, prod, or dev"
- }
```

Rename `dev.tf` to `main.tf`
```sh
mv dev.tf main.tf`
```

Open this file in your text editor and replace the "dev" resource IDs and variables with the function of the resource itself. You are creating a generic configuration file that can apply to multiple environments.

```hcl
-resource "aws_s3_bucket" "dev" {
+resource "aws_s3_bucket" "bucket" {
-  bucket = "${var.dev_prefix}-${random_pet.petname.id}"
+  bucket = "${var.prefix}-${random_pet.petname.id}"

   force_destroy = true
 }

-resource "aws_s3_bucket_website_configuration" "dev" {
+resource "aws_s3_bucket_website_configuration" "bucket" {
-  bucket = aws_s3_bucket.dev.id
+  bucket = aws_s3_bucket.bucket.id

   index_document {
     suffix = "index.html"
   }

   error_document {
     key = "error.html"
   }
 }

-resource "aws_s3_bucket_acl" "dev" {
+resource "aws_s3_bucket_acl" "bucket" {
-  bucket = aws_s3_bucket.dev.id
+  bucket = aws_s3_bucket.bucket.id

  acl = "public-read"
}

- resource "aws_s3_bucket_policy" "dev" {
+ resource "aws_s3_bucket_policy" "bucket" {
-   bucket = aws_s3_bucket.dev.id
+   bucket = aws_s3_bucket.bucket.id

   policy = <<EOF
 {
     "Version": "2012-10-17",
     "Statement": [
         {
             "Sid": "PublicReadGetObject",
             "Effect": "Allow",
             "Principal": "*",
             "Action": [
                 "s3:GetObject"
             ],
             "Resource": [
-                "arn:aws:s3:::${aws_s3_bucket.dev.id}/*"
+                "arn:aws:s3:::${aws_s3_bucket.bucket.id}/*"
             ]
         }
     ]
 }
 EOF
 }

-resource "aws_s3_object" "dev" {
+resource "aws_s3_object" "webapp" {
   acl          = "public-read"
   key          = "index.html"
-  bucket       = aws_s3_bucket.dev.id
+  bucket       = aws_s3_bucket.bucket.id
   content      = file("${path.module}/assets/index.html")
   content_type = "text/html"
 }
```

Using workspaces organizes the resources in your state file by environments, so you only need one output value definition. Open your `outputs.tf` file in your text editor and remove the `dev` environment reference in the output name. Change `dev` in the value to `bucket`.


Finally, replace `terraform.tfvars` with a `prod.tfvars` file and a `dev.tfvars` file to define your variables for each environment.

For your `dev` workspace, copy the `terraform.tfvars` file to a new `dev.tfvars` file, and change `prefix` to `dev`


Create a new `.tfvars` file for your production environment variables by renaming the `terraform.tfvars` file to `prod.tfvars`, and updating `prefix` to `prod`.

Now that you have a single `main.tf` file, initialize your directory to ensure your Terraform configuration is valid.



### Create a `dev` workspace
Create a new workspace in the Terraform CLI with the `workspace` command.

```sh
terraform workspace new dev
```

Terraform's output will confirm you created and switched to the workspace.
```
Created and switched to workspace "dev"!

You're now on a new, empty workspace. Workspaces isolate their state,
so if you run "terraform plan" Terraform will not see any existing state
for this configuration.
```

Any previous state files from your `default` workspace are hidden from your `dev` workspace, but your directory and file structure do not change.

Initialize the new workspace `terraform init`.

Apply the configuration for your development environment in the new workspace, specifying the `dev.tfvars` file with the `-var-file` flag.

Terraform will create three resources and prompt you to confirm that you want to perform these actions in the workspace "dev".

Enter `yes` and check your website endpoint in a browser.

### Create a prod workspace.

```sh
terraform workspace new prod
```

Terraform's output will confirm you created the workspace and are operating within that workspace.

Any previous state files from your `dev` workspace are hidden from your `prod` workspace, but your directory and file structure do not change.


You have a specific `prod.tfvars` file for your new workspace. Run `terraform apply` with the `-var-file` flag and reference the file. Enter `yes` when you are prompted to accept the changes and check your website endpoint in a browser.


Your output now contains only resources labeled "production" and your single website endpoint is prefixed with `prod`.


### State storage in workspaces    
When you use the default workspace with the local backend, your `terraform.tfstate` file is stored in the root directory of your Terraform project. When you add additional workspaces your state location changes; Terraform internals manage and store state files in the directory `terraform.tfstate.d`.

Your directory will look similar to the one below.

```
.
├── README.md
├── assets
│   └── index.html
├── dev.tfvars
├── main.tf
├── outputs.tf
├── prod.tfvars
├── terraform.tfstate.d
│   ├── dev
│   │   └── terraform.tfstate
│   ├── prod
│   │   └── terraform.tfstate
├── terraform.tfvars
└── variables.tf
```


### Destroy your workspace deployments

To destroy your infrastructure in a multiple workspace deployment, you must select the intended workspace and run `terraform destroy -var-file=` with the `.tfvars` file that corresponds to your workspace.

Destroy the infrastructure in your `prod` workspace, specifying the `prod.tfvars` file with the `-var-file` flag.

When you are sure you are running your destroy command in the correct workspace, enter `yes` to confirm the destroy plan.

Next, to destroy your development infrastructure, switch to your `dev` workspace using the select subcommand.

```sh
terraform workspace select dev
```

Run `terraform destroy` specifying `dev.tfvars` with the `-var-file` flag.

```sh
terraform destroy -var-file=dev.tfvars
```

## Congrats!

