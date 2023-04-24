from Pages.Acceleride import *
from Pages.Butte import *
from Pages.Button import *
from Pages.Expando import *
from Pages.Kinsel import *
from Pages.Linky import *
from Pages.Meador import *
from Pages.NinetiesButton import *
from Pages.Simple import *
from Pages.Smartpath import *
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sys
from Log import log
import logging
from colorama import Fore
from colorama import Style
import colorama
import os
import json

import undetected_chromedriver.v2 as uc

def Analyze(driver, url):
    try:
        url = url.rstrip('\n')

        log("╔" + "═" * len(url) + "╗", Fore.MAGENTA)
        log(f"║{url}║", Fore.MAGENTA)
        log("╚" + "═" * len(url) + "╝", Fore.MAGENTA)

        # Get page here so it doesn't load twice
        driver.get(url)
        WebDriverWait(driver, 10).until(
            lambda wd: driver.execute_script("return document.readyState") == "complete",
            "Page took too long to load"
        )
        log(f"Sleep 7s", Fore.LIGHTBLACK_EX)
        time.sleep(7)

        found = None

        for c in (Acceleride, Butte, Button, Expando, Kinsel, Linky, Meador, NinetiesButton, Simple, Smartpath):
            c = c(driver)
            if (c.Is()):
                log(c.__class__.__name__, Fore.WHITE)
                found = c.run()
                break

        if (found is None):
            log("Could not match to class", Fore.RED)
            input()
        elif (found is False):
            log(".run() returned False", Fore.RED)
            input()

    except Exception as e:
        #raise e
        log(str(type(e)) + " - " + str(e), Fore.RED)
        input()


colorama.init()

options = uc.ChromeOptions()
options.add_argument("--mute-audio")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#driver = uc.Chrome(options)
#driver = uc.Chrome(chrome_options=options,use_subprocess=True)
#driver.implicitly_wait(1)
#driver.get("https://nowsecure.nl/")
#input()

#urls = ["https://www.roundrocktoyota.com/new-inventory/index.htm"]

#opts = Options()
#opts.add_argument('--no-sandbox')
#opts.add_argument("load-extension=C:/Users/Jon/AppData/Local/Microsoft/Edge Dev/User Data/Default/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.43.0_0")
#opts.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36")
#opts.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
#opts.add_experimental_option('useAutomationExtension', False)
#opts.binary_location = "C:/Program Files (x86)/Microsoft/Edge Dev/Application/msedge.exe"
#opts.add_argument('--disable-blink-features=AutomationControlled')

#driver = webdriver.Edge(options=opts)
#driver = uc.Chrome()

#driver.get("https://nowsecure.nl/")
#input()

#driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#  "source": """
#    Object.defineProperty(navigator, 'webdriver', {
#      get: () => undefined
#    })
#  """
#})
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'})
if (len(sys.argv) > 1):
    Analyze(uc.Chrome(chrome_options=options,use_subprocess=True), sys.argv[1])
    exit()

progress = ""
progressFile = os.path.join(os.path.dirname(__file__), "progress.txt")
if os.path.isfile(progressFile):
    file = open(progressFile, mode='r')
    progress = file.read()
    file.close()

driver = uc.Chrome(chrome_options=options,use_subprocess=True)

dealersDir = os.path.join(os.path.dirname(__file__), "dealers")
for filename in os.listdir(dealersDir):
    if filename.endswith(".txt"):
        log(filename, Fore.YELLOW)
        filename = os.path.join(dealersDir, filename)
        with open(filename) as file:
            for url in file:
                if not url.startswith("#"):
                    if url in progress:
                        log(f"Skip {url}", Fore.LIGHTBLACK_EX)
                    else:
                        #driver = uc.Chrome(chrome_options=options,use_subprocess=True)
                        #driver.minimize_window()
                        Analyze(driver, url)
                        #driver.close()
                        pFile = open(progressFile, "a")
                        pFile.write(f"{url}")
                        pFile.close()

os.remove(progressFile)
