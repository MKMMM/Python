from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/search/")
wait = WebDriverWait(driver, 10)

time.sleep (1)
elem = driver.find_element_by_css_selector("#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > form > div.lssxud > div > button")
elem.click()
time.sleep (5)

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#searchboxinput"))).send_keys("motels in new jersey")
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#searchbox-searchbutton"))).click()
time.sleep (5)

while True:
    try:
        for count, item in enumerate(wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[class='section-result'] h3[class='section-result-title']")))):
            refreshList = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[class='section-result'] h3[class='section-result-title']")))
            # click on each of the results
            refreshList[count].click()
            # the script now in inner page to parse the title
            name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.section-hero-header-title-title"))).text
            print(name)
            # click on the "Back to results" link located on the top left to get back to the results page
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[class^='section-back-to-list-button']"))).click()
            # wait for the spinner to be invisible
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#searchbox[class*='loading']")))
            # tried to get rid of staleness condition
            wait.until(EC.staleness_of(refreshList[count]))
    except Exception:
        break