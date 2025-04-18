# Ansible Error Handling
## Scenario

We have to set up automation to pull down a data file, from a notoriously unreliable third-party system, for integration purposes. Create a playbook that attempts to download https://bit.ly/3dtJtR7 and save it as `transaction_list` to `localhost`. The playbook should gracefully handle the site being down by outputting the message "Site appears to be down. Try again later." to stdout. If the task succeeds, the playbook should write "File downloaded." to stdout. No matter if the playbook errors or not, it should always output "Attempt completed." to stdout.

If the report is collected, the playbook should write and edit the file to replace all occurrences of `#BLANKLINE` with a line break '\n'.

## Set up maintenance script

### Prerequisites

### Create Projects

In Ansible Automation Platform, create a new project with the following: 

* Name: **automation-dev**
* Source Control Type: **Git**
* Source Control URL: **https://github.com/jruels/automation-dev.git**
* Options: 
  * **Clean**
  * **Delete**
  * **Update Revision on Launch**



Now, create a project with your `ansible-working` repository

* Name: **ansible-working**
* Source Control Type: **Git**
* Source Control URL: https://github.com/[YOUR_USERNAME]/ansible-working.git
* Options: 
  * **Clean**
  * **Delete**
  * **Update Revision on Launch**

### Create templates

Create a template with the following to simulate a down service: 

* Name: **service_down**
* Inventory: **First Inventory**
* Project: **automation-dev**
* Execution Environment: **Default execution environment**
* Playbook: **labs/error-handling/maint/break_stuff.yml**
* Credentials: **Linux credentials**
* Job Tags: **service_down**
* Privilege Escalation: **Check the box**



Create a template with the following to restore the service: 

* Name: **service_up**
* Inventory: **First Inventory**
* Project: **automation-dev**
* Execution Environment: **Default execution environment**
* Playbook: **labs/error-handling/maint/break_stuff.yml**
* Credentials: **Linux credentials**
* Job Tags: **service_up**
* Privilege Escalation: **Check the box**



## Create the playbook

In VS Code, open your `ansible-working` repository.

Create a playbook named `report.yml` with the following:

First, we'll specify our **host** and **tasks** (**name**, and **debug** message):

```yaml
---
- hosts: all
  tasks:
    - name: download transaction_list
      block:
        - file:
            path: /home/ansible/lab-error-handling
            state: directory
            mode: '0755'
        - get_url:
            url: https://bit.ly/3dtJtR7
            dest: /home/ansible/lab-error-handling/transaction_list
        - debug: msg="File downloaded"
```



### Add connection failure logic

We need to reconfigure a bit here, adding a **block** keyword and a **rescue**, in case the URL we're reaching out to is down:

```yaml
---
- hosts: all
  tasks:
    - name: download transaction_list
      block:
        - file:
            path: /home/ansible/lab-error-handling
            state: directory
            mode: '0755'
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
- hosts: all
  tasks:
    - name: download transaction_list
      block:
        - file:
            path: /home/ansible/lab-error-handling
            state: directory
            mode: '0755'
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
- hosts: all
  tasks:
    - name: download transaction_list
      block:
        - file:
            path: /home/ansible/lab-error-handling
            state: directory
            mode: '0755'
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



## Commit and Push Changes to GitHub

1. In the sidebar, click on the “Source Control” icon (it looks like a branch).
2. Confirm you've saved your changes.
3. In the “Source Control” pane, review the changes you made to the file.
4. Under the `ansible-working` repo, enter a commit message describing your changes.
5. Click the “Commit” button to commit the changes.
6. Click “yes”, if prompted to stage all files. If you get an error about “user.email” and “user.name” not being set, do the following.
7. Open PowerShell and type:
   1. `cd "C:\Program Files\Git\bin"`
   2. `git config --global user.name "< your name >"`
   3. `git config --global user.email "< your email address >"`
8. Click on the “…” menu in the “Source Control” pane, and select “Push” to push the changes to GitHub.
9. If you are prompted, log into GitHub to authenticate.
10. Click on the “…” menu in the “Source Control” pane, and select “Push” to push the changes to GitHub.



## Run the playbook 

In Automation Platform, create a new template with the following: 

* Name: **error_handling**
* Inventory: **First Inventory**
* Project: **ansible-working**
* Execution Environment: **Default execution environment**
* Playbook: **report.yml**
* Credentials: **Linux credentials**



Run the `error_handling` job.

You can confirm it ran successfully by reviewing the job output. 



### Simulate a failure 

Now, let's simulate a down service by running the `service_down` job. 



After it completes, run the `error_handling` job again and you'll see the output shows that the connection failed. 



Finally, run the `service_up` job, and then rerun the `error_handling` job. 



### Bonus 

Use ad-hoc to confirm the `/home/ansible/lab-error-handling/transaction_list` file was created and is formatted correctly. 

## Congrats!

