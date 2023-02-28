import subprocess
import argparse
import os
import math
import requests
from bs4 import BeautifulSoup
import termcolor
from termcolor import colored
from urllib.parse import urljoin
import requests
import urllib.parse
from bs4 import BeautifulSoup

banner = colored('''--------------------------------------------------------------------------
############         ##         ##        ##  ############  #
#                   #  #        # #      # #  #             #
#                  #    #       #  #    #  #  #             #
#                 #      #      #   #  #   #  #             #
#                ##########     #    #     #  ############  #
#               #          #    #          #  #             #
#              #            #   #          #  #             #
############  #              #  #          #  ############  ###########
                                                                            v0.1
                                                                            AUTHOR: SOURAV CHAKRABORTY
---------------------------------------------------------------------------------''', '''cyan''')

print(banner)
parser = argparse.ArgumentParser(description="supply the url")
parser.add_argument('url', type=str, help='get all the URL of the domain')
parser.add_argument('--js', default=False, action='store_true', help='enable downloading of javascript files')
parser.add_argument('--be', default=False, action='store_true', help='enable detection of Backend technologies and CMS')
parser.add_argument('--dsearch', default=False, action='store_true', help='search for hidden directories based on backend technologies')
parser.add_argument('--pfuzz', default=False, action='store_true', help='fuzz for working parameters')
parser.add_argument('--slack', default=False, action='store_true', help='enable slack notification')

args = parser.parse_args()

url = args.url
js = args.js
be = args.be
dsearch = args.dsearch
pfuzz = args.pfuzz
slack = args.slack



asp = url + "index.asp"
php = url + "index.php"
html = url + "index.html"
drupal = url + "core"
wordpress = url + "wp-login.php"
req = requests.get(asp)
req2 = requests.get(php)
req3 = requests.get(html)
req4 = requests.get(drupal)
req5 = requests.get(wordpress)

def allurl(url):
    req = requests.get(url)
    htmlcontent = req.content
    soup = BeautifulSoup(htmlcontent, "html.parser")
    achoor = soup.find_all("a")
    all_links = set()
    for link in achoor:
        if link.get('href') != '#':
            link_text = link.get('href')
            full_url = urljoin(url, link_text)
            all_links.add(full_url)
    unique_links = list(all_links)
    for good in unique_links:
        print(good)

def javascript(url):

    req = requests.get(url)
    htmlcontent = req.content
    soup = BeautifulSoup(htmlcontent, "html.parser")
    all_js_links = set()
    js_tags = soup.find_all("script")
    for tag in js_tags:
        src_attr = tag.get("src")
        if src_attr:
            full_url = urljoin(url, src_attr)
            all_js_links.add(full_url)
    unique_js_links = list(all_js_links)
    for link in unique_js_links:
        print(link)

def backend(url):
    # global req global req2 global req3 global req4 global req5
    if req.status_code == 200:
        print("Microsoft ASP detected")
    elif req3.status_code == 200:
        print("HTML detected")
    else:
        print("Unknown Backend. Do you want to search for CMS?")
        ask = input("Press Y for Yes and N for NO: ")
        ask = ask.upper()
        if ask == "N":
            exit()
        else:
            print("Searching for CMS...")
    if req2.status_code == 200:
        print("PHP detected")
        if req4.status_code == 403:
            print("Drupal Detected")
        elif req5.status_code == 200:
            print("WordPress Detected")
        else:
            print("Couldn't detect CMS")

def directorysearch():

    if req.status_code==200:
        print("Downloading ASPX wordlist")
        asppp = subprocess.run(['powershell.exe',
                                'wget https://raw.githubusercontent.com/orwagodfather/WordList/main/aspx.txt -outfile "aspx.txt"'],
                               capture_output=True, text=True)
        with open("aspx.txt", "r") as f:
            for line in f:
                allurl = (url + line)
                print(allurl, requests.get(allurl))
        os.remove("aspx.txt")


    elif req3.status_code==200:
        print("Downloading HTML wordlist")
        common = subprocess.run(['powershell.exe',
                                 'wget https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt -outfile "common.txt"'],
                                capture_output=True, text=True)
        with open("common.txt", "r") as f:
            for line in f:
                allurl = (url + line)
                print(allurl, requests.get(allurl))
        os.remove("common.txt")


    elif req4.status_code==200:
        print("Downloading Drupal wordlist")
        drupalll = subprocess.run(['powershell.exe',
                                   'wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/URLs/urls-Drupal-7.20.txt -outfile "drupal.txt"'],
                                  capture_output=True, text=True)
        with open("drupal.txt", "r") as f:
            for line in f:
                allurl = (url + line)
                print(allurl, requests.get(allurl))
        os.remove("drupal.txt")


    elif req5.status_code==200:
        print("Downloading wordpress wordlist")
        wordpresss = subprocess.run(['powershell.exe',
                                     'wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/CMS/wordpress.fuzz.txt -outfile "wordpress.txt"'],
                                    capture_output=True, text=True)
        with open("wordpress.txt", "r") as f:
            for line in f:
                allurl = (url + line)
                print(allurl, requests.get(allurl))
        os.remove("wordpress.txt")


    elif req2.status_code == 200:
        print("Downloading PHP Wordlist")
        phppp = subprocess.run(['powershell.exe',
                                'wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/Common-PHP-Filenames.txt -outfile "php.txt"'],
                               capture_output=True, text=True)
        with open("php.txt", "r") as f:
            for line in f:
                allurl = (url + line)
                print(allurl, requests.get(allurl))
        os.remove("php.txt")

def get_parameter():
    prompt = input(
        "If you want to search for parameters from a wordlist press W and if you want to search manually press X")
    prompt = prompt.upper()
    if prompt == "X":

        parameter = input("enter the name of the parameter")
        value = input("enter the value of parameter")
        emp = {parameter: value}
        query = urllib.parse.urlencode(emp)
        final = url + "?" + query
        response = requests.get(final)
        cont = (len(response.content))
        if response.status_code == 200:

            print(f"Content length of {final} is {cont}")
        else:
            print(f"Failed to get content length of {url}.")
    elif prompt == "W":
        wordlist_path = input("enter the path of the wordlist")
        value = input("enter the value of parameter")
        with open(wordlist_path, "r") as f:
            for words in f:
                words = words.strip()
                wholeurl = url + "?" + words + "=" + value
                response = requests.get(wholeurl)
                cont = (len(response.content))
                if response.status_code == 200:
                    print(f"Content length of {wholeurl} is {cont}")
                else:
                    print(f"Failed to get content length of {wholeurl}")

def notify_slack():
    with open('webhook_url.txt', 'r') as f:
        webhook_url = f.read().strip()

    os.system(
        r'''PowerShell -Command "Invoke-WebRequest -Uri '{0}' -Method POST -ContentType 'application/json' -Body '{{\"text\":\"Hello,Your task is completed\"}}' -UseBasicParsing" > NUL 2>&1"'''.format(
            webhook_url))


if url:
    print("[++]---Gathering The URL--[++]")
    allurl(url)
if js:
    print("[++]---Gathering the JS files--[++]")
    javascript(url)
if be:
    print("[++]--Detecting the Backend Technologies--[++]")
    backend(url)
if dsearch:
    print("[++]--Performing Directory Search--[++]")
    directorysearch()
if pfuzz:
    print("[++]--Fuzzing for Parameters--[++]")
    get_parameter()
if slack:
    print("[++]--You will be notified once the task is completed--[++]")
    notify_slack()