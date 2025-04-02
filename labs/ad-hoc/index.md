# Ad-Hoc Ansible Commands

## The Scenario

Some consultants will be performing audits on a number of systems in our company's environment. We've got to create the user accounts listed in `/home/ansible/lab-ad-hoc/userlist.txt` and set up the provided public keys for their accounts. The security team has built a jump host for the consultants to access production systems and provided us with the full key-pair so we can set up and test the connection. All hosts in `dbsystems` will need that public key installed so the consultants may use key-pair authentication to access the systems. We must also ensure the `auditd` service is enabled and running on all systems.



### Prerequisites

In VS Code, create a new lab directory named `lab-ad-hoc,` in the terminal run `cd ~/lab-ad-hoc`

Inside the `lab-ad-hoc` folder, create an `inventory` file with the following:

```
[dbsystems]
db1 ansible_host=<IP of node1 from /home/ansible/inventory/inventory.yaml>
db2 ansible_host=<IP of node2 from /home/ansible/inventory/inventory.yaml>
```



## User Accounts File

Copy the user accounts file from the lab directory to `/home/ansible/lab-ad-hoc/userlist.txt`

```
cp /home/ansible/automation-dev/labs/ad-hoc/files/userlist.txt /home/ansible/lab-ad-hoc/userlist.txt
```



## Create the User Accounts 

If we read the `userlist.txt` file in our work directory, we'll see `consultant` and `supervisor`. Those are the two new user accounts we have to create.

Run the following commands to create those accounts.

```
ansible -i inventory dbsystems -b -m user -a "name=consultant" 
ansible -i inventory dbsystems -b -m user -a "name=supervisor" 
```



## Create keys for users

Create keys for the `consultant` and `supervisor` users.

```
mkdir -p keys/{consultant,supervisor}/.ssh
```



Generate SSH key for `consultant` and `supervisor` users. **RUN EACH LINE SEPARATELY**

```
ssh-keygen -f keys/consultant/.ssh/id_rsa
ssh-keygen -f keys/supervisor/.ssh/id_rsa
```

Create the `authorized_keys` files

```
cat keys/consultant/.ssh/id_rsa.pub > keys/consultant/authorized_keys
cat keys/supervisor/.ssh/id_rsa.pub > keys/supervisor/authorized_keys
```



## Place Key Files in the Correct Location, `/home/$USER/.ssh/authorized_keys`, on Hosts in `dbsystems`

```
ansible -i inventory dbsystems -b -m file -a "path=/home/consultant/.ssh state=directory owner=consultant group=consultant mode=0755" 
ansible -i inventory dbsystems -b -m copy -a "src=/home/ansible/lab-ad-hoc/keys/consultant/authorized_keys dest=/home/consultant/.ssh/authorized_keys mode=0600 owner=consultant group=consultant" 
ansible -i inventory dbsystems -b -m file -a "path=/home/supervisor/.ssh state=directory owner=supervisor group=supervisor mode=0755"
ansible -i inventory dbsystems -b -m copy -a "src=/home/ansible/lab-ad-hoc/keys/supervisor/authorized_keys dest=/home/supervisor/.ssh/authorized_keys mode=0600 owner=supervisor group=supervisor" 
```

## Ensure `auditd` Is Enabled and Running on All Hosts

```
ansible -i inventory dbsystems -b -m service -a "name=auditd state=started enabled=yes" 
```

## Conclusion

By watching the output from those commands, we can see that they all ran successfully. Congratulations!
