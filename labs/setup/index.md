# Lab Setup 
If you haven't already done so, clone the git repository to your local machine using Visual Studio Code.


## Mac/Linux


Open a terminal and `cd` to the extracted lab directory. Inside the directory, you will see a `keys` directory. Enter it using `cd` and run the following commands.

### Set permission on SSH key

```
chmod 600 lab.pem
```

### SSH to lab servers
```
ssh -i lab.pem ec2-user@<VM IP from the spreadsheet> 
```

## Windows 

Windows users can use the built-in PowerShell SSH client to connect to the lab servers.
### PowerShell

Open a Terminal session in Visual Studio Code and `cd` to the extracted lab directory. Inside the directory, you will see a `keys` directory. Enter it using `cd` and run the following commands.

```
ssh -i lab.pem ec2-user@<VM IP from the spreadsheet> 
```
After logging into the Tower server, open a new terminal session and connect to Managed Node 1, then repeat the process for Managed Node 2.

## Set up a remote SSH session in Visual Studio Code.   
The first thing needed is to install the Remote - SSH extension.
1. Open Visual Studio Code and click on the Extensions icon in the Activity Bar on the left side of the window.
2. Search for "Remote - SSH" in the Extensions Marketplace.
3. Click on the "Install" button to install the extension.
4. Once installed, you will see a new icon in the left sidebar that looks like a computer with a remote connection symbol.
5. Click on the icon to open the Remote Explorer.

### Create the SSH configuration file.
In the Remote Explorer, rest your mouse cursor over **SSH**, click on the gear icon (⚙️) in the top right corner, and select "Open SSH Configuration File." This will open the SSH configuration file in a new editor tab.
### Add the SSH configuration for the lab servers.
Add the following lines to the SSH configuration file, replacing `<VM IP from the spreadsheet>` with the actual IP addresses of your Tower server.

```plaintext
Host tower
  HostName <IP of Tower server from the spreadsheet>
  IdentityFile <Path to the cloned lab directory/keys/lab.pem>
  User ansible
```

### Save the SSH configuration file.
Save the changes to the SSH configuration file and close it.
### Connect to the lab servers.
1. In the Remote Explorer, you should now see the entry for the Tower server under "SSH Targets."
2. Click on the entry to connect to the Tower server.
3. Visual Studio Code will open a new window connected to the Tower server.
4. You can now open a terminal in this new window and run commands on the Tower server.

### Create a working directory
In Visual Studio Code, you can create a new folder or file as if it was on your local machine.
Click **Open Folder** and select `/home/ansible`.
In future labs, you will create a directory for each lab.

## Congratulations!
You have successfully set up your lab environment and are ready to start working on the labs.
