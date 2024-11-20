# Lab Setup 
At the top of the lab page, click **View on GitHub**. Click the green **Code** button in the top right corner, then click **Download as zip**. Once the download is done, extract the zip file and put it somewhere you can easily access it.

### Mac/Linux

The username for SSH is 
`ec2-user`

Open a terminal and `cd` to the extracted lab directory. Inside the directory, you will see a `keys`directory. Enter it using `cd` and run the following commands.

### Set permission on SSH key

```
chmod 600 lab.pem
```

### SSH to lab servers

```
ssh -i lab.pem <user>@<VM IP> 
```

### Set up Putty

If you don’t already have it, download Putty from [here](https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe) and save it to your desktop.

Open Putty and configure a new session.

![img](https://jruels.github.io/openshift-admin/labs/openshift-deploy/images/putty-session.png)

Expand Connection -> SSH -> Auth -> Credentials, click “Browse”, and then choose the `lab.ppk` file from the extracted lab directory

![image-20230918185300995](https://jruels.github.io/openshift-admin/labs/openshift-deploy/images/putty-auth.png)

Remember to save your session.
