# permit-enforcer
This is a simple tool that keeps file/folder permissions correctly set by applying them based on a configuration file.
The script simply applies the permissions on the files based on config file data.


This tool only runs on Linux (tested in Ubuntu 18.04)

## Installation
- Download this repo project, save it locally
- cd to the repo folder
- Run the script `setup.sh` to set up the necessary files (creates a Python virtual env inside the repo dir)

## Usage
The config file defines which files to set the permissions on and what those permissions should be.
See the file `permissions.template.csv` for some sample data of how to format the CSV file to define the files and permissions.

Next, create a new file `permissions.csv` inside of the repo directory in the same folder as the template 
and place your actual config CSV data in there. The script is designed to read from the config file with this name located in the repo.

Finally, run the script. Doing this will give you the required sudo permissions needed to change the
file permissions as you defined. Make sure you are cd into the repo folder and then run:

```
sudo ./pv-venv-linux/bin/python3 apply-permissions.py 
```