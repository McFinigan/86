from Base import *

class Linky(Base):

    def __init__(self, driver):
        super().__init__(driver)
    
    def Is(self):
        isSelectors = ["li.filter_option", "li.checkbox.mb-lg-4", ".ddc-icon.icon-style-collapse.ddc-icon-expand"]

        for selector in isSelectors:
            elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elems) > 0:
                return True
        
        return False
    
    def run(self):
        driver = self.driver
        
        super().run()

        # Find all GR86 filter links
        elems = driver.find_elements(By.CSS_SELECTOR, "li.filter_option")
        elems = [x for x in elems if "GR86" in x.text]

        # Check for other kind of filter link
        if len(elems) < 1:
            elems = self.driver.find_elements(By.CSS_SELECTOR, "li.checkbox.mb-lg-4")
            elems = [x for x in elems if "GR86" in x.text]
            if len(elems) < 1:
                # Expand Model with nice red button
                elems = driver.find_elements(By.CSS_SELECTOR, "a.collapsed")
                elems = [x for x in elems if "Model" in x.text]

                if len(elems) > 0:
                    log(f"Expand model section with red button", Fore.LIGHTBLACK_EX)
                    try:
                        elems[0].click()
                    except ElementClickInterceptedException:
                        log(f"Element is not clickable", Fore.LIGHTBLACK_EX)

                # Expand Model with basic black button
                elems = driver.find_elements(By.CSS_SELECTOR, ".group.thm-general_border")
                elems = [x for x in elems if "Model" in x.text]

                if len(elems) > 0:
                    log(f"Expand model section with basic button", Fore.LIGHTBLACK_EX)
                    try:
                        elems[0].click()
                    except ElementClickInterceptedException:
                        log(f"Element is not clickable", Fore.LIGHTBLACK_EX)

        # Find all GR86 filter links
        elems = driver.find_elements(By.CSS_SELECTOR, "li.filter_option")
        elems = [x for x in elems if "GR86" in x.text]

        # Exit if no filter links
        if len(elems) < 1:
            elems = self.driver.find_elements(By.CSS_SELECTOR, "li.checkbox.mb-lg-4")
            elems = [x for x in elems if "GR86" in x.text]
            if len(elems) < 1:
                log("No GR86 filter links found", Fore.YELLOW)
                return True

        # Click GR86 filter link
        log(f"Click filter option: {elems[0].text}".replace("\n",""), Fore.LIGHTBLACK_EX)
        with super().wait_for_page_load("h2 a"):
            elems[0].click()

        # Scroll to bottom of page
        super().scrollToBottom()

        # Find all car links
        elems = driver.find_elements(By.CSS_SELECTOR, "h2 a")
        elems = [x for x in elems if "GR86" in x.text]

        if len(elems) < 1:
            log("No car links found", Fore.RED)
            return False

        i = 0
        
        while i < len(elems):
            log(f"Sleep 2s", Fore.LIGHTBLACK_EX)
            time.sleep(2)
            super().closeAllPopups()

            log(f"({str(i+1)} of {str(len(elems))}) Navigate to car page: {elems[i].text}", Fore.WHITE)
            super().navigateToPage(elems[i])

            super().checkStats()
        
            i += 1
        
            if i < len(elems):
                # Go back
                driver.execute_script("window.history.go(-1)")
                time.sleep(5)

                # Scroll to bottom of page
                super().scrollToBottom()
                    
                elems = driver.find_elements(By.CSS_SELECTOR, "h2 a")
                elems = [x for x in elems if "GR86" in x.text]
            
        return True
            