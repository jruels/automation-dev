## Introduction

Working with Ansible roles is a key concept. This should not be a surprise, considering how much functionality roles provide. This exercise covers how to create a role and how to use roles within a playbook. After completing this learning activity, you will better understand how to work with Ansible roles.

Log in to the control node as `ec2-user` and sudo to the `ansible` user.
 ```
 sudo su - ansible
 ```

### Prerequisites

Before we begin, we need to pull the latest changes from our lab repo.

cd into the lab repo directory and pull updates.

```
cd ~/ansible-best-practices && git pull
```



 Create and enter a working directory

 ```
 mkdir /home/ansible/lab-roles && cd /home/ansible/lab-roles
 ```



Create a `roles` directory for our `baseline` role 

```
mkdir roles
```



### Create a Role Called `baseline` 

1. Create the structure needed for the role:

   `cd roles/ `

   `mkdir -p baseline/{templates,tasks,files}  `

   `echo "---" > baseline/tasks/main.yml `

### Configure the Role to Deploy the `/etc/motd` Template

1. Copy the file:

   `cp /home/ansible/ansible-best-practices/labs/roles/resources/motd.j2 baseline/templates `

2. Create a file called `deploy_motd.yml`:

   `vim baseline/tasks/deploy_motd.yml `

3. Add the following content:

   ```yaml
   ---
   - template:
       src: motd.j2
       dest: /etc/motd
   ```

   

   Save and exit with **Escape** followed by `:wq`.

4. Open `main.yml`:

   `vim baseline/tasks/main.yml `

5. Add the following lines to the file:

   ```yaml
   - name: configure motd
     import_tasks: deploy_motd.yml
   ```

   Save and exit with **Escape** followed by `:wq`.

### Configure the Role to Install the Latest Nagios Client

1. We need to install the `nrpe.x86_64` package.

2. Create a file which will install the package named `deploy_nagios.yml`:

   `vim baseline/tasks/deploy_nagios.yml `

3. Add the following content:

   ```yaml
   ---
   - name: Install prerequisite EPEL repository
     yum:
       name:
         - epel-release
       state: latest
   
   - name: Install Nagios client (nrpe)
     yum:
       name:
         - nrpe
       state: latest
   ```

   

   Save and exit with **Escape** followed by `:wq`.

4. Open `main.yml`:

   `vim baseline/tasks/main.yml `

5. Add the following lines to the bottom of the file:

   ```yaml
   - name: deploy nagios client
     import_tasks: deploy_nagios.yml
   ```

   Save and exit with **Escape** followed by `:wq`.

   

### Configure the Role to Add an Entry to `/etc/hosts` for the Nagios Server

1. Create a file called `edit_hosts.yml`:

   `vim baseline/tasks/edit_hosts.yml `

2. Add the following content, substituting `<IP_ADDRESS>` with the node1 server IP from the spreadsheet:

   ```yaml
   ---
   - lineinfile:
       line: "<IP_ADDRESS of node1 from spreadsheet> nagios.example.com"
       path: /etc/hosts
   ```

   

   Save and exit with **Escape** followed by `:wq`.

3. Open `main.yml`:

   `vim baseline/tasks/main.yml `

4. Add the following lines to the bottom of the file:

   ```yaml
   - name: edit hosts file
     import_tasks: edit_hosts.yml
   ```

   

   Save and exit with **Escape** followed by `:wq`.

### Configure the Role to Create the `noc` User and Deploy the Provided Public Key for the `noc` User on Target Systems

1. Copy the provided `authorized_keys` file to our `files` directory:

   `cp /home/ansible/ansible-best-practices/labs/roles/resources/authorized_keys baseline/files/ `

2. Create a file called `deploy_noc_user.yml`:

   `vim baseline/tasks/deploy_noc_user.yml `

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

   `vim baseline/tasks/main.yml `

5. Add the following to the file:

   ```yaml
   - name: set up noc user and key
     import_tasks: deploy_noc_user.yml
   ```
   

   
Save and exit with **Escape** followed by `:wq`.

### Edit `web.yml` to Deploy the `baseline` Role

1. Copy `web.yml` to the lab directory:

   `cp /home/ansible/ansible-best-practices/labs/roles/resources/web.yml /home/ansible/lab-roles/ `

2. Open `web.yml`:

   `vim /home/ansible/lab-roles/web.yml `

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

3. Check to see if the `nrpe` package was installed:

   `sudo yum list nrpe `

## Conclusion

All these plays ran, and now we've got a playbook that we can edit when we want to keep things consistent across our webservers. Congratulations!
