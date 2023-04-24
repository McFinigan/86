from Base import *

class Button(Base):

    def __init__(self, driver):
        self.driver = driver
        
    def Is(self):
        elems = self.driver.find_elements(By.CSS_SELECTOR, "[data-facettype~=\"model\"]")
        return len(elems) > 0
    
    def run(self):
        driver = self.driver

        super().closeAllPopups()
        super().closeAllPopups()

        # Find model button
        elems = driver.find_elements(By.CSS_SELECTOR, "[data-facettype~=\"model\"]")
        elems = [x for x in elems if "Model" in x.text]
        
        if len(elems) != 1:
            log(f"Found {len(elems)} Model buttons", Fore.YELLOW)
            return False
        
        log("Click Model button", Fore.LIGHTBLACK_EX)
        elems[0].click()
        time.sleep(3)
        
        # Find all GR86 filter links
        elems = driver.find_elements(By.CSS_SELECTOR, "a[data-facet~=\"model\"]")
        elems = [x for x in elems if "GR86" in x.text]
        
        if len(elems) != 1:
            log(f"Found {len(elems)} GR86 buttons", Fore.YELLOW)
            return True

        # Click li element
        log(f"Click filter button: {elems[0].text}".replace("\n",""), Fore.LIGHTBLACK_EX)
        elems[0].click()
        time.sleep(3)

        super().closeAllPopups()

        # Find View Results link
        elems = driver.find_elements(By.CSS_SELECTOR, "a#facets-container-close")
        elems = [x for x in elems if "View" in x.text]
        
        if len(elems) != 1:
            log(f"Found {len(elems)} \"View Results\" links", Fore.RED)
            return False

        # Click li element
        log(f"Click View Results button", Fore.LIGHTBLACK_EX)
        elems[0].click()
        time.sleep(3)

        # Find all car links
        elems = driver.find_elements(By.CSS_SELECTOR, "h2 span")
        elems = [x for x in elems if "GR86" in x.text]

        if len(elems) < 1:
            log("No car links found", Fore.YELLOW)
            return False

        i = 0
        
        while i < len(elems):
            log(f"({str(i+1)} of {str(len(elems))}) Navigate to car page: {elems[i].text}", Fore.WHITE)
            
            try:
                elems[i].click()
            except WebDriverException:
                log("click() threw WebDriverException", Fore.YELLOW)
                time.sleep(1)
                try:
                    elems[i].click()
                except StaleElementReferenceException:
                    log("StaleElementReferenceException - Continuing", Fore.YELLOW)
                
            time.sleep(3)

            super().checkStats()
            
            i += 1
            
            if i < len(elems):
                time.sleep(3)
                driver.execute_script("window.history.go(-1)")
                time.sleep(5)
                elems = driver.find_elements(By.CSS_SELECTOR, "h2 span")
                elems = [x for x in elems if "GR86" in x.text]
            
        return True