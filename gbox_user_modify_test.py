import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

def load_page(url):
    start_time = time.time()
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#loginFields")))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load login page: {round(loading_time,3)}s")
    # log_event("load_page", loading_time)

def login_to_gbox(company, username, password):
    driver.find_element(By.CSS_SELECTOR, '#company').send_keys(company)
    driver.find_element(By.CSS_SELECTOR, '#username').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '#password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    start_time = time.time()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#more-menu > div:nth-child(1) > div:nth-child(1)")))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load login: {round(loading_time,3)}s")
    # log_event("load_page", loading_time)

def load_users(url):
    start_time = time.time()
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.nav-item:nth-child(4) > a:nth-child(1)")))
    driver.find_element(By.CSS_SELECTOR, "li.nav-item:nth-child(4) > a:nth-child(1)").click()
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load users page: {round(loading_time,3)}s")
    time.sleep(2)
    driver.find_element(By.XPATH, '//html/body/div[2]').click()
    # log_event("load_page", loading_time)



def modify_user(user_id):

    url = f"https://online.gbox.pl/settings/users/edit/{user_id}"
    driver.get(url)
    time.sleep(2)
    try:
        start_time = time.time()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//iframe'))
        )

        end_time = time.time()
        loading_time = end_time - start_time
        print(f"Time taken to load user's iframe: {round(loading_time,3)}s")

        iframe = driver.find_element(By.XPATH, '//iframe')
        driver.switch_to.frame(iframe)

        
        submit_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[8]/form/div/div[1]/fieldset/div[3]/a[1]'))
        )
        driver.find_element(By.XPATH, '//html/body/div[8]/form/div/div[2]/fieldset[2]/div[2]/div[1]/div/a').click()

        checkboxes = driver.find_elements(By.XPATH, '//*[@id="formik"]/div/div[2]/fieldset[1]/div/table//input[@type="checkbox"]')
        for i in range(30):
            checkbox = random.choice(checkboxes)
            checkbox.click()
            time.sleep(0.2)
            
        start_time = time.time()
        submit_button.click()
    except:
        print("Element not found")
    finally:
        driver.switch_to.default_content()

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.nav-item:nth-child(4) > a:nth-child(1)")))
        end_time = time.time()
        loading_time = end_time - start_time
        print(f"Time taken to load modify user: {round(loading_time,3)}s")

def start():
    load_page(url)
    login_to_gbox(company, username, password)
    load_users(url)
    modify_user("")

if __name__ == "__main__":
    url = ""
    company = ""
    username = ""
    password = ""

    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)

    start()

    time.sleep(2)
    driver.quit()
