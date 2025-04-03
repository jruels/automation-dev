# Working with Ansible Templates, Variables, and Facts

## The Scenario

A colleague was the unfortunate victim of a scam email, and their network account was compromised. We have been tasked with deploying a hardened `sudoers` file. We need to create an Ansible template of the `sudoers` file.

We must also create an accompanying playbook in `/home/ansible/lab-template/security.yml` to deploy this template to all servers in the default inventory.

## Logging In



In VS Code, create a new lab directory named `lab-template`

## Create a Template *sudoers* File

Inside the new directory, create a file named `hardened.js` with the contents below:

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
localhost ansible_connection=local
[nodes]
node1 ansible_host=<IP of node1> 
node2 ansible_host=<IP of node2> 
[web]
node1 ansible_host=<IP of node1> 
[database]
node2 ansible_host=<IP of node2> 
```



## Create a Playbook

In the `lab-template` directory, create a playbook named `security.yml`

The `security.yml` file should look like this:

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
