import os
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium.webdriver.common.action_chains import ActionChains


def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))


def type_like_human(field, text):
    for char in text:
        field.send_keys(char)
        random_delay(0.1, 0.3)


def human_like_click(element):
    random_delay(0.5, 2)
    ActionChains(driver).move_to_element(element).click().perform()
    random_delay(0.5, 1)


def login():
    try:
        # Wait for the email field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        type_like_human(email_field, username)
        random_delay(1, 2)

        # Wait for the password field
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        type_like_human(password_field, password)
        random_delay(1, 2)

        # Click login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        )
        human_like_click(login_button)

    except Exception as e:
        print(e)
        driver.quit()


def handle_modal():
    try:
        # Wait for the modal to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root"))
        )
        random_delay(1, 2)

        # Locate and click the Dismiss button
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Dismiss')]")))
        human_like_click(dismiss_button)

    except Exception as e:
        print("No modal found or other error:", e)


def sell_on_pos():
    try:
        pos_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Point Of Sale')]"))
        )
        pos_button.click()
        # Wait for the items to load (i.e., the 'Add' buttons to appear)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.MuiIconButton-root"))
        )
        add_random_items_to_cart()
        checkout()
    except Exception as e:
        driver.save_screenshot('screenshot_pos.png')  # Saves a screenshot to verify the window size
        print(e)
        driver.quit()


def checkout():
    try:
        # Wait for the checkout button to appear and click it
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue to Payment')]"))
        )
        checkout_button.click()

        # Select the 'CASH' payment method using JavaScript click
        cash_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'CASH')]"))
        )
        driver.execute_script("arguments[0].click();", cash_option)

        # Confirm the selection
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        # Wait for the modal to update and close button to appear
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[1]/div[2]/button"))
            # Adjust the selector
        )
        close_button.click()

    except Exception as e:
        print("Error during checkout:", e)


def add_random_items_to_cart():
    try:
        # Find all SVGs
        svg_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.MuiIconButton-root svg[data-testid='AddIcon']")
            )
        )

        # Select and click buttons
        add_buttons = [driver.execute_script("return arguments[0].parentNode;", svg) for svg in svg_elements]
        if len(add_buttons) >= 3:
            selected_buttons = random.sample(add_buttons, 3)
            for button in selected_buttons:
                human_like_click(button)
                random_delay(0.5, 1.5)

    except Exception as e:
        print("Error adding items to cart:", e)

def selectprofile(username):
    # Use an absolute path for the profile directory, e.g., '/home/user/profiles' or 'C:\\profiles'
    base_profile_dir = os.path.abspath('./profiles')
    print(f"Base Profile Directory: {base_profile_dir}")

    # Create the base directory if it doesn't exist
    if not os.path.exists(base_profile_dir):
        os.makedirs(base_profile_dir)
        print(f"Created base directory at {base_profile_dir}")

    # Complete path for the new profile
    profile_path = os.path.join(base_profile_dir, username)
    print(f"Profile Path: {profile_path}")

    # Check if the profile directory exists
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
        print(f"Created profile directory at {profile_path}")

    # Set up Chrome options to use the new profile
    chrome_options = Options()

    # Define minimum size and generate random dimensions
    min_width, min_height = 1200, 1200
    random_width = random.randint(min_width, min_width + 200)
    random_height = random.randint(min_height, min_height + 600)

    # Set the window size
    chrome_options.add_argument(f"--window-size={random_width},{random_height}")
    chrome_options.add_argument("--headless")

    return chrome_options


if __name__ == "__main__":
    url = "https://jng-fnd2-zpqy7.ondigitalocean.app"
    username = "lilostitchhh6@gmail.com"
    password = "12345678"
    chrome_option = selectprofile(username)
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(url)
    login()
    handle_modal()
    sell_on_pos()
    driver.quit()
