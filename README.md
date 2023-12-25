# permit-enforcer
This tool keeps Linux file/folder permissions correctly set by applying them based on a configuration file.
Only for on Linux-based, uses `chown` and `chmod` (tested in Ubuntu 18.04, 20.04)

## Installation & Usage
- Make sure python3 and python3-venv are installed
- Download this repo project, save it locally
- cd to the repo folder
- Run the script `setup.sh` to set up the necessary files (creates a Python virtual env inside the repo dir)
- Open file `permissions.json` (in config/) and write your permission configuration there
  - tip: you can use any config file you create here
- While in the repo directory, run (use sudo if needed):
```
sudo ./pv-venv-linux/bin/python main.py --config-file "permissions.json"
```
