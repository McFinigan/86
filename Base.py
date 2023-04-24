from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support import expected_conditions as EC
from contextlib import contextmanager
import time
import re
from Log import *

detailsSelectors = [
    "li .columns",
    "li.vdp-info",
    ".details-overview_data",
    ".ws-quick-spec",
    ".basic-info-item",
    ".vehicle-info .callout ul li",
    "#quick-specs1-app-root",
    ".basic-info-wrapper",
    ".vdp-vehicle-details",
    ".mid-section",
    "table.fields",
    ".top-0 div.mt-3", # Acceleride
    "vdp-vehicle-info", # Smartpath
    ".bottom-block__item--info" # Kinsel
]

titleSelectors = [
    ".vehicle-title h1",
    ".vdp-vehicle-title h1",
    "h1.vehicle-title",
    ".vehicle_title.fl_l",
    ".vdp-title__vehicle-info",
    "h1.main-car-title",
    ".widget-paragraph h2 strong",
    ".hidden h1", # Acceleride
    "div.vehicle-title", # Smartpath and Kinsel
]

popupSelector = [
    ["button.ml-auto.text-link", "personalize"],
    ["button[aria-label=\"Accept and Continue ➞\"]", "privacy banner"],
    ["button.close[aria-label=\"Close\"]", "fullscreen \"The One\""],
    [".cnpk5__x[aria-label=\"Close\"]", "chat pop-up"],
    ["#dg-mstc-component-modal-close", "smart path"],
    ["a.ui-dialog-titlebar-close", "center screen"],
    ["#cq1-hard-close", "KBB"],
    #[".contactDealer-close-button", "Smartpath Contact Us"],
    ["button.ca-primary-button, button.consumer-privacy-banner-button", "privacy banner"],
]

deleteSelector = [
    [".gg-toolbar", "gg-toolbar"],
    [".gg-chat-wrapper", "gg-chat-wrapper"],
    [".consumer-privacy-banner", "bottom left blue guy icon"]
]

class Base:
    def __init__(self, driver):
        self.driver = driver
        
    def run(self):
        self.closeAllPopups()

    # Closes a pop-up
    def closePopup(self, selector, name="unspecified"):
        # Check for pop-up
        try:
            element = WebDriverWait(self.driver, .501).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except TimeoutException as e:
            return

        log(f"Close {name} pop-up", Fore.LIGHTBLACK_EX)
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            ).click()

            time.sleep(1)
        except (ElementClickInterceptedException, ElementNotInteractableException, TimeoutException) as e:
            log(f"{type(e)} - {selector} {name} element is not clickable", Fore.LIGHTBLACK_EX)

    @contextmanager
    def wait_for_page_load(self, selector, timeout=10):
        old_element = self.driver.find_element(By.CSS_SELECTOR, selector)
        yield
        WebDriverWait(self.driver, timeout).until(
            staleness_of(old_element)
        )

    def deleteElement(self, selector, name="unspecified"):
        elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
        
        if len(elems) > 0:
            self.driver.execute_script(f"""
            var l = document.querySelectorAll("{selector}")[0];
            l.parentNode.removeChild(l);
            """)

    def closeAllPopups(self):
        try:
            while(True):
                alert = self.driver.switch_to.alert
                log("Dismiss alert", Fore.LIGHTBLACK_EX)
                alert.dismiss()
        except(NoAlertPresentException):
            pass

        for i in range(len(deleteSelector)):
            self.deleteElement(deleteSelector[i][0], deleteSelector[i][1])

        for i in range(len(popupSelector)):
            self.closePopup(popupSelector[i][0], popupSelector[i][1])

        # Close "didn't find the one" overlay
        findFrame = self.driver.find_elements(By.CSS_SELECTOR, "iframe#pw_frame_c2f53853-c592-4a2b-9145-7f463217537c")
        if len(findFrame) > 0:
            log("Found \"Didn't find\" iframe", Fore.LIGHTBLACK_EX)

            findBtn = self.driver.switch_to.frame(findFrame[0])

            # Close "didn't find the one" overlay
            findBtn = self.driver.find_elements(By.CSS_SELECTOR, "a.msg-btn-no")

            if len(findBtn) > 0:
                log("Close \"Didn't find\" pop-up", Fore.LIGHTBLACK_EX)
                findBtn[0].click()
                #time.sleep(2)

    def navigateToPage(self, elem):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)

        try:
            elem.click()
        except WebDriverException:
            log("click() threw WebDriverException", Fore.YELLOW)
            #time.sleep(1)
            try:
                elem.click()
            except StaleElementReferenceException:
                log("StaleElementReferenceException - Continuing", Fore.YELLOW)


    def getDetails(self):
        for selector in detailsSelectors:
            detailsElems = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if len(detailsElems) > 0:
                return detailsElems

        log("Could not find detailsElems", Fore.RED)
        input()
        return None
    
    def getTitle(self):
        for selector in titleSelectors:
            titleElems = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if len(titleElems) > 0:
                return titleElems

        log("Could not find titleElems", Fore.RED)
        input()
        return None
    
    def detectTrans(self):
        transElems = [x for x in self.getDetails() if re.search("[Mm]anual", x.text)]
        if len(transElems) > 0:
            log("Found transmission", Fore.CYAN)
            return True

        transElems = [x for x in self.getDetails() if re.search("[Aa]utomatic", x.text)]
        if len(transElems) > 0:
            return False

        transElems = [x for x in self.getDetails() if re.search("6MT", x.text)]
        if len(transElems) > 0:
            return True

        transElems = [x for x in self.getDetails() if re.search("6AT", x.text)]
        if len(transElems) > 0:
            return False

        log("Could not find transmission", Fore.RED)
        return None
                
    def detectColor(self):
        colorElems = [x for x in self.getDetails() if re.search("[Hh]alo", x.text)]
        
        if len(colorElems) > 0:
            log("Found color", Fore.CYAN)

        return len(colorElems) > 0
        
    def detectTrim(self):
        # Check for Premium in details
        trimElems = [x for x in self.getDetails() if re.search("[Pp][Rr][Ee][Mm][Ii][Uu][Mm]", x.text)]
        if len(trimElems) > 0:
            log("Found trim", Fore.CYAN)
            return True

        # Check for Base in details
        trimElems = [x for x in self.getDetails() if re.search("[Bb][Aa][Ss][Ee]", x.text)]
        if len(trimElems) > 0:
            return False

        # Check for Anniversary in details
        trimElems = [x for x in self.getDetails() if re.search("[Aa][Nn][Nn][Ii][Vv][Ee][Rr][Ss][Aa][Rr][Yy]", x.text)]
        if len(trimElems) > 0:
            return False

        # Check for Premium in title
        trimElems = self.getTitle()
        trimElems = [x for x in trimElems if re.search("[Pp][Rr][Ee][Mm][Ii][Uu][Mm]", x.text)]
        if len(trimElems) > 0:
            log("Found trim", Fore.CYAN)
            return True

        # Check for Base in title
        trimElems = self.getTitle()
        trimElems = [x for x in trimElems if re.search("[Bb][Aa][Ss][Ee]", x.text)]
        if len(trimElems) > 0:
            return False

        # Check for STD in title
        trimElems = self.getTitle()
        trimElems = [x for x in trimElems if re.search("STD", x.text)]
        if len(trimElems) > 0:
            return False

        # Check for Anniversary in title
        trimElems = self.getTitle()
        trimElems = [x for x in trimElems if re.search("[Aa][Nn][Nn][Ii][Vv][Ee][Rr][Ss][Aa][Rr][Yy]", x.text)]
        if len(trimElems) > 0:
            return False

        log("Could not find trim", Fore.RED)
        return None


    def checkStats(self):
        trans = self.detectTrans()
        color = self.detectColor()
        trim = self.detectTrim()

        if not any(e == False for e in [trans, color, trim]):
            input()

    def scrollToBottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollBy(0,250)")

            # Wait to load page
            time.sleep(.5)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
