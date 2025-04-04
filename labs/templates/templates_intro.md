# Working with Ansible Templates, Variables, and Facts

## The Scenario

A colleague was the unfortunate victim of a scam email, and their network account was compromised. We have been tasked with deploying a hardened `sudoers` file. We need to create an Ansible template of the `sudoers` file.

We must also create an accompanying playbook named `security.yml` to deploy this template to all servers in the default inventory.



## Create a Template *sudoers* file

In VS Code, open your `ansible-working` repository.

Create a file named `hardened.j2` with the contents below:

```
{% raw %}
%sysops {{ ansible_default_ipv4.address }} = (ALL) ALL
Host_Alias WEBSERVERS = {{ groups['web']|join(' ') }}
Host_Alias DBSERVERS = {{ groups['database']|join(' ') }}
%httpd WEBSERVERS = /bin/su - webuser
%dba DBSERVERS = /bin/su - dbuser
{% endraw %}
```



## Create a Playbook

In VS Code, open your `ansible-working` repository.

Create a file named `security.yml` with the contents below:

```
---
- hosts: all
  become: yes
  tasks:
  - name: deploy sudo template
    template:
      src: hardened.j2
      dest: /etc/sudoers.d/hardened
      validate: /sbin/visudo -cf %s
```



## Commit and Push Changes to GitHub

1. In the sidebar, click on the “Source Control” icon (it looks like a branch).
2. Confirm you've saved your changes.
3. In the “Source Control” pane, review the changes you made to the file.
4. Under the `ansible-working` repo, enter a commit message describing your changes.
5. Click the “Commit” button to commit the changes.
6. Click “yes” if prompted to stage all files. 
7. Click on the “…” menu in the “Source Control” pane, and select “Push” to push the changes to GitHub.
8. If you are prompted, log into GitHub to authenticate.
9. Click on the “…” menu in the “Source Control” pane, and select “Push” to push the changes to GitHub.



## Create an inventory

In AAP, create a new inventory containing: 

Provide the following:

* **Name**:  sudoers
* **Description**: Sudoers inventory
* **Organization**: Default

Click **Save**

Add nodes 1 and 2 to the inventory. 

Remember to configure the IP address for each host. 

Under **Variables** confirm **YAML** is highlighted and then paste the following:

```yaml
ansible_host: <IP of node (1 or 2) from spreadsheet> 
```



#### Add hosts to required groups

The hosts must be members of groups as defined below. 

* `node1` and `node2` must be in group `nodes`
* `node1` must be in group `web`
* `node2` must be in group `database`



## Run the Playbook

In Automation Platform, create a new template with the following: 

* Name: **sudoers**
* Inventory: **sudoers**
* Project: **ansible-working**
* Execution Environment: **Default execution environment**
* Playbook: **security.yml**
* Credentials: **Linux credentials**
* Privilege Escalation: **Check the box**



Run the `sudoers` job.

You can confirm it ran successfully by reviewing the job output. 





### Bonus challenge

Use `ad-hoc` to confirm the content of `/etc/sudoers.d/hardened` is correct. 



## Conclusion

Congratulations on completing the lab!
