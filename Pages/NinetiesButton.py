from Base import *

class NinetiesButton(Base):

    def __init__(self, driver):
        self.driver = driver
        
    def Is(self):
        elems = self.driver.find_elements(By.CSS_SELECTOR, "#collapse-Model ul li")
        return len(elems) > 0
    
    def run(self):
        driver = self.driver

        super().closeAllPopups()

        # Find GR86 buttons"
        elems = self.driver.find_elements(By.CSS_SELECTOR, "#collapse-Model ul li")
        elems = [x for x in elems if "GR86" in x.text]

        if len(elems) != 1:
            # Find model dropdown
            elems = driver.find_elements(By.CSS_SELECTOR, "#filter-Model")
            
            if len(elems) != 1:
                log(f"Found {len(elems)} Model dropdowns", Fore.YELLOW)
                return False
            
            # Expand Model drop down
            log("Click Model dropdown", Fore.LIGHTBLACK_EX)
            elems[0].click()
            time.sleep(3)
            
            # Find all GR86 filter links
            elems = driver.find_elements(By.CSS_SELECTOR, "#collapse-Model ul li")
            elems = [x for x in elems if "GR86" in x.text]
        
            if len(elems) != 1:
                log(f"Found {len(elems)} GR86 buttons", Fore.YELLOW)
                return True

        # Click li element
        log(f"Click filter button: {elems[0].text}".replace("\n",""), Fore.LIGHTBLACK_EX)
        elems[0].click()
        time.sleep(3)

        # Find all car links
        elems = driver.find_elements(By.CSS_SELECTOR, "h2 a span")#.multi_widget h2 a
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