# Lab Setup 

# Open the lab repo in VS Code

### Step 1: Open the folder

1. Open Visual Studio Code
2. In a new Visual Studio Code window, click **File** -> **Open Folder** and browse to `C:\Users\TEKstudent\Downloads\repos\automation-dev`
3. After opening the folder, click the third icon in the left toolbar for source control. Next to **changes**, click the three dots and choose **pull**.


## Set up a remote SSH session in Visual Studio Code.   

### Create the SSH configuration file.

On the left sidebar, click the icon that looks like a computer with a connection icon.

In the Remote Explorer, hover your mouse cursor over **SSH**, click on the gear icon (⚙️) in the top right corner, and select the top option: `C:\Users\tekstudent\.ssh\config` This will open the SSH configuration file in a new editor tab.


### Add the SSH configuration for the lab servers.
Add the following lines to the SSH configuration file, replacing `<IP of Tower server from the spreadsheet>` with the actual IP address of your Tower.

```plaintext
Host tower
  HostName <IP of Tower server from the spreadsheet>
  IdentityFile "C:\Users\tekstudent\Downloads\repos\automation-dev\keys\lab.pem"
  User ansible
```

### Save the SSH configuration file.
Save the changes to the SSH configuration file and close it.


### Connect to the lab servers.
1. In the Remote Explorer, you should now see the entry for the Tower server under "SSH Targets."
2. Click on the entry to connect to the Tower server.
3. Visual Studio Code will open a new window connected to the Tower server.
4. When prompted for the Operating System, choose 'Linux'.  
5. Accept the SSH fingerprint
6. You can now open a terminal in this new window and run commands on the Tower server.

### Create a working directory

In Visual Studio Code, you can create a new folder or file as if it was on your local machine.
Click **Open Folder** and select `/home/ansible`.
In future labs, you will create a directory for each lab.

## Confirm Ansible is configured correctly 

In the VS Code window connected to your Ansible Tower, open a terminal and run: 
```bash 
ansible all -i inventory -m ping 
```

This command confirms ansible can connect to the managed nodes and they have Python installed. 

The expected output should look similar to below: 

```
ControlNode | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
TargetNode1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
TargetNode2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

## Congratulations!
You have successfully set up your lab environment and are ready to start working on the labs.
