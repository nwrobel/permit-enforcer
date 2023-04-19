# permit-enforcer
This is a simple tool that keeps file/folder permissions correctly set by applying them based on a configuration file.
The script simply applies the permissions on the files based on config file data.

This tool only runs on Linux (tested in Ubuntu 18.04, 20.04)

## Installation & Usage
- Make sure python3 and python3-venv are installed
- Download this repo project, save it locally
- cd to the repo folder
- Run the script `setup.sh` to set up the necessary files (creates a Python virtual env inside the repo dir)
- Create a new file `permissions.csv` (any name/path is okay, specify it later) and write your permission configuration data there
- Update the Python script `apply-permissions.py` to change the path of the permissions.csv to your permissions config file path
- While in the repo directory, run (use sudo if needed to change the owner/group or mask of the files):
```
sudo ./pv-venv-linux/bin/python3 apply-permissions.py 
```
