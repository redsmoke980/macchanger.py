#!/usr/bin/env python3

import subprocess   # Allows to run terminal commands from this program
import argparse     # allows for arguments to be added prior to program launch
import re           # Regex
import colorama     # Allows colored text
from colorama import init
from colorama import Fore, Back, Style # Allows to color the text, background, and change style

# resets the colors after every line of code to prevent blocks of code from being colored
init(autoreset=True)

# function to gather arguments prior to the program running (Python3 macchanger.py -i [interface] -m [mac])
def get_arguments():
    parser = argparse.ArgumentParser()

    # Creates the options needed for the program to be initialized
    # And creates the help menu for each option
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="mac",help="New MAC address ('o' changes to the original MAC)")

    # Options consist of [interface] and [MAC address]
    # Arguments consist of [-i] [-m]
    # Allows us to prepare the options to go into variables
    options = parser.parse_args()

    # checking that the interface and MAC address have been provided
    if not options.interface: # if the interface was not provided, return a help message to advise of the issue
        #code to handle error
        parser.error(Fore.RED + Style.BRIGHT + "[-] Please specify an interface, use --help for more info.")
    elif not options.mac: # if the MAC address was not provided, return a help message to advise of the issue
        #code to handle error
        parser.error(Fore.RED + Style.BRIGHT + "[-] Please specify a MAC, use --help for more info.")

    # returns the interface and MAC to be used later in the program
    return options

# function to change the mac using the "ip" command
def change_mac(iface, mac): # Function requires the interface and mac in order to run

    # Formatting
    print("\n" + ("-" * 60))
    print(Fore.GREEN + Style.BRIGHT + "\n[+] changing MAC address for " + iface + " to " + mac + "\n")
    print("-" * 60)

    # Subprocess.call with a list [] inside prevents the user from adding additional commands to be run by using ;
    # Turning off the interface
    subprocess.call(["sudo", "ip", "link", "set", "dev", iface, "down"])

    # Changing the MAC address
    subprocess.call(["sudo", "ip", "link", "set", "dev", iface, "address", mac.upper()])

    # Turning back on the interface
    subprocess.call(["sudo", "ip", "link", "set", "dev", iface, "up"])

# Function that checks to see if the MAC address you want is already the current one
def get_current_mac(iface, new_mac): # Requires the interface and the new mac from the provided arguments

    # outputs the output of the "ip" command into a variable and decodes the string
    ip_result = subprocess.check_output(["ip", "a", "show", iface]).decode("utf-8")

    # Uses RegEx to look for the pattern XX:XX:XX:XX:XX:XX in the output of the previous command and puts it into a new variable
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ip_result)

    # Checks to see if there is something in the mac_address_search_result variable
    if mac_address_search_result:

        # Prints the found MAC address that is currently used on the Interface
        # group(0) says the first item in the list since "ip" also has a broadcast address with the same format as the MAC
        print(mac_address_search_result.group(0))

        # Checks to see if the current MAC address is the same as the requested one
        if mac_address_search_result.group(0) == new_mac:

            # Prints an error message and returns True
            print("\n" + Fore.YELLOW + Style.BRIGHT + "[-] The MAC address you have selected is already the current MAC address")
            return True

        else:
            # Returns false if the current MAC address and new MAC address are different
            return False
    else:
        # Error message incase program has issues reading the output of the "ip" command
        print(Fore.RED + Style.BRIGHT + "[-] Could not read MAC address")

# Function to check the new MAC address
def check_new_mac(iface, new_mac):

    # outputs the output of the "ip" command into a variable and decodes the string
    ip_result = subprocess.check_output(["ip", "a", "show", iface]).decode("utf-8")

    # Uses RegEx to look for the pattern XX:XX:XX:XX:XX:XX in the output of the previous command and puts it into a new variable
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ip_result)

    # Checks to see if there is something in the mac_address_search_result variable
    if mac_address_search_result:

        # Prints the found MAC address that is currently used on the Interface
        # group(0) says the first item in the list since "ip" also has a broadcast address with the same format as the MAC
        print(mac_address_search_result.group(0))

        #checks to see if the MAC address was successfully changed
        if mac_address_search_result.group(0) == new_mac.lower():

            # Prints success message
            print("\n")
            print(Fore.GREEN + Style.BRIGHT + "[+] The MAC address has been successfully changed")

        # If it didn't succeed in changing
        else:

            # Prints failure message
            print("\n")
            print(Fore.RED + Style.BRIGHT + "[-] The MAC adress failed to change")

    else:
        # Error message incase program has issues reading the output of the "ip" command
        print(Fore.RED + Style.BRIGHT + "[-] Could not read MAC address")



# Puts the returned interface and MAC address into the options object
options = get_arguments()


# pulls the interface item from the options list and puts it into an interface variable
iface = options.interface

#sets the original MAC address of the users interface incase they need to change back (must be set manually per interface)
original_mac = "60:57:18:55:72:60"

# if the mac provided was "o", then they user wanted the original MAC from above
if options.mac == "o":
    # sets mac variable equal to the original mac
    mac = original_mac

else:
    # sets the mac variable to the provided mac address
    mac = options.mac

# prints the current MAC address
print(Fore.CYAN + Style.BRIGHT + "\nCurrent " + iface + " address")
# used for formatting
print("*" * 30)

# checks to see if the current mac is the mac requested and sets the output into a variable
# provides the mac requested for the specified interface
is_current_mac = get_current_mac(iface, mac)

# Deteermines if the program will try to change the MAC address based on if the current MAC and the new MAC are the same
if is_current_mac == True:
    #prints message before skipping out of the program
    print(Style.BRIGHT + "[-] Terminating program")

# changes MAC if new MAC is not current MAC
elif is_current_mac == False:

    # Runs the change_mac function while providing the interface and the new MAC
    change_mac(iface, mac)

    # Formatting
    print(Fore.CYAN + Style.BRIGHT + "\nNew " + iface + " address")
    print("*" * 30)

    # Checks to see if the MAC was successfully changed
    check_new_mac(iface, mac)
