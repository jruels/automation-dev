# Write a Terraform module

## Overview
In this lab, you will create a module to manage AWS S3 buckets to host static websites.

## Module structure

Remember the typical structure for a new module is: 
```
.
├── LICENSE
├── README.md
├── main.tf
├── variables.tf
├── outputs.tf
```
None of these files are required, or have any special meaning to Terraform when it uses your module. You can create a module with a single `.tf` file, or use any other file structure you like.

Each of these files serves a purpose:

- `LICENSE` will contain the license under which your module will be distributed. When you share your module, the `LICENSE` file will let people using it know the terms under which it has been made available. Terraform itself does not use this file.
- `README.md` will contain documentation describing how to use your module, in markdown format. Terraform does not use this file, but services like the Terraform Registry and GitHub will display the contents of this file to people who visit your module's Terraform Registry or GitHub page`
- `main.tf` will contain the main set of configuration for your module. You can also create other configuration files and organize them however makes sense for your project.
- `variables.tf` will contain the variable definitions for your module. When your module is used by others, the variables will be configured as arguments in the `module block`. Since all Terraform values must be defined, any variables that are not given a default value will become required arguments. Variables with default values can also be provided as module arguments, overriding the default value.
- `outputs.tf` will contain the output definitions for your module. Module outputs are made available to the configuration using the module, so they are often used to pass information about the parts of your infrastructure defined by the module to other parts of your configuration.

You also want to make sure and add the following to your ignore list. If you are tracking your module in GitHub use `.gitignore`

- `terraform.tfstate` and `terraform.tfstate.backup`: These files contain your Terraform state, and are how Terraform keeps track of the relationship between your configuration and the infrastructure provisioned by it.
- `.terraform`: This directory contains the modules and plugins used to provision your infrastructure. These files are specific to a specific instance of Terraform when provisioning infrastructure, not the configuration of the infrastructure defined in `.tf` files.
- `*.tfvars`: Since module input variables are set via arguments to the module block in your configuration, you don't need to distribute any `*.tfvars` files with your module, unless you are also using it as a standalone Terraform configuration.

## Create a module 

### Create Terraform configuration

1. In **Visual Studio Code**, open the working directory created in the previous lab (`YYYYMMDD/terraform`).
2. Right-click in the **Explorer** pane and select **New Folder**.
3. Name the folder `tf-lab5`.
4. Right click `tf-lab5` and click **Open in Integrated Terminal**.

Clone the GitHub repository.
```sh
git clone https://github.com/jruels/learn-terraform-modules-create.git
```

Enter the directory.
```sh
cd learn-terraform-modules-create
```

Ensure that Terraform has downloaded all the necessary providers and modules by running `terraform init`.

In this lab, you will create a local submodule within your existing configuration that uses the s3 bucket resource from the AWS provider.

Inside your `tf-lab5/learn-terraform-modules-create` folder, create a sub-folder called `modules`. In the new `modules` folder create a sub-folder named `aws-s3-static-website-bucket`. 



After creating these directories, your configuration's directory structure will look like this:
```
learn-terraform-modules-create
├── LICENSE
├── README.md
├── main.tf
├── modules
│   └── aws-s3-static-website-bucket
├── outputs.tf
└── variables.tf
```


Hosting a static website with S3 is a fairly common use case. While it isn't too difficult to figure out the correct configuration to provision a bucket this way, encapsulating this configuration within a module will provide your users with a quick and easy way create buckets they can use to host static websites that adhere to best practices. Another benefit of using a module is that the module name can describe exactly what buckets created with it are for. In this example, the `aws-s3-static-website-bucket` module creates S3 buckets that host static websites.

You will work with three Terraform configuration files inside the `aws-s3-static-website-bucket` directory: `main.tf`, `variables.tf`, and `outputs.tf`.

Inside the `modules/aws-s3-static-website-bucket` directory, create a `main.tf`  with the following: 

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name

  tags = var.tags
}

resource "aws_s3_bucket_cors_configuration" "s3_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id  

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }  
}

resource "aws_s3_bucket_website_configuration" "s3_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_acl" "s3_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id
  acl = "public-read"
  depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
}

resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
  bucket = aws_s3_bucket.s3_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
  depends_on = [aws_s3_bucket_public_access_block.example]
}

resource "aws_iam_user" "s3_bucket" {
  name = "s3-bucket"
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.s3_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "s3_bucket" {
  bucket = aws_s3_bucket.s3_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource = [
          aws_s3_bucket.s3_bucket.arn,
          "${aws_s3_bucket.s3_bucket.arn}/*",
        ]
      },
    ]
  })
  depends_on = [aws_s3_bucket_public_access_block.example]
}
```

This configuration creates a public S3 bucket hosting a website with an index page and an error page.

You will notice that there is no provider block in this configuration. When Terraform processes a module block, it will inherit the provider from the enclosing configuration. Because of this, there's no need to include `provider` blocks in modules.

Define the following variables in `variables.tf` inside the `modules/aws-s3-static-website-bucket` directory:

- name: `bucket_name`
- description: `Name of S3 bucket. Must be unique`
- type: `string`

- name: `tags`
- description: `Tags to set on bucket.`
- type: `map(string)`
- default: `{}`


When using a module, variables are set by passing arguments to the module in your configuration. You will set values for some of these variables when calling this module from your root module's `main.tf`.

Consider which resource arguments to expose to module end users as input variables when creating a module. For example, you might choose to make the index and error documents available to end users of this module as variables, but refrain from defining a variable to set the ACL , since hosting a website requires your bucket to have the ACL set to "public-read. "

You should also consider which values to add as outputs since outputs are the only way users can get information about resources configured by the module.

Inside the `modules/aws-s3-static-website-bucket` directory, add outputs to your module in the `outputs.tf` file :

## Output variable definitions

- name: `arn`
- description: `ARN of the bucket`
- value: `aws_s3_bucket.s3_bucket.arn`

- name: `name`
- description: `Name (id) of the bucket`
- value: `aws_s3_bucket.s3_bucket.id`

- name: `domain`
- description: `Domain name of the bucket`
- value: `aws_s3_bucket_website_configuration.s3_bucket.website_domain`

Like variables, outputs in modules perform the same function as they do in the root module but are accessed differently. A module's outputs can be accessed as read-only attributes on the module object, which is available within the configuration that calls the module. You can reference these outputs in expressions as `module.<MODULE NAME>.<OUTPUT NAME>`.

Now that you have created your module, return to the `main.tf` in your root module and add a reference to the new module:

```hcl
module "website_s3_bucket" {
  source = "./modules/aws-s3-static-website-bucket"

  bucket_name = "<UNIQUE BUCKET NAME>"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```

AWS S3 Buckets must be globally unique. Because of this, you will need to **replace `<UNIQUE BUCKET NAME>`** with a unique, valid name for an S3 bucket. Using your name and the date is usually a good way to guess a unique bucket name. For example:

```hcl
  bucket_name = "jrs-example-2023-01-15"
```

In this example, the `bucket_name` and `tags` arguments will be passed to the module, and values will be provided for the matching variables found in `modules/aws-s3-static-website-bucket/variables.tf`.

## Define outputs
Earlier, you added several outputs to the `aws-s3-static-website-bucket` module, making those values available to your root module configuration.

Add these values as outputs to your root module by adding the following to `outputs.tf` file in your root module directory (not the one in `modules/aws-s3-static-website-bucket`).

```hcl
# Output definitions

output "website_bucket_arn" {
  description = "ARN of the bucket"
  value       = module.website_s3_bucket.arn
}

output "website_bucket_name" {
  description = "Name (id) of the bucket"
  value       = module.website_s3_bucket.name
}

output "website_bucket_domain" {
  description = "Domain name of the bucket"
  value       = module.website_s3_bucket.domain
}
```

## Install the local module
When you add a new module to a configuration, Terraform must install it before it can be used. Both the `terraform get` and `terraform init` commands will install and update modules. The `terraform init` command will also initialize backends and install plugins.

```sh
terraform get
```

Now that your new module is installed and configured, run `terraform apply` to provision your bucket.


## Bonus
Use the `aws s3` command to copy an `index.html` file to your bucket, and load it in a browser. 


## Cleanup
Now clean everything up by running `terraform destroy -auto-approve`

# Congrats! 
You have now configured and used your own module to create a static website. 
