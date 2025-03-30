# Setup Student VM's

### Launch VS Code in Administrator Mode to install software in a Terminal window

### Step 1: Run VS Code as Administrator

1. Close any open instances of Visual Studio Code.
2. Search for "Visual Studio Code" in the Start menu.
3. Right-click on it and select **Run as Administrator**.
   - If prompted by User Account Control (UAC), click **Yes** to allow it.

---

### **Step 2: Open the Integrated Terminal**

1. In VS Code, click on the **Terminal** menu at the top and select **New Terminal**.
   - Alternatively, use the shortcut: `Ctrl + ~`.
2. Ensure the terminal is using **PowerShell**, as Chocolatey requires it.

---

### **Step 3: Use Chocolatey to install needed packages**

1. Install some required packages:

   ```powershell
   choco install git wget awscli terraform python -y
   ```

---

### **Important Note:**

Always run VS Code in **Administrator mode** whenever you need to use Chocolatey to install or manage software that requires system-level changes.

# Install extensions for VS Code

### **Step 1: Open Visual Studio Code**

1. Launch **Visual Studio Code** on your computer.
2. Make sure you have it installed. If not, you can download it from [https://code.visualstudio.com/](https://code.visualstudio.com/).

---

### **Step 2: Open the Extensions View**

1. In VS Code, click on the **Extensions** icon on the left-hand sidebar. 
   - Alternatively, press `Ctrl + Shift + X` to open the Extensions view.

---

### **Step 3: Search for the following extensions**

1. In the search bar at the top of the Extensions view, search for each:
   * Terraform
   * Ansible
   * Python
2. Install each extension. 

NOTE: There are multiple **Terraform** extensions. Install the one by **HashiCorp**.

## Restart Visual Studio Code

Restart VS Code to update the path to see the newly installed applications.

---

# Open the lab repo in VS Code

### Step 1: Clone the repository

1. Open Visual Studio Code
2. In the Visual Studio Code sidebar, click the third icon down “Source Control”
3. Click “Clone repository” and enter the `https://github.com/jruels/automation-dev`
4. In the File Explorer window that pops up, create a new folder “repos” and select it.
5. After cloning the repository, in Visual Studio Code, click the “Explorer” icon at the top of the left sidebar.

# Configure AWS credentials

### **Step 1: Log into the AWS Console**

1. In a browser, log into the [AWS Console](https://console.aws.amazon.com/).
2. Search for IAM in the search bar.
3. Click **IAM**
4. Click **Users**.
5. Click **autodev-admin**.
6. Click **Security Credentials**.
7. Scroll down to **Access Keys**
   1. Click **Actions** -> and **Deactivate** and **Delete** any existing keys.

8. Click **Create access key**
9. Select **Command Line Interface (CLI)**. 
10. Check the confirmation box at the bottom of the page and click **Next**.
11. Skip the description and click **Create access key**.
12. **IMPORTANT:** Copy the **Access key** and **Secret access key** and save them somewhere. You can optionally download the csv file for easy reference. 

---

### **Step 2: Use AWS Configure**

1. Run aws configure in the Visual Studio Code terminal. 
2. Supply the required information.
   * Credentials 
   * Region = `us-west-1`
3. Select the default option for remaining.

---

### **Step 3: Test AWS CLI**

1. Confirm that `aws` can use the credentials.

   ```
   aws sts get-caller-identity
   ```

2. You should see your account information returned.



## Congratulations

Congratulations, you've successfully configured your machine.
