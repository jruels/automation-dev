## Introduction

Working with Ansible roles is a key concept. This should not be a surprise, considering how much functionality roles provide. This exercise covers how to create a role and how to use roles within a playbook. After completing this learning activity, you will better understand how to work with Ansible roles.



In the VS Code session connected to your Ansible Controller, create a directory `roles`.


Inside that directory, create a sub-folder `baseline`



### Create a Role Called `baseline` 

1. Create the structure needed for the role:

   `cd roles/ `

   `mkdir -p baseline/{templates,tasks,files}  `

   `echo "---" > baseline/tasks/main.yml `

### Configure the Role to Deploy the `/etc/motd` Template

1. Copy the file:

   `cp /home/ansible/automation-dev/labs/roles/resources/motd.j2 baseline/templates `

2. Create a file called `deploy_motd.yml`:

   `vi baseline/tasks/deploy_motd.yml `

3. Add the following content:

   ```yaml
   ---
   - template:
       src: motd.j2
       dest: /etc/motd
   ```

   

   Save and exit with **Escape** followed by `:wq`.

4. Open `main.yml`:

   `vi baseline/tasks/main.yml `

5. Add the following lines to the file:

   ```yaml
   - name: configure motd
     import_tasks: deploy_motd.yml
   ```

   Save and exit with **Escape** followed by `:wq`.

   

### Configure the Role to Add an Entry to `/etc/hosts`

1. Create a file called `edit_hosts.yml`:

   `vi baseline/tasks/edit_hosts.yml `

2. Add the following content:

   ```yaml
   ---
   - lineinfile:
   {% raw %}
       line: "{{ ansible_default_ipv4.address }} {{ inventory_hostname_short }}.example.com"
       path: /etc/hosts
   {% endraw %}
   ```

   

   Save and exit with **Escape** followed by `:wq`.

3. Open `main.yml`:

   `vi baseline/tasks/main.yml `

4. Add the following lines to the bottom of the file:

   ```yaml
   - name: edit hosts file
     import_tasks: edit_hosts.yml
   ```

   

   Save and exit with **Escape** followed by `:wq`.

### Configure the Role to Create the `noc` User and Deploy the Provided Public Key for the `noc` User on Target Systems

1. Copy the provided `authorized_keys` file to our `files` directory:

   `cp /home/ansible/automation-dev/labs/roles/resources/authorized_keys baseline/files/ `

2. Create a file called `deploy_noc_user.yml`:

   `vi baseline/tasks/deploy_noc_user.yml `

3. Add the following content:

   ```yaml
   ---
   - user: name=noc
   - file:
        state: directory
        path: /home/noc/.ssh
        mode: 0600
        owner: noc
        group: noc
   - copy:
        src: authorized_keys
        dest: /home/noc/.ssh/authorized_keys
        mode: 0600
        owner: noc
        group: noc
   ```

   

   Save and exit with **Escape** followed by `:wq`.

4. Open `main.yml`:

   `vi baseline/tasks/main.yml `

5. Add the following to the file:

   ```yaml
   - name: set up noc user and key
     import_tasks: deploy_noc_user.yml
   ```
   
   
   

Save and exit with **Escape** followed by `:wq`.

### Edit `web.yml` to Deploy the `baseline` Role

1. Copy `web.yml` to the lab directory:

   `cp /home/ansible/automation-dev/labs/roles/resources/web.yml /home/ansible/roles/ `

2. Open `web.yml`:

   `vi /home/ansible/roles/web.yml `

3. Edit it to match the following:

```yaml
---
- hosts: webservers
  become: yes
  roles:
    - baseline
  tasks:
    - name: install httpd
      yum: name=httpd state=latest
    - name: start and enable httpd
      service: name=httpd state=started enabled=yes
```

   

   Save and exit with **Escape** followed by `:wq`.

### Create inventory

Create an `inventory` file containing the following: 

```
localhost
[webservers]
node1 ansible_host=<IP of node1 from spreadsheet> 
node2 ansible_host=<IP of node2 from spreadsheet> 
```



### Run Your Playbook 

1. Deploy the playbook:

   `ansible-playbook -i inventory web.yml `

### Check Our Work

1. Log in to `node1` :

   `ssh <node1's ip address> `

   We should see a new MOTD, so we know that play worked.

2. See if the `noc` user was set up:

   `id noc `

## Conclusion

All these plays ran, and now we've got a playbook that we can edit when we want to keep things consistent across our webservers. Congratulations!
