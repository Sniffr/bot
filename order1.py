import random
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def selectprofile():
    chrome_options = Options()
    min_width, min_height = 1600, 720
    max_width, max_height = 1920, 1440
    random_width = random.randint(min_width, max_width)
    random_height = random.randint(min_height, max_height)
    chrome_options.add_argument(f"--window-size={random_width},{random_height}")
    print(f"Window size: {random_width}x{random_height}")
    return chrome_options

if __name__ == '__main__':
    chrome_option = selectprofile()
    driver = webdriver.Chrome(options=chrome_option)
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    driver.get("https://business.jungopharm.com")

    # Wait for username field to be visible
    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    username.send_keys("miriam@yahoo.com")

    # Wait for password field to be visible
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password.send_keys("12345678")

    # Wait for login button to be clickable
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "kc-login")))
    login_button.click()

    # Wait for the element to be visible before moving the mouse over it
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiBox-root:nth-child(5) .MuiButtonBase-root")))
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

    # Wait for "Order Products" to be clickable
    order_products = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBox-root:nth-child(4) .MuiBox-root")))
    order_products.click()

    # Wait for "Belea" to be clickable
    # Wait for "Belea" to be clickable
    belea = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBox-root:nth-child(4) .MuiGrid-root:nth-child(4) img")))

    # Add a small random delay
    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {'bubbles': true, 'cancelable': true}));",
                          belea)

    # Wait for the SVG icon to be clickable
    svg_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiGrid-root:nth-child(2) .MuiStack-root .MuiSvgIcon-root")))
    svg_icon.click()

    # Mouse over and out actions
    actions.move_to_element(svg_icon).perform()
    body = driver.find_element(By.CSS_SELECTOR, "body")
    actions.move_to_element(body, 0, 0).perform()

    # Don't forget to close the browser when you're done
    driver.quit()