# M$ Rewards
A Selenium based automatic Microsoft Rewards bot that literally makes you money! 
## Disclaimer
I am not responsible for your account(s). This program is a use at your own risk, Microsoft holds the right to lock, or ban your account.
## Features
M$ Rewards has many features including:
* DOES NOT REQUIRE WINDOWS 10 ADMINISTRATOR (read below)
* Automatic Mobile search
* Automatic Desktop search
* Automatic Daily set completion
* Automatic Quest and Punch Card completion
* Automatic "More Activites" completion
* Detect locked, suspended, and "unusual activity" accounts. 
* Should be bot undectable, who really knows though.  
* Multi-account management (support for as many accounts as you want, although the most ever tested was 3)
## First Time Set Up
To initally run M$ Rewards, you will need to open up command line and type in:
```
pip install -r requirements.txt
```
If you have administrator you can skip to **Configuration** running the file, however if you don't, you want to download the latest edge driver [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/). Place this file where ever you want, but make sure to copy the file path. In credentials.json change "webdriver location" to the webdriver's location, eg. the example webdriver location is stored in "C://Utility//msedgedriver.exe". 
```
"webdriver location": "C://Utility//msedgedriver.exe"
```
## Configuration
BEFORE READING ON FURTHER MAKE SURE THE FIRST NAME ON YOUR MICROSOFT ACCOUNT IS IN YOUR EMAIL EG. Sarah and sarahjones@gmail.com, Harry and harrylarry@outlook.com, or Tacos and tacosaretasty@tacos.com. The ONLY exception to this rule is if your microsoft account does not have a first name and just shows its email, eg. email@email.com = email@email.com.
To add, change, or remove microsoft acccounts, open "credentials.json", and change the file accordingly. For example: (Keep in mind, the more accounts you run, the higher chance you get detected as a bot, your absolute maximum should be 6 per IP address.)
```
{
  "username": "username@example.com",
  "password": "Password"
},
```
You want to put in your microsoft email in the "username" section. IMPORTANTLY, make sure the email you are using has an attached microsoft account. And obviously put your password in the "password" section. To make sure M$ Rewards works correctly on all of your accounts, make sure to edit config inside credentials.json.
```
"config": {
  "How many accounts are you using?": 1,
  ...
},
```
## Running
To run the file download Python **3.10** and run the following command. Note: M$ Rewards may work on previous and future versions of python however they are not fully tested and are to be used at your own risk. 
```
python main.py
```
You can use flags such as --delay which will delay the script from running by 1 to 30 minutes (good for users who are running this in task scheduler), or --logs which will activate logging to a log file (once again good for automaters), and --calculatetime which will not run the script but rather use the M$ Calculator, read below to find out more.
```
python main.py --delay --logs
```
This process can be streamlined on windows by downloading python, right clicking "main.py", clicking "open with", and click python. (Make sure to click "always use this app to open .py files") However you will still need terminal to use --delay, --logs, and --calculatetime
## M$ Calculator
M$ Calculator is a way to calculate how long it will take to purchase an item using M$ Rewards. To use M$ Calculator, you want to change credentials json to:
```
  ...
    "how much does it cost to buy your item": 99.98
  ...
```
The first option you must answer is "redeem_microsoft_gift_card?", which basically means, can the product you want to buy be bought on the Microsoft or Xbox store? If so, type in "yes", if not enter in "no". The second option is "how much does it cost to buy your item in ", which self explaintory-ly asks how expensive is the product you wish to purchase. To run M$ Calculator, use the command down below.
``` 
python main.py --calculatetime
```
It will return an result that should look something like this:
``` 
It is estimated that it will take 206 days to get 20 $5 gift cards (7 giftcards on each of the 3 accounts) to purchase your item that costs $99.98, leaving you an excess giftcard value of $5.02!
```
## Credit
Credit to [@charlesbel]("https://github.com/charlesbel") for originally coming up and developing the idea!
