# Ansible Templates - Intermediate Lab

## Scenario

A colleague was the unfortunate victim of a scam email, and their network account was compromised. We have been tasked with deploying a hardened `sudoers` file. We need to create an Ansible template of the `sudoers` file.

We must also create an accompanying playbook named `security.yml` to deploy this template to all servers using Ansible Automation Platform.

## Prerequisites

This lab assumes you have completed the error-handling lab and have:
- The `ansible-working` project already created in Automation Platform
- The `First Inventory` configured with your managed nodes
- Linux credentials configured in Automation Platform
- VS Code with access to your ansible-working repository

## Tasks

Complete the following tasks in order. This is an intermediate-level lab, so you'll need to determine the specific implementation details based on your Ansible knowledge.

### Task 1: Configure Inventory Groups

**Objective**: Set up the required host groups for template variable population.

Using the Ansible Automation Platform interface:
- Configure your existing `First Inventory` to include the necessary groups
- Create a `web` group and assign appropriate hosts
- Create a `database` group and assign appropriate hosts
- Ensure hosts are properly distributed between groups for the template to work correctly

**Hint**: The template will reference `groups['web']` and `groups['database']`, so these group names must be exact.

### Task 2: Create the Jinja2 Template

**Objective**: Build a dynamic sudoers template using Ansible facts and variables.

Using VS Code and your `ansible-working` repository:
- Create a folder named `templates-lab`
- In the folder, create a Jinja2 template file named `hardened.j2`
- The template should include:
  ```
  {% raw %}
  %sysops {{ ansible_default_ipv4.address }} = (ALL) ALL
  Host_Alias WEBSERVERS = {{ groups['web']|join(' ') }}
  Host_Alias DBSERVERS = {{ groups['database']|join(' ') }}
  %httpd WEBSERVERS = /bin/su - webuser
  %dba DBSERVERS = /bin/su - dbuser
  {% endraw %}
  ```
  
  

### Task 3: Create the Deployment Playbook

**Objective**: Build a robust playbook that deploys the template with proper validation.

Create a playbook named `security.yml` that:
- Targets all hosts in the inventory
- Uses appropriate privilege escalation
- Creates any necessary directories
- Deploys the template to the correct location (`/etc/sudoers.d/hardened`)
- Validates the sudoers syntax before deployment
- Provides appropriate feedback on deployment success
- Sets correct file permissions and ownership

**Hint**: Use the `template` module with the `validate` parameter to ensure sudoers syntax is correct.

### Task 4: Version Control Integration

**Objective**: Commit your template and playbook to version control.

- Stage and commit all your changes to Git
- Use an appropriate commit message
- Push changes to your GitHub repository
- Handle any Git configuration issues that arise

### Task 5: Create and Execute Job Template

**Objective**: Deploy your template using Ansible Automation Platform.

- Create a new job template in Automation Platform
- Configure it to use your existing project and inventory
- Set appropriate credentials and privilege escalation
- Execute the job template and monitor the results
- Verify successful deployment across all hosts

### Task 6: Validation and Testing

**Objective**: Confirm the template deployment works correctly and produces host-specific content.

- Use Automation Platform's ad-hoc command feature to verify deployment
- Check that deployed files contain host-specific IP addresses
- Verify that group memberships are correctly reflected in the deployed files
- Test that the sudoers syntax is valid
- Document any differences you observe between hosts

### Task 7: Advanced Verification

**Objective**: Demonstrate understanding of how templates work with facts and variables.

- Use ad-hoc commands to gather facts about your hosts
- Compare the facts with the deployed template content
- Verify that Jinja2 filters are working correctly
- Test the dynamic nature of the template by modifying group membership and re-deploying

## Success Criteria

Your lab is complete when:
- [ ] Template file uses proper Jinja2 syntax with Ansible facts and variables
- [ ] Playbook deploys the template with validation and proper permissions
- [ ] Job template executes successfully through Automation Platform
- [ ] Deployed files contain host-specific IP addresses
- [ ] Group aliases are correctly populated from inventory groups
- [ ] Sudoers syntax validation passes on all hosts
- [ ] File permissions are set correctly (0440)
- [ ] Template demonstrates dynamic behavior based on inventory data

## Troubleshooting Tips

- Ensure group names in your template match exactly with inventory group names
- Pay attention to Jinja2 syntax - missing spaces or brackets will cause errors
- Use the `validate` parameter to catch sudoers syntax errors before deployment
- Check that your inventory groups contain the expected hosts
- Remember that template deployment happens on each target host individually
- Use debug tasks to troubleshoot variable values if needed

## Advanced Challenge (Optional)

If you complete the basic requirements quickly, try these additional challenges:

1. **Conditional Logic**: Add conditional statements to the template that include different rules based on host facts (e.g., OS version or architecture)

2. **Complex Filters**: Use additional Jinja2 filters to manipulate the group data (e.g., sort hosts, filter by certain criteria)

3. **Multiple Templates**: Create a second template for a different configuration file and deploy both using the same playbook

4. **Variable Files**: Move some template variables to external variable files and reference them in your playbook

## Conclusion

Congratulations! You've successfully implemented a complete Ansible templating solution that demonstrates:
- Dynamic content generation using Ansible facts
- Integration of inventory data into templates
- Proper template validation and deployment
- Use of Ansible Automation Platform for enterprise automation
- Version control integration for infrastructure as code

This skill set is essential for managing configuration files at scale while maintaining consistency and allowing for host-specific customization.
