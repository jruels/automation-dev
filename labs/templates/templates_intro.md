# Ansible Templates - Intro Lab

## Scenario

A colleague was the unfortunate victim of a scam email, and their network account was compromised. We have been tasked with deploying a hardened `sudoers` file. We need to create an Ansible template of the `sudoers` file.

We also need to create an accompanying playbook named `security.yml` that will deploy this template to all servers using Ansible Automation Platform.

## Prerequisites

This lab assumes you have completed the error-handling lab and have:
- The `ansible-working-[your initials]` project already created in Automation Platform
- The `First Inventory-[your initials]` configured with your managed nodes
- Linux credentials configured in Automation Platform
- VS Code with access to your ansible-working repository

## Update Inventory Groups

We need to update the groups the hosts are assigned to:

1. Navigate to **Resources** → **Inventories**
2. Click on **First Inventory-[your initials]**
3. Click the **Groups** tab
4. Click `web` group
6. In the `web` group, click the **Hosts** tab and remove the `Server2-[your initials]`
7. Go back to the inventory Groups tab and click **Add** to create the `database` group:
   * **Name**: `database`
   * **Description**: `Database servers group`
8. Click **Save**
9. In the `database` group, click the **Hosts** tab and click **Add existing host**
10. Select the second node from your inventory and click **Save**

## Create the Template and Playbook

In VS Code, open your `ansible-working` repository.

### Create the Jinja2 Template

Create a directory structure and files:

1. Create a directory named `templates-lab`
2. Inside `templates-lab`, create a file named `hardened.j2` with the following content:

```jinja2
{% raw %}
%sysops {{ ansible_default_ipv4.address }} = (ALL) ALL
Host_Alias WEBSERVERS = {{ groups['web']|join(' ') }}
Host_Alias DBSERVERS = {{ groups['database']|join(' ') }}
%httpd WEBSERVERS = /bin/su - webuser
%dba DBSERVERS = /bin/su - dbuser
{% endraw %}
```

### Create the Playbook

In the `templates-lab` directory, create a playbook named `security.yml` with the following:

```yaml
---
- hosts: all
  become: yes
  tasks:
    - name: Create directory for template deployment
      file:
        path: /home/ansible/lab-templates
        state: directory
        mode: '0755'
    
    - name: Deploy sudo template
      template:
        src: hardened.j2
        dest: /etc/sudoers.d/hardened
        mode: '0440'
        validate: /sbin/visudo -cf %s
    
    - name: Display success message
      debug:
        msg: "Hardened sudoers template deployed successfully"
```

## Commit and Push Changes to GitHub

1. Confirm you've saved your changes
2. In the sidebar, click on the "Source Control" icon (it looks like a branch)
3. In the "Source Control" pane, review the changes you made to the files
4. Under the `ansible-working` repo, enter a commit message: "Add templates lab files"
5. Click the "Commit" button to commit the changes
6. Click "yes", if prompted to stage all files
7. Click on the "…" menu in the "Source Control" pane, and select "Push" to push the changes to GitHub
8. If you are prompted, log in to GitHub to authenticate

## Create Job Template

In Automation Platform, create a new job template:

1. Navigate to **Resources** → **Templates**
2. Click **Add** and select **Add job template**
3. Fill in the following details:
   * **Name**: `deploy_hardened_sudoers-[your initials]`
   * **Description**: `Deploy hardened sudoers template`
   * **Job Type**: `Run`
   * **Inventory**: `First Inventory-[your initials]`
   * **Project**: `ansible-working-[your initials]`
   * **Execution Environment**: `Default execution environment`
   * **Playbook**: `templates-lab/security.yml`
   * **Credentials**: `Linux credentials-[your initials]`
   * **Privilege Escalation**: Check the box
4. Click **Save**

## Run the Job Template

1. Click the **Launch** button on your `deploy_hardened_sudoers-[your initials]` template
2. Monitor the job execution in real-time
3. Review the job output to ensure successful deployment

The output should show:
- Directory creation
- Template deployment with validation
- Success message for each host

## Verify the Deployment

### Using Ad-Hoc Commands

1. Navigate to **Resources** → **Inventories**
2. Select **First Inventory-[your initials]**
3. Click the **Hosts** tab
4. Select all hosts using the checkboxes
5. Click **Run Command**
6. Configure the ad-hoc command:
   * **Module**: `shell`
   * **Arguments**: `sudo cat /etc/sudoers.d/hardened`
   * **Credentials**: `Linux credentials-[your initials]`
   * **Privilege Escalation**: Check the box
7. Click **Launch**

You should see the customized sudoers content with:
- The actual IP addresses of your nodes
- Properly populated host aliases for WEBSERVERS and DBSERVERS groups

### Expected Output

The deployed file should contain something like:
```
%sysops 192.168.1.10 = (ALL) ALL
Host_Alias WEBSERVERS = node1
Host_Alias DBSERVERS = node2
%httpd WEBSERVERS = /bin/su - webuser
%dba DBSERVERS = /bin/su - dbuser
```

*(IP addresses will match your actual node IPs)*

## Understanding the Template

Let's break down what the template accomplished:

- **`{{ ansible_default_ipv4.address }}`**: This Ansible fact gets replaced with each host's primary IP address
- **`{{ groups['web']|join(' ') }}`**: This creates a space-separated list of all hosts in the 'web' group
- **`{{ groups['database']|join(' ') }}`**: This creates a space-separated list of all hosts in the 'database' group
- **Template validation**: The `validate` parameter ensures the sudoers syntax is correct before deployment
- **Jinja2 filters**: The `join(' ')` filter converts the host list into a space-separated string

## Test Template Customization

Let's verify that the template is truly dynamic by checking different hosts:

1. Run another ad-hoc command to see the IP differences:
   * **Module**: `setup`
   * **Arguments**: `filter=ansible_default_ipv4`
2. Compare the IPs shown in the setup module with those in the deployed sudoers file

Each host should have its own IP address in the sudoers file, demonstrating the power of Ansible templates.

## Conclusion

Congratulations! You have successfully:
- Created a Jinja2 template using Ansible facts and group variables
- Built a playbook that deploys templates with syntax validation
- Used Ansible Automation Platform to deploy customized configuration files
- Verified that templates generate host-specific content
- Understood how Jinja2 filters work with Ansible group data

This demonstrates how Ansible templates enable you to maintain consistent configuration patterns while allowing for host-specific customization - a crucial skill for managing diverse infrastructure at scale.
