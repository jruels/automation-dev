# Ansible Playbooks - the Basics

## The Scenario

Our company has been increasing the deployment of small brochure-style websites for clients. The head of IT has decided that each client should have their own web server for better client isolation and has tasked us with creating concept automation to quickly deploy web nodes with simple static website content.

We must create an Ansible inventory containing a host group named `web`. The web group should contain `node1` and `node2`.

Then we've got to design an Ansible playbook that will execute the following tasks on your configured inventory:

- Install `httpd`
- Start and enable the `httpd` service
- Install a simple website provided on a repository server.

## Get Logged In

Log in to the control server as `ec2-user` and sudo to the `ansible` user.
 ```
 sudo su - ansible
 ```

### Prerequisites

Create and enter a working directory

 ```
 mkdir /home/ansible/lab-playbook-fun && cd /home/ansible/lab-playbook-fun
 ```

## Create an inventory 

Create an inventory that contains a Host Group named `web` containing node1 and node2

```
echo "[web]" >> inventory 
echo "node1 ansible_host=<IP of node1 from spreadsheet>" >> inventory 
echo "node2 ansible_host=<IP of node2 from spreadsheet>" >> inventory 
```



## Create a Playbook 

Create`/home/ansible/lab-playbook-fun/web.yml` file with these contents:

```yaml
---
- hosts: web
  become: yes
  tasks:
    - name: install httpd
      yum: 
        name: httpd 
        state: latest
    - name: start and enable httpd
      service: 
        name: httpd 
        state: started 
        enabled: yes
    - name: retrieve website from repo
      get_url: 
        url: https://github.com/jruels/ansible-best-practices/raw/main/labs/playbook-fun/files/website.zip 
        dest: /tmp/website.zip
    - name: install website
      unarchive: 
        remote_src: yes 
        src: /tmp/website.zip 
        dest: /var/www/html/
```



## Execute the playbook

```
ansible-playbook -i inventory web.yml 
```



This playbook will fail with the following error: 

```
Make sure the required command to extract the file is installed. Unable to find required 'unzip' or 'zipinfo' binary in the path.
```



## Update the playbook

The playbook must be updated to install the `unzip` package.

Change the `yum` section to install `httpd` and `unzip`

```yaml
tasks:
  - name: install httpd and unzip
    yum: 
      name:
        - unzip
        - httpd
      state: latest
```

Rerun the playbook and confirm it is succesful.



## Conclusion

This new setup is everything we needed. The Ansible playbook installs `httpd` and `unzip`, starts and enables it, and creates a simple website, all on its own web node. That's what we needed. Congratulations!
