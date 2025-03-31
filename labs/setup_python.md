# **Hands-On Lab: Installing Python on Windows (64-bit)**

## **Overview**
In this lab, you will download and install Python on a Windows machine using the official Python Windows Installer. You will configure the installation to add Python to the system `PATH` and verify the installation in Visual Studio Code.

---

## **Step 1: Download Python Windows Installer**
1. Open your web browser and navigate to the official Python downloads page:  
   👉 [Python Windows Downloads](https://www.python.org/downloads/windows/)
2. Scroll down to the **"Stable Releases"** section.

---

## **Step 2: Install Python as an Administrator**
1. Open **File Explorer** and navigate to your **Downloads** folder.
2. Locate the downloaded `python-3.x.x-amd64.exe` file.
3. Click the **"Download Windows Installer (64-bit)"** for the latest stable version of Python.
4. Once the download is complete, locate the installer file (e.g., `python-3.x.x-amd64.exe`) in your **Downloads** folder.
5. **Right-click** the installer file and select **"Run as administrator."**
6. If prompted by the **User Account Control (UAC)**, click **"Yes"** to proceed.

---

## **Step 3: Configure Installation Options**
1. At the bottom of the installer window, check the box **"Add Python.exe to PATH."**  
   📌 *This step ensures Python can be accessed from any command prompt or terminal.*
2. Click **"Install Now."**
3. Wait for the installation process to complete.
4. Once finished, click **"Close."**

---

## **Step 4: Verify Installation in Visual Studio Code**
1. **Restart** Visual Studio Code (close and reopen it).
2. Open the **Integrated Terminal** in VS Code:
3. Run the following command to confirm Python is installed and available in your system's PATH:

```
   python --version
```
