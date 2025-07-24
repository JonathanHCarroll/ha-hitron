# ha-hitron

A Python utility for interacting with Hitron router APIs (API version 1.11, Software Version 7.1.1.32+). This tool allows you to query system information, check router version, and perform actions such as rebooting the router via command-line.

## Features
- Query router system information
- Check router firmware and API version
- Reboot the router remotely
- Command-line interface with configurable options

## Requirements
- Python 3.7+
- [requests](https://pypi.org/project/requests/)

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/ha-hitron.git
   cd ha-hitron
   ```
2. Install dependencies:
   ```sh
   pip install requests
   ```

## Usage
Run the script with desired options:
```sh
python hiron_router.py [options]
```

### Options
- `-u`, `--username`   Router username (default: `cusadmin`)
- `-p`, `--password`   Router password (default: `uni.2311`)
- `-i`, `--ip`         Router IP address (default: `192.168.0.1`)
- `--sysinfo`          Query system information (default: enabled)
- `--reboot`           Reboot the router
- `-v`, `--verbose`    Enable verbose logging

Example:
```sh
python hiron_router.py -u cusadmin -p mypassword --sysinfo
```

## Output
- System information and other responses are printed to the console and can be saved to `output.txt` in pretty-printed JSON format.

## Deployment
To deploy or copy files to a remote server, consider using an `rsync` or `scp` script (see project documentation for details).

## License
Specify your license here (e.g., MIT, Apache 2.0, etc.). 
