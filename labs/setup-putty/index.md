# Lab Setup 
### Visual Studio Code

The username for SSH is 
`ubuntu`

In Visual Studio Code, open a terminal and `cd` to the lab keys directory. 
```
cd "C:\Users\tekstudent\Downloads\repos\automation-dev\keys"
```
### SSH to the Ansible controller

```
ssh -i lab.pem ansible@<Controller IP from spreadsheet>
```

