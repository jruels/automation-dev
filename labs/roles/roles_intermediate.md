# Ansible roles
Working with Ansible roles is a key concept. This should not be a surprise, considering how much functionality roles provide. This exercise covers how to create a role and how to use roles within a playbook. After completing this learning activity, you will better understand how to work with Ansible roles.



**NOTE:** All resource files can be found in the lab repo under `labs/roles/resources`

Task list: 

* Create a role named `baseline` 
* Configure the role to deploy `motd.j2` to /etc/motd on all nodes.
* Configure the role to install the latest Nagios client
  * The EPEL repository is required 
  * The Nagios client package is named `nrpe`

* Configure the role to add an entry to `/etc/hosts` on the Nagios server with: 
* nagios.example.com resolving to the `node1` IP address
* Configure the role to create the `noc` user and deploy the provided public key on all nodes.
* Edit `web.yml` to deploy the new `baseline` role
* Create an inventory file that includes:
  * a `webservers` group with both nodes.




## Congrats!

