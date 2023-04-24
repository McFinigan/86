from Base import *

class Smartpath(Base):

    def __init__(self, driver):
        self.driver = driver
        
    def Is(self):
        elems = self.driver.find_elements(By.CSS_SELECTOR, "app-card-container")
        return len(elems) > 0
    
    def run(self):
        driver = self.driver

        super().closeAllPopups()

        # Find all GR86 filter links
        elems = driver.find_elements(By.CSS_SELECTOR, ".vehicle-name")
        elems = [x for x in elems if "GR86" in x.text]
        
        if len(elems) != 1:
            log(f"Found {len(elems)} GR86 cards", Fore.YELLOW)
            return True

        # Click filter link
        log(f"Click filter card: {elems[0].text}".replace("\n",""), Fore.LIGHTBLACK_EX)
        super().navigateToPage(elems[0])
        time.sleep(3)

        # Check for contact us popup, if there then no cars
        elems = driver.find_elements(By.CSS_SELECTOR, ".contactDealer-close-button")
        if len(elems) > 0:
            log("No cars in stock", Fore.YELLOW)
            return True

        # Find all car links
        elems = driver.find_elements(By.CSS_SELECTOR, "app-card-container ng-component.ng-star-inserted div.vehicle-card.ng-star-inserted")

        if len(elems) < 1:
            log("No car link cards found", Fore.YELLOW)
            return False

        i = 0
        
        while i < len(elems):
            driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", elems[i])

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
                elems = driver.find_elements(By.CSS_SELECTOR, "app-card-container ng-component.ng-star-inserted div.vehicle-card.ng-star-inserted")
            
        return True