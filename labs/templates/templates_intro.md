# Working with Ansible Templates, Variables, and Facts

## The Scenario

A colleague was the unfortunate victim of a scam email, and their network account was compromised. We have been tasked with deploying a hardened `sudoers` file. We need to create an Ansible template of the `sudoers` file.

We must also create an accompanying playbook in `/home/ansible/lab-template/security.yml` to deploy this template to all servers in the default inventory.

## Logging In

Log in to the server as `ec2-user` and sudo to the `ansible` user.
 ```
 sudo su - ansible
 ```

Create and enter a working directory

 ```
 mkdir /home/ansible/lab-template && cd /home/ansible/lab-template
 ```

## Create a Template *sudoers* File

```
vim hardened.j2 
```

Now that we're in Vim, we'll put these contents in the file:

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
localhost
[nodes]
node1 ansible_host=<IP of node1 from spreadsheet> 
node2 ansible_host=<IP of node2 from spreadsheet> 
[web]
node1 ansible_host=<IP of node1 from spreadsheet> 
[database]
node2 ansible_host=<IP of node2 from spreadsheet> 
```

## Set up SSH key

We must configure SSH access to localhost as the `ansible` user. 

```
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
```

 Set permissions on the `authorized_keys` file

```
chmod 600 ~/.ssh/authorized_keys
```



Confirm you can ssh as the `ansible` user to `localhost`

```
ssh localhost
```

Type `yes` when prompted to accept the key. 

You should now be logged into `localhost` over `SSH` as the `ansible` user. 



Exit the SSH connection

```
exit
```



## Create a Playbook

```
vim security.yml 
```

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
