from Base import *
# https://www.odessatoyota.com/inventory?type=new&make=Toyota

class Simple(Base):

    def __init__(self, driver):
        self.driver = driver
    
    def Is(self):
        elems = self.driver.find_elements(By.CSS_SELECTOR, "li.clearfix")
        if len(elems) > 0:
            return True
    
    def run(self):
        driver = self.driver
        
        # Expand model dropdown
        elems = driver.find_elements(By.CSS_SELECTOR, "#filter-model .maxlist-more a") 
        if len(elems) > 0:
            log("Click View More models", Fore.LIGHTBLACK_EX)
            elems[0].click()
            time.sleep(1)

        # Find all GR86 filter links
        elems = driver.find_elements(By.CSS_SELECTOR, "li.clearfix")
        elems = [x for x in elems if "GR86" in x.text]

        # Exit if no filter links
        if len(elems) < 1:
            log("No GR86 filter links found", Fore.YELLOW)
            return True

        # Click li element
        log(f"Click filter option: {elems[0].text}".replace("\n",""), Fore.LIGHTBLACK_EX)
        elems[0].click()
        time.sleep(3)

        # Find all car links
        elems = driver.find_elements(By.CSS_SELECTOR, ".srp-vehicle-title")
        elems = [x for x in elems if "GR86" in x.text]

        if len(elems) < 1:
            log("No car links found", Fore.RED)
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
                elems = driver.find_elements(By.CSS_SELECTOR, ".srp-vehicle-title")
                elems = [x for x in elems if "GR86" in x.text]
            
        return True
            