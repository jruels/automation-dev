# Working with Ansible Inventories

## Introduction

Your coworker has created a simple script and an Ansible playbook to create an archive of select files, depending on pre-defined Ansible host groups. You will create the inventory file to complete the backup strategy.

## Log into the controller manager

Log in to the server as `ec2-user` and sudo to the `ansible` user.
```
sudo su - ansible
```

### Prerequisites

Before we begin, we need to clone the lab directory, and install some community modules. 

Clone the lab directory

```
cd /home/ansible
git clone https://github.com/jruels/automation-dev.git
```

Install the community module collection

```
ansible-galaxy collection install community.general
```


Create and enter a working directory

```
mkdir /home/ansible/lab-inventory && cd /home/ansible/lab-inventory
```

### Configure the `media` Host Group to Contain `media1` and `media2`

1. Create `/home/ansible/lab-inventory/inventory ` with your preferred editor

3. Paste in the following:

   ```
   [media] 
   media1 ansible_host=<IP of node1 from spreadsheet>
   media2 ansible_host=<IP of node2 from spreadsheet>
   ```



### Define variables for `media` with their accompanying values

1. Create a `group_vars` directory:

   `mkdir group_vars `

2. Move into the `group_vars` directory:

   `cd group_vars/ `

3. Create a `media` file with the following:

   ```
   media_content: /tmp/var/media/content/
   media_index: /tmp/opt/media/mediaIndex
   ```



### Configure the `webservers` Host Group to contain the hosts `web1` and `web2`

1. Move into the working directory:

   `cd /home/ansible/lab-inventory`

2. Edit the `inventory` file:

   

3. Beneath `media2`, paste in the following:

   ```
   [webservers] 
   web1 ansible_host=<IP of node1 from spreadsheet>
   web2 ansible_host=<IP of node2 from spreadsheet>
   ```



### Define Variables for `webservers` with their accompanying values

1. Move into the `group_vars` directory:

   `cd group_vars/ `

3. Edit the `webservers` file:

4. Paste in the following:

   ```
   httpd_webroot: /var/www/
   httpd_config: /etc/httpd/
   ```



### Define the `script_files` variable for `web1` 

1. Move into the working directory:

   `cd /home/ansible/lab-inventory `

2. Create a `host_vars` directory:

   `mkdir host_vars `

3. Move into the `host_vars` directory:

   `cd host_vars/ `

4. Create a `web1` file

6. Paste in the following:

   `script_files: /tmp/usr/local/scripts `

Copy the ``scripts`` directory from the clone repository to the working directory.

```
cp -r /home/ansible/automation-dev/labs/inventory/scripts /home/ansible/lab-inventory/.
```

## Testing

1. Return to the working directory:

   `cd /home/ansible/lab-inventory `

2. Run the backup script:

   `bash ./scripts/backup.sh `

   If you have correctly configured the inventory, it should not error.



## Conclusion

Congratulations — You've completed this hands-on lab!
