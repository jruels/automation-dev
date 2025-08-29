# Ansible Error Handling - Intermediate Lab
## Scenario

We have to set up automation to pull down a data file, from a notoriously unreliable third-party system, for integration purposes. Create a playbook that attempts to download https://bit.ly/3dtJtR7 and save it as `transaction_list` to `localhost`. The playbook should gracefully handle the site being down by outputting the message "Site appears to be down. Try again later." to stdout. If the task succeeds, the playbook should write "File downloaded." to stdout. No matter if the playbook errors or not, it should always output "Attempt completed." to stdout.

If the report is collected, the playbook should write and edit the file to replace all occurrences of `#BLANKLINE` with a line break '\n'.

## Prerequisites
Before starting this lab, ensure you have:
- Access to Ansible Automation Platform
- A configured inventory with managed nodes
- VS Code with access to your ansible-working repository
- Linux credentials configured in Automation Platform

## Tasks

Complete the following tasks in order. This is an intermediate-level lab, so you'll need to determine the specific implementation details based on your Ansible knowledge.

### Task 1: Set up Maintenance Infrastructure

**Objective**: Create the necessary projects and job templates to simulate service outages for testing purposes.

- Create a new project in Ansible Automation Platform called `automation-dev` that pulls from the Git repository: `https://github.com/jruels/automation-dev.git`
- Configure this project with Clean, Delete, and Update Revision on Launch options
- Create two job templates using this project:
  - One template to simulate a service being down (use the `break_stuff.yml` playbook with `service_down` job tag)
  - One template to restore the service (use the `break_stuff.yml` playbook with `service_up` job tag)
- Both templates should use privilege escalation and your Linux credentials

### Task 2: Create the Error Handling Playbook

**Objective**: Build a robust playbook that handles download failures gracefully.

Using VS Code and your `ansible-working` repository:

- Create a playbook named `report.yml` that targets all hosts
- Implement the playbook with proper error handling structure using `block`, `rescue`, and `always` sections
- The playbook should:
  - Create a directory `/home/ansible/lab-error-handling` with proper permissions
  - Download the file from `https://bit.ly/3dtJtR7` to `/home/ansible/lab-error-handling/transaction_list`
  - Replace all occurrences of `#BLANKLINE` with newline characters (`\n`) in the downloaded file
  - Output "File downloaded." when successful
  - Output "Site appears to be down. Try again later." when the download fails
  - Always output "Attempt completed." regardless of success or failure

**Hint**: Use the `file`, `get_url`, `replace`, and `debug` modules. Structure your playbook with proper error handling blocks.

### Task 3: Version Control Integration

**Objective**: Commit your work to version control for deployment.

- Save your changes to the `report.yml` playbook
- Stage and commit your changes to Git with an appropriate commit message
- Push the changes to your GitHub repository
- Handle any Git configuration issues that may arise

### Task 4: Create Deployment Project

**Objective**: Set up a project in Automation Platform to run your custom playbook.

- Create a new project called `ansible-working` in Automation Platform
- Configure it to use your personal GitHub repository URL: `https://github.com/[YOUR_USERNAME]/ansible-working.git`
- Configure the project with Clean, Delete, and Update Revision on Launch options

### Task 5: Create and Test the Main Job Template

**Objective**: Create a job template to execute your error handling playbook.

- Create a job template called `error_handling` that:
  - Uses your `ansible-working` project
  - Executes the `report.yml` playbook
  - Uses your configured inventory and Linux credentials
- Run the job template and verify successful execution
- Check the job output to confirm the file was downloaded and processed correctly

### Task 6: Test Error Handling

**Objective**: Verify that your playbook handles failures gracefully.

- Run your service disruption template to simulate the external service being down
- Execute your `error_handling` job template again
- Verify that the playbook outputs the appropriate error message and completes gracefully
- Restore the service using your service restoration template
- Run the `error_handling` job template one more time to confirm it works normally again

### Task 7: Verification and Documentation

**Objective**: Confirm your implementation works correctly.

- Use an ad-hoc command to verify the `/home/ansible/lab-error-handling/transaction_list` file exists and is properly formatted
- Document any issues encountered and how you resolved them
- Confirm that all job templates execute successfully

## Success Criteria

Your lab is complete when:
- The error handling playbook downloads and processes files successfully under normal conditions
- The playbook gracefully handles connection failures with appropriate error messages
- The "Attempt completed." message appears regardless of success or failure
- The `#BLANKLINE` text is properly replaced with newline characters
- All job templates execute without errors
- The transaction list file is created with correct formatting

## Troubleshooting Tips

- If you encounter Git configuration issues, ensure your user name and email are set globally
- Pay attention to file paths - they should be consistent throughout your implementation
- Remember that the `replace` module uses regular expressions
- Test your playbook structure carefully - `block`, `rescue`, and `always` sections must be properly indented

## Congrats!

You've successfully implemented a robust error handling solution in Ansible that can gracefully manage third-party service failures while ensuring consistent reporting and file processing.

