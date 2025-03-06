# Ansible Automation Platform

## Install Ansible Automation Platform

### Prerequisites

#### Red Hat Developer account

Go to the [Red Hat Developer portal](https://developers.redhat.com/about), click "Join now," and fill out the form. 

Provide the following: 

* Username 
* Email address 
* Job role 
* Password 



#### Red Hat registry service account token

Navigate to the [Registry Service Account Management Application](https://access.redhat.com/terms-based-registry/), and log in if necessary.

1. From the **Registry Service Accounts** page, click the **New Service Account** button.

2. Provide a name for the Service Account. It will be prepended with a fixed, random string.

   - Enter a description.
   - Click **create**.

3. Navigate back to your Service Accounts.

4. Click the Service Account you created.

   - Note the username, including the prepended string (i.e. `XXXXXXX|username`). This is the username that should be used to log in to registry.redhat.io in the `inventory` file.
   - Note the password. This is the password that should be used to authenticate to [registry.redhat.io.](https://registry.redhat.io) in the `inventory` file.

   

Log in to the control node as `ec2-user` 

**RUN ON THE CONTROL NODE**


### Install Automation Platform 


Install `subscription-manager`

```bash
sudo yum install -y subscription-manager
```



Register VM with Red Hat package repos

```bash
sudo subscription-manager register --auto-attach
```



When prompted, provide your Red Hat Developer username and password.

Click [Here](https://access.redhat.com/downloads/content/480) to download the Ansible Automation Platform installer. 

* Log in to the portal 

* At the top, select  version 2.4 for `RHEL 9`

* Click the "Download Now" link on the "Bundle" installer

  ![image-20220913022904472](images/image-20220913022904472.png)
  
  

Copy the installer to the lab VM. 

## Macos/Linux
Use `scp` to copy the setup file from your local machine to the Ansible Control node.



## Windows

Copy the installer to the lab VM using WinSCP:


Create a new connection to the lab server:

- Change File protocol to SCP
- Enter the Hostname of the Lab VM
- Enter the username provided by the instructor

![img](https://winscp-static-746341.c.cdn77.org/data/media/screenshots/login.png?v=6990)



Configure SSH Key Authentication:

* Browse the key provided by the instructor.

![img](https://winscp-static-746341.c.cdn77.org/data/media/screenshots/login_authentication.png?v=6990)



After connecting, copy the download setup file to the Lab VM in `/home/ec2-user`

<img src="https://winscp-static-746341.c.cdn77.org/data/media/screenshots/commander.png?v=6990" alt="img" style="zoom:85%;" />



Connect to the server using SSH



Extract the installer 

If the file is a ``.tar`` run:

```bash
tar -xvf ansible-automation-platform-setup-*.tar
```

If the file is a `.tar.gz` run:

```bash
tar -zxvf ansible-automation-platform-setup-*.tar.gz
```



Enter directory 

```bash
cd ansible-automation-platform-setup-<version>
```



The latest version of AAP does not support installation on `localhost`. Due to this, we need to add the following to `/etc/hosts`

Using `sudo` open `/etc/hosts` in your favorite editor. 

```
sudo vi /etc/hosts
```



Now add `aap.localhost.com` to the end of the line beginning with `127.0.0.1` so it looks like this:

```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 aap.localhost.com
```

Save the file and run the following to test.

```
ping aap.localhost.com
```



Delete the original inventory file

```bash
rm -rf inventory
```



Create a new `inventory` file and paste the following into it.

```
[automationcontroller]
aap.localhost.com ansible_connection=local

[database]

[all:vars]
admin_password='Password1234'
redis_mode = standalone

pg_host=''
pg_port=''

pg_database='awx'
pg_username='awx'
pg_password='Password1234'

registry_url='registry.redhat.io'
registry_username='<YOUR_REGISTRY_NAME>'
registry_password='<YOUR_REGISTRY_TOKEN'
```

Set the following in the `inventory` file (if not already completed) 

* admin password = Password1234   
* pg_password = Password1234   
* registry_username = The username generated earlier in the lab (i.e 15765574|ansible-tower)   
* registry_password = The token you generated earlier in the lab.   

Run installation script

```bash
sudo ./setup.sh -e required_ram=2048
```





**NOTE**: This will take some time to complete.



After the script above completes, you can access the Dashboard at the following URL (replacing `Server IP` with your lab VM IP)  

https://[Server IP from spreadsheet]



Log into the dashboard with the username `admin` and the password you specified in the `inventory` file `Password1234`



> NOTE: You can reset the admin password by running the following on the Ansible Control VM:
>
> ```bash
> sudo awx-manage changepassword admin
> ```



You will see a screen asking to register Automation Platform. Log in with your developer credentials.

<img src="images/image-20220222022946979.png" alt="image-20220222022946979" style="zoom: 33%;" />



Select your subscription, and click "Next"

<img src="images/image-20220222024205420.png" alt="image-20220222024205420" style="zoom:50%;" />

Accept defaults, and click "Next"

<img src="images/image-20220222024307322.png" alt="image-20220222024307322" style="zoom:45%;" />

Accept the license agreement and click "Submit"



You should now see the dashboard 

![image-20220222024405897](images/image-20220222024405897.png)

### Congratulations
