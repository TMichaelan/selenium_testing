import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import random
import sqlite3
from faker import Faker

def setup_db():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS logs 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            event TEXT, 
            loading_time FLOAT, 
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def log_event(event, loading_time):
    conn = sqlite3.connect('logs.db')  
    c = conn.cursor()
    c.execute("INSERT INTO logs (event, loading_time) VALUES (?, ?)", (event, loading_time))
    conn.commit()
    conn.close()

def check_element_has_class(driver, xpath, classname):
    element = driver.find_element(By.XPATH, xpath)
    return classname in element.get_attribute("class")

def login_to_erp():
    global login
    global password

    try:
        driver.find_element(By.XPATH, '//*[@id="inputEmail1"]').send_keys(login)
        driver.find_element(By.XPATH, '//*[@id="inputPassword1"]').send_keys(password)
        driver.find_element(By.XPATH, '/html/body/app-root/app-login/div/form/button').click()
    except Exception as e:
        print("ERROR" + e)
        login_to_erp()

def cancel_reservation(reservation_number):
    erp_url = f"https://dev.erp.oskar.com.pl/reservation/{reservation_number}"
    driver.get(erp_url)
    time.sleep(1)
    start_time = time.time()
    login_to_erp()
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to login to erp: {round(loading_time,3)}s")
    log_event("login_erp", loading_time)
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "//*[@id=\"mat-tab-content-0-0\"]/div/app-reservation-summary/div/div/div[2]/app-reservation-summary-status/mat-card/mat-card-content/button").click()
        driver.find_element(By.XPATH, "//*[@id=\"mat-menu-panel-2\"]/div/button[3]").click()
        driver.find_element(By.XPATH, "//*[@id=\"mat-input-1\"]").send_keys(0)
        driver.find_element(By.XPATH, "//html/body/div[2]/div[2]/div/mat-dialog-container/app-reservation-summary-cancel-dialog/mat-dialog-content/mat-form-field[2]/div/div[1]/div[3]/mat-select/div").click()
        driver.find_element(By.XPATH, "//*[@id=\"mat-option-2\"]").click()
        driver.find_element(By.XPATH, "//html/body/div[2]/div[2]/div/mat-dialog-container/app-reservation-summary-cancel-dialog/mat-dialog-actions/button[1]").click()
        start_time = time.time()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//html/body/app-root/app-infobox/div/div/div/div[1]")))
        end_time = time.time()
        loading_time = end_time - start_time
        print(f"Time taken to cancel reservation: {round(loading_time,3)}s")
        log_event("cancel_reservation", loading_time)
    except Exception as e:
        print("ERROR" + e)
        return cancel_reservation(reservation_number)

def find_offers(offer_number):
    find_offers_button = driver.find_element(By.CSS_SELECTOR,".hover\:bg-accentColorDarker")
    find_offers_button.click()

    start_time = time.time()
    find_offers_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//html/body/app-root/app-offer-list/div[2]/div[{offer_number}]/app-offer-list-box/div/div[2]/div[2]/div/a")))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load all offers: {round(loading_time,3)}s")
    log_event("load_all_offers", loading_time)


def load_offer():
    start_time = time.time()
    driver.find_element(By.CSS_SELECTOR,"body > app-root > app-offer-list > div.pt-\[150px\].lg\:pt-0.max-w-\[1300px\].mx-auto.ng-star-inserted > div:nth-child(3) > app-offer-list-box > div > div.w-full.flex.flex-row.justify-between.items-stretch.p-5.px-10.border-\[1px\].border-mainColor.rounded-\[60px\] > div:nth-child(2) > div > a").click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"configurator\"]/div[2]/div/div/div/div/div/div[1]/app-offer-form-term/div/app-offer-default-form/div[1]/div")))
    WebDriverWait(driver, 20).until(lambda driver: check_element_has_class(driver, "//*[@id=\"configurator\"]/div[3]/div[2]/button", "bg-mainYellow"))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load offer: {round(loading_time,3)}s")
    log_event("load_offer", loading_time)

def book_offer():
    time.sleep(1)
    book_offer = driver.find_element(By.XPATH,"//div[2]/button")
    book_offer.click()

    fake = Faker()
    reservation_data = {
        'email': fake.email(),
        'sex': random.choice(['Mężczyzna', 'Kobieta']),
        'firstName': fake.first_name(),
        'lastName': fake.last_name(),
        'phoneNumber': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
        'birth': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d.%m.%Y'),
        # 'invoice': random.choice([True, False])
        'invoice': False
    }
    reservation_form = driver.find_element(By.XPATH, "//html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-owner/div/div[1]")
    reservation_form.click()

    driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="email"]').send_keys(reservation_data['email'])
    driver.execute_script("window.scrollBy(0, 400);")
    Select(driver.find_element(By.CSS_SELECTOR, 'select[formcontrolname="sex"]')).select_by_visible_text(reservation_data['sex'])
    driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="firstName"]').send_keys(reservation_data['firstName'])
    driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="lastName"]').send_keys(reservation_data['lastName'])
    driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="phoneNumber"]').send_keys(reservation_data['phoneNumber'])
    driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="birth"]').send_keys(reservation_data['birth'])
    driver.execute_script("window.scrollBy(0, 400);")
    driver.find_element(By.XPATH, '//div[2]/div/div[2]/div/div[2]').click()


    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-resignation/div/div[1]").click()
    driver.execute_script("window.scrollBy(0, 400);")
    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-resignation/div/div[2]/div/div[1]/div[2]/label/input").click()

    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-consents/div/div[1]").click()
    driver.execute_script("window.scrollBy(0, 1000);")

    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-consents/div/div[2]/div/label[1]/input").click()
    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-consents/div/div[2]/div/label[2]/input").click()
    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-consents/div/div[2]/div/label[3]/input").click()
    driver.find_element(By.XPATH, "/html/body/app-root/app-reservation-form/div[2]/div/div[2]/app-reservation-form-consents/div/div[2]/div/label[4]/input").click()

    time.sleep(2)
    make_reservation_button = driver.find_element(By.CSS_SELECTOR, "body > app-root > app-reservation-form > div.w-full.mx-auto.pt-20.relative.bg-\[\#f0f0f0\] > div > div.fixed.bottom-0.left-0.right-0.bg-accentColor.z-10 > div > app-button > button")
    start_time = time.time()
    make_reservation_button.click()

    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//html/body/app-root/app-reservation-form-summary/div[1]")))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//html/body/app-root/app-reservation-form-summary/div/div/div[7]/div[2]/div/div[2]/app-button/button")))
    element = driver.find_element(By.TAG_NAME,'h1')
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load reservation: {round(loading_time,3)}s")
    log_event("load_reservation", loading_time)

    reservation_info = element.text.split()
    reservation_number = reservation_info[-1]

    return reservation_number
    

def load_page(url):
    start_time = time.time()
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".swiper-slide:nth-child(1) > .flex .text-mainColor:nth-child(2)")))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load {url}: {round(loading_time,3)}s")
    log_event("load_page", loading_time)

def pay_for_reservation():
    driver.find_element(By.XPATH, "//html/body/app-root/app-reservation-form-summary/div/div/div[7]/div[2]/div/div[2]/app-button/button").click()
    start_time = time.time()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"app\"]/div/div[2]/main/div[2]/article/div/div/a[1]")))
    driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/main/div[2]/article/div/div/a[1]").click()
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load PayU: {round(loading_time,3)}s")
    log_event("load_payu", loading_time)

    driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/main/div[2]/article/div/div/ul/li[1]/div").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[@id=\"form-email\"]").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//html/body/div[4]/div/div/button").click()

    start_time = time.time()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#formSubmit")))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load PayU Auth: {round(loading_time,3)}s")
    log_event("load_payu_auth", loading_time)
    driver.find_element(By.CSS_SELECTOR, "#formSubmit").click()
    start_time = time.time()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#formSubmit")))
    end_time = time.time()
    loading_time = end_time - start_time
    print(f"Time taken to load PayU Payment Status: {round(loading_time,3)}s")
    log_event("load_payu_payment_status", loading_time)
    driver.find_element(By.CSS_SELECTOR, "#formSubmit").click()
    
def start():
    offer_number = random.randint(2,12)
    try:
        load_page(url)
        find_offers(offer_number)
        load_offer()
        reservation_number = book_offer()
        pay_for_reservation()
        cancel_reservation(reservation_number)
    except Exception as e:
        print("ERROR" + e)
        start()

if __name__ == "__main__":
    url = ""
    login = ""
    password = ""

    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)

    setup_db()
    start()

    time.sleep(1)
    driver.quit()
