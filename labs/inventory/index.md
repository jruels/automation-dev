# Working with Ansible Inventories

## Introduction

Your coworker has created a simple script and an Ansible playbook to create an archive of select files, depending on pre-defined Ansible host groups. 

You will create the inventory file to complete the backup strategy.

### Prerequisites

Install the community module collection

```
ansible-galaxy collection install community.general
```



### Configure the `media` Host Group to Contain `media1` and `media2`

In VS Code, create a new lab directory named `lab-inventory`

Inside the new directory, create an `inventory` file

1. Paste in the following:

   ```
   [media] 
   media1 ansible_host=<IP of node1 from /home/ansible/inventory/inventory.yaml>
   media2 ansible_host=<IP of node2 from /home/ansible/inventory/inventory.yaml>
   ```



### Define variables for `media` with their accompanying values

1. Create a `group_vars` directory:

2. In the `group_vars` directory, create a `media` file with the following:

   ```
   media_content: /tmp/var/media/content/
   media_index: /tmp/opt/media/mediaIndex
   ```



### Configure the `webservers` Host Group to contain the hosts `web1` and `web2`

1. In the lab directory (`lab-inventory`), update the `inventory` file.

3. Beneath `media2`, paste in the following:

   ```
   [webservers] 
   web1 ansible_host=<IP of node1 from /home/ansible/inventory/inventory.yaml>
   web2 ansible_host=<IP of node2 from /home/ansible/inventory/inventory.yaml>
   ```



### Define Variables for `webservers` with their accompanying values

1. In the `group_vars` directory, edit the `webservers` file:

4. Paste in the following:

   ```
   httpd_webroot: /var/www/
   httpd_config: /etc/httpd/
   ```



### Define the `script_files` variable for `web1` 

1. In the lab directory (`lab-inventory`), create a `host_vars` directory

2. Inside the `host_vars` directory, create a `web1` file

3. Paste in the following:

   `script_files: /tmp/usr/local/scripts `

Copy the ``scripts`` directory from the clone repository to the lab directory.

```
cp -r /home/ansible/automation-dev/labs/inventory/scripts /home/ansible/lab-inventory/.
```

## Testing

1. Ensure you're in the `lab-inventory` directory and run the following.

   `bash ./scripts/backup.sh `

   If you have correctly configured the inventory, you won't see any errors.



## Conclusion

Congratulations — You've completed this hands-on lab!
