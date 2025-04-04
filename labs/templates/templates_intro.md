# Ansible Templates

## The Scenario

A colleague was the unfortunate victim of a scam email, and their network account was compromised. We have been tasked with deploying a hardened `sudoers` file. We need to create an Ansible template of the `sudoers` file.

We also need to create an accompanying playbook in `/home/ansible/lab-template/security.yml` that will deploy this template to all servers in the default inventory.



## Create a Template *sudoers* File

In the VS Code window connected to Ansible Controller, create a lab directory named ``/home/ansible/lab-template`

In the new directory, create a file named `hardened.j2 ` with the following: 

```
{% raw %}
%sysops {{ ansible_default_ipv4.address }} = (ALL) ALL
Host_Alias WEBSERVERS = {{ groups['web']|join(' ') }}
Host_Alias DBSERVERS = {{ groups['database']|join(' ') }}
%httpd WEBSERVERS = /bin/su - webuser
%dba DBSERVERS = /bin/su - dbuser
{% endraw %}
```



## Create an inventory file

Create an `inventory` file containing: 

```
[nodes]
node1 ansible_host=<IP of node1 from spreadsheet> 
node2 ansible_host=<IP of node2 from spreadsheet> 
[web]
node1 ansible_host=<IP of node1 from spreadsheet> 
[database]
node2 ansible_host=<IP of node2 from spreadsheet> 
```



## Create a Playbook

In the lab directory create a playbook named `security.yml` with the following: 

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



## Run the Playbook

```
ansible-playbook -i inventory security.yml 
```

The output will show that everything deployed fine, but we can check locally to make sure. Run the following command to read the file:

```
sudo cat /etc/sudoers.d/hardened 
```

The custom IP and host aliases are in there.

## Conclusion

Congratulations on completing the lab!
