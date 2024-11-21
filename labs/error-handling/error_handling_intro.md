# Ansible Error Handling
## Scenario

We have to set up automation to pull down a data file, from a notoriously unreliable third-party system, for integration purposes. Create a playbook that attempts to download https://bit.ly/3dtJtR7 and save it as `transaction_list` to `localhost`. The playbook should gracefully handle the site being down by outputting the message "Site appears to be down. Try again later." to stdout. If the task succeeds, the playbook should write "File downloaded." to stdout. No matter if the playbook errors or not, it should always output "Attempt completed." to stdout.

If the report is collected, the playbook should write and edit the file to replace all occurrences of `#BLANKLINE` with a line break '\n'.

## Create playbook

### Prerequisites

Log in to the Control Node as `ec2-user` and sudo to the `ansible` user.
 ```
 sudo su - ansible
 ```

 Create and enter the working directory

 ```
 mkdir /home/ansible/lab-error-handling && cd /home/ansible/lab-error-handling
 ```



Create a playbook named `report.yml`

First, we'll specify our **host** and **tasks** (**name**, and **debug** message):

```yaml
---
- hosts: localhost
  tasks:
    - name: download transaction_list
      get_url:
        url: https://bit.ly/3dtJtR7
        dest: /home/ansible/lab-error-handling/transaction_list
    - debug: msg="File downloaded"
```



### Add connection failure logic

We need to reconfigure a bit here, adding a **block** keyword and a **rescue**, in case the URL we're reaching out to is down:

```yaml
---
- hosts: localhost
  tasks:
    - name: download transaction_list
      block:
        - get_url:
            url: https://bit.ly/3dtJtR7
            dest: /home/ansible/lab-error-handling/transaction_list
        - debug: msg="File downloaded"
      rescue:
        - debug: msg="Site appears to be down.  Try again later."
```



### Add an always message

An **always** block here will let us know that the playbook at least made an attempt to download the file:

```yaml
---
- hosts: localhost
  tasks:
    - name: download transaction_list
      block:
        - get_url:
            url: https://bit.ly/3dtJtR7
            dest: /home/ansible/lab-error-handling/transaction_list
        - debug: msg="File downloaded"
      rescue:
        - debug: msg="Site appears to be down.  Try again later."
      always:
        - debug: msg="Attempt completed."
```

### Replace '#BLANKLINE' with '\n'

We can use the **replace** module for this task, and we'll sneak it in between the **get_url** and first **debug** tasks.

```yaml
---
- hosts: localhost
  tasks:
    - name: download transaction_list
      block:
        - get_url:
            url: https://bit.ly/3dtJtR7
            dest: /home/ansible/lab-error-handling/transaction_list
        - replace:
            path: /home/ansible/lab-error-handling/transaction_list
            regexp: "#BLANKLINE"
            replace: '\n'
        - debug: msg="File downloaded"
      rescue:
        - debug: msg="Site appears to be down.  Try again later."
      always:
        - debug: msg="Attempt completed."
```

## Run the playbook 

```
ansible-playbook /home/ansible/lab-error-handling/report.yml
```

If all went well, we can read the downloaded text file:

```
cat /home/ansible/lab-error-handling/transaction_list
```



After confirming the playbook successfully downloads and updates the `transaction_list` file, pull the latest changes from the repository, and run the `break_stuff.yml` playbook in the `maint` directory to simulate an unreachable host. 

```
cd ~/automation-dev && git pull
```

Add the `ansible` user to the `sudoers` file. 

Exit to the `ec2-user` account
```
exit
```

As `ec2-user` run `visudo`   

```
sudo visudo
```

Add the following: 
```
ansible    ALL=(ALL)       NOPASSWD: ALL
```

Change back to the `ansible` user. 

```
sudo su - ansible
```

```sh
ansible-playbook ~/automation-dev/labs/error-handling/maint/break_stuff.yml --tags service_down
```

Confirm the host is no longer reachable 
```sh
curl -L -o transaction_list https://bit.ly/3dtJtR7
```

Run the playbook again and confirm it gracefully handles the failure.



Restore the service using `break_stuff.yml`, and confirm the `report.yml` playbook reports the service is back online.

```
ansible-playbook ~/automation-dev/labs/error-handling/maint/break_stuff.yml --tags service_up
```

```
ansible-playbook /home/ansible/lab-error-handling/report.yml
```



## Congrats!

