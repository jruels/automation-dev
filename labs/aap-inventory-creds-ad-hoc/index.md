# AAP - Inventories, credentials, and ad-hoc commands

## Objective

This exercise will cover

- Locating and understanding:
  - Ansible Automation Controller **Inventory**
  - Ansible Automation Controller **Credentials**
- Running ad hoc commands via the Ansible Automation Platform web UI


## Create an Inventory

Let’s get started: The first thing we need is an inventory of managed hosts. This is the equivalent of an inventory file in Ansible Engine. There is a lot more to it (like dynamic inventories) but let’s start with the basics.

In the web UI menu on the left side, go to **Resources** → **Inventories**, click the **Add** button and choose **Add inventory**

Provide the following:

* **Name**:  First Inventory
* **Description**: My first inventory file
* **Organization**: Default

Click **Save**

At the top of the page click the **Hosts** button, the list will be empty since we have not added any hosts yet.



Let's add our hosts.  



For each (`node1`, `node2`) Add the host to the inventory in Automation Platform:

Click the **Add** button and give a **Name**, and **Description**: 

* **Name**: Server (1 or 2)

* **Description**: Node (1 or 2) from the spreadsheet

* Under **Variables** confirm **YAML** is highlighted and then paste the following:

  ```yaml
  ansible_host: <IP of node (1 or 2) from spreadsheet> 
  ```

  

* Click **Save** 

You have now created an inventory with new managed hosts.



## Machine Credentials

One of the great features of the Ansible Automation Platform is to make credentials usable to users without making them visible. To allow AAP to execute jobs on remote hosts, you must configure connection credentials.

> **TIP**:This is one of the most important features of Automation Platform: **Credential Separation**! Credentials are defined separately and not with the hosts or inventory settings.

We need to configure the Ansible Automation Platform with the Controller SSH Private Key to enable it to connect to our managed nodes.



In the VS Code window that is connected to the Controller, expand `.ssh` and click `id_rsa`

Copy the **complete private key** (including “BEGIN” and “END” lines) and save it for the next step.



Now configure the credentials to access the managed hosts from Ansible Automation Platform.

In the **Resources** menu choose **Credentials**, and click **Add** then fill in the following:

* **Name**: Linux credentials
* **Description**: Credentials to authenticate over SSH
* **Organization**: Default
* **Credential Type**: Machine

Under **Type Details** fill in: 

* **Username**: ansible

* **SSH Private Key**: Paste the private key from above.  

**Privilege Escalation Method**: sudo 

> **TIP**: Whenever you see a magnifying glass icon next to an input field, clicking it will open a list to choose from.

* Click **Save**

Go back to the **Resources -> Credentials -> Linux credentials** and note that the SSH key is not visible.

You have now set up credentials for Ansible to access your managed host.



## Run Ad Hoc Commands

As you've done with Ansible before you can run ad hoc commands from AAP as well.

In the web UI go to **Resources → Inventories → First Inventory**

- Click **Hosts** at the top of the page to change into the hosts view.
- Click **Run Command**.
- On the next screen specify the ad-hoc command: 
- **Module**: choose `ping`
- Click **Next**
- **Execution Environment**: Default execution environment
- Click **Next**
- **Machine Credential**: Linux credentials
- Click **Next**
- Click **Launch**, and watch the output. 



The simple **ping** module doesn’t need options. For other modules, you need to supply the command to run as an argument. Try the **command** module to find the user ID of the executing user using an ad-hoc command.

- **Module**: command
- **Arguments**: id

> **TIP**: After choosing the module to run, Tower will provide a link to the docs page for the module when clicking the question mark next to "Arguments". This is handy, give it a try.



## Challenge Lab: Ad Hoc Commands

Run an ad-hoc command to make sure the package `tmux` is installed on the host. If unsure, consult the documentation either via the web UI as shown above or by running `ansible-doc yum` on your AAP control host.



The instructor will provide the solution. 



## Congrats!
