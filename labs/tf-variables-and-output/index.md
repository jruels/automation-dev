# Terraform Variables&#x20;

## Overview

In this lab, you will update the existing `main.tf` file to use variables.

## Set the Instance Name with a Variable

### Create the Lab Directory

1. In **Visual Studio Code**, open the working directory created in the previous lab (`YYYYMMDD/terraform`).
2. Right-click in the **Explorer** pane and select **New Folder**.
3. Name the folder `tf-lab2`.
4. Copy `main.tf` from `tf-lab1` to `tf-lab2`:
   - Right-click on `main.tf` in `tf-lab1` and select **Copy**.
   - Navigate to `tf-lab2`, right-click inside the folder, and select **Paste**.

### Define a Variable for the Instance Name

1. Right-click inside `tf-lab2` and select **New File**.
2. Name the file `variables.tf` and open it.
3. Paste the following variable definition:

```hcl
variable "instance_name" {
  description    = "Name tag for EC2 instance"
  type           = string
  default        = "Lab2-TF-example"
}
```

### Update `main.tf` to Use the Variable

1. Open `main.tf` in `tf-lab2`.
2. Update the `aws_instance` resource block to use the new variable:

```hcl
  tags = {
    Name = var.instance_name
  }
```

3. Rename the resource from `lab1-tf-example` to `lab2-tf-example`:

```hcl
resource "aws_instance" "lab2-tf-example" {
 
}
```

## Apply the Configuration

1. Open **Integrated Terminal** in `tf-lab2`.

2. Run the following command:

   ```sh
   terraform apply
   ```

3. If everything looks correct, type `yes` to confirm and apply the configuration.

4. Apply the configuration again, passing the variable via the command line:

   ```sh
   terraform apply -var 'instance_name=SomeOtherName'
   ```

### Note

Variables passed via the command line are not saved, so they must be set each time unless added to a variable file.

## Query Data with Outputs

### Define Output Values

1. Right-click inside `tf-lab2` and select **New File**.
2. Name the file `outputs.tf` and open it.
3. Paste the following output definitions:

```hcl
output "instance_id" {
  description    = "ID of the EC2 instance"
  value          = aws_instance.lab2-tf-example.id
}

output "instance_private_ip" {
  description   = "Private IP address of EC2 instance"
  value       = aws_instance.lab2-tf-example.private_ip
}
```

### Inspect Output Values

1. Apply the configuration:
   ```sh
   terraform apply
   ```
2. Query the outputs:
   ```sh
   terraform output
   ```
3. Example output:
   ```
   instance_id = "i-0bf954919ed765de1"
   instance_public_ip = "54.186.202.254"
   ```

Terraform outputs are useful for integrating with other infrastructure components or CI/CD pipelines.

## Cleanup

1. Destroy the infrastructure:
   ```sh
   terraform destroy -auto-approve
   ```

## Congratulations!

You have successfully used Terraform variables and outputs.
