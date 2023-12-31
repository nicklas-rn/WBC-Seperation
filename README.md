# Installation
Note: This installation is for beginners with few programming experience and no intent to modify this software. Consequently, this installation does not use a virtual environment but instead installs programs system-wide.
## 1. Installation of prerequisites
### 1.1 Install Git
Open a terminal window and enter the following command to check if you have Git installed on your system:
```
git --version
```
If Git is installed, this command will display the installed version of Git. Otherwise, go to https://git-scm.com/downloads and download the Git version for your operating system.
### 1.2 Install Python
Now, perform the same for Python. In a terminal window, enter the following command to check if you have Python installed on your system:
```
python --version
```
If Python is installed, this command will display the installed version. Otherwise, go to https://www.python.org/downloads/ and download Python for your operating system. Please make sure to install **version 3.10** or lower.
### 1.3 Install Packages
This software uses a few Python packages. To install them, enter the following command:
```
pip install -r requirements.txt
```

## 2. Installation of this software
To install this software, you have to clone this repository to your system. First, open a terminal window and go to the folder where you want it installed:
```
cd path\to\folder
```
Replace 'path\to\folder' with the respective path to the desired folder. **Write the path to the folder down** somewhere. You will need it whenever you want to start the software.
Then, clone this repository to your system with the following command in the same terminal window:
```
git clone https://github.com/nicklas-rn/WBC-seperation
```
Now, when you go to the previously specified path in your explorer/finder, you should find a folder with the name WBS-Seperation. The installation was successful!

# Running the software
First, go to the folder 'WBC-Seperation' in a terminal window. To achieve that, open a terminal window and enter the following command:
```
cd path\to\folder\WBC-Seperation
```
To run the software, enter:
```
python app.py
```
Then, open your browser and open the following domain: http://127.0.0.1:5000
You're good to go!

# Updating the software
If other developers have made changes to this software, you can update your version by pulling this repository. To achieve that, first go to the 'liquid-handler' folder in a terminal window, in case you aren't there already. Then, use the following command to pull the new version:
```
git pull
```
Now, you have the current version on your PC!
