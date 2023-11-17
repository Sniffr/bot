import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login():
    try:
        # Wait for the email field and enter the username
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(username)

        # Wait for the password field and enter the password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        )
        login_button.click()

        # Add any additional actions post-login

    except Exception as e:
        print(e)
        driver.quit()


def handle_modal():
    try:
        # Wait for the modal to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root"))
        )

        # Locate the Dismiss button and click it
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Dismiss')]")))
        dismiss_button.click()

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
        # Wait for and find all SVGs that match the criteria
        svg_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.MuiIconButton-root svg[data-testid='AddIcon']")
            )
        )

        # Get the parent button elements of the selected SVGs
        add_buttons = [driver.execute_script("return arguments[0].parentNode;", svg) for svg in svg_elements]

        # Randomly select three buttons
        if len(add_buttons) >= 3:
            selected_buttons = random.sample(add_buttons, 3)
        else:
            print("Not enough items to add to cart.")
            return

        # Click on each of the selected buttons
        for button in selected_buttons:
            # Scroll the button into view and click
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()

    except Exception as e:
        print("Error adding items to cart:", e)


if __name__ == "__main__":
    # Replace with your own credentials and URL
    url = "https://jng-fnd2-zpqy7.ondigitalocean.app"
    username = "mbugua@jungopharm.com"
    password = "123456789"
    # Setup WebDriver
    driver = webdriver.Firefox()
    # Path to ChromeDriver
    driver.get(url)
    login()
    handle_modal()  # Call the function to handle the modal
    sell_on_pos()

