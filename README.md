# Typeracerbot
This selenium automaton project bit human typing speed.. Just for fun .😥

![Preview](assets/typeracer-preview.gif)

# Installation
First you need some requirements to fill up on you system.

## Requirments
- Python 3.10+ (Windows [Download](https://www.python.org/downloads/))
- [Microsoft edge browser](https://www.microsoftedgeinsider.com/en-us/download) and [WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [Selenium 4](https://pypi.org/project/selenium/)
  
## First time run dependency install
``` pip install -r requirments.txt ```


# Some example of use case

### Place you name on all typeracer mode auto. It is require logged account browser.
``` python main.py ```

### Login and run on all mode
``` python main.py -u <username> -p <password> ```

### Run with specific  mode only
``` python main.py --justOne https://play.typeracer.com/?universe=accuracy ```

### Run with specific  mode and infinity loop
``` python main.py --justOne https://play.typeracer.com/?universe=accuracy -l ```

### Run with specific  speed rate
``` python main.py --speed 0.2 ```

### Create fake/random accounts. It is required a human for solving recapture
``` python main.py --createAccounts 10```

# Help
```
usage: main.py [-h] [--justOne JUSTONE] [--speed SPEED] [--createAccounts CREATEACCOUNTS] [-l] [-u U] [-p P]

Auto geting blc exp. Just for fun!

options:
  -h, --help            show this help message and exit
  --justOne JUSTONE     Target just one mode
  --speed SPEED         Set your speed
  --createAccounts CREATEACCOUNTS
                        Create multiple accounts. It is required human for recapture solving.
  -l                    Set as infinity loop
  -u U                  Set your username
  -p P                  Set your password
  ```

If you have any issue on this program. Do not hesitate to create issue on this repository. Thank you. 
