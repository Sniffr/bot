import csv
import datetime
import os
import random
from datetime import date

import certifi
from bson import ObjectId
from pymongo import MongoClient
import schedule
import pandas as pd

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


def human_like_click(element, driver):
    random_delay(0.5, 2)
    ActionChains(driver).move_to_element(element).click().perform()
    random_delay(0.5, 1)


def login(driver, username, password):
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
        human_like_click(login_button, driver)

    except Exception as e:
        print("error logging in ", e)
        driver.quit()


def handle_modal(driver):
    try:
        # Wait for the modal to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root"))
        )
        random_delay(1, 2)

        # Locate and click the Dismiss button
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Dismiss')]")))
        human_like_click(dismiss_button, driver)

    except Exception as e:
        print("No modal found or other error:", e)
        login(driver, us, passw)
        handle_modal(driver)


def sell_on_pos(driver):
    try:
        pos_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Point Of Sale')]"))
        )
        pos_button.click()
        # Wait for the items to load (i.e., the 'Add' buttons to appear)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.MuiIconButton-root"))
        )
        add_random_items_to_cart(driver)
        checkout(driver)
    except Exception as e:
        print("Initial POS action failed:", e)
        try:
            # Attempt to click on the menu icon
            menu_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/div/button[1]"))
            )
            human_like_click(menu_icon, driver)
            # Add further actions if needed, like clicking on the POS button in the menu
            sell_on_pos(driver)
        except Exception as e:
            print("Error clicking menu icon:", e)
            driver.quit()


def checkout(driver):
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


def add_random_items_to_cart(driver):
    try:
        # Find all SVGs
        svg_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.MuiIconButton-root svg[data-testid='AddIcon']")
            )
        )

        # Get the parent button elements of the selected SVGs
        add_buttons = [driver.execute_script("return arguments[0].parentNode;", svg) for svg in svg_elements]

        # Randomly determine how many items to add (between 2 and 8)
        num_items_to_add = random.randint(2, 8)
        if len(add_buttons) >= num_items_to_add:
            selected_buttons = random.sample(add_buttons, num_items_to_add)
            for button in selected_buttons:
                # Randomly decide how many times to click the button (e.g., between 1 to 3 times)
                num_clicks = random.randint(1, 3)
                for _ in range(num_clicks):
                    # Scroll the button into view and click
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    random_delay(0.5, 1)  # Adding a short delay between clicks
        else:
            print("Not enough items to add to cart.")

    except Exception as e:
        print("Error adding items to cart:", e)


def select_belea_pharma(driver):
    try:
        # Wait for the element to be present on the page
        belea_pharma_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'BelEa Pharma')]"))
        )
        # Click the element
        belea_pharma_element.click()
        print("BelEa Pharma selected.")
    except Exception as e:
        print("Error selecting BelEa Pharma:", e)


def makeorder(driver):
    orders_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Order Products')]"))
    )
    orders_button.click()
    # Wait for the items to load (i.e., the 'Add' buttons to appear)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.MuiIconButton-root"))
    )
    select_belea_pharma(driver)

    # add_random_items_to_cart(driver)
    # checkout(driver)


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
    min_width, min_height = 1400, 1000
    random_width = random.randint(min_width, min_width)
    random_height = random.randint(min_height, min_height)

    # Set the window size
    chrome_options.add_argument(f"--window-size={random_width},{random_height}")
    # chrome_options.add_argument("--headless")

    return chrome_options


def run_driver(username, password):
    print(f"Running driver for {username} at {datetime.datetime.now().strftime('%H:%M:%S')}")
    global us
    global passw
    us = username
    passw = password
    chrome_option = selectprofile(username)
    driver = webdriver.Chrome(options=chrome_option)
    print(f"Email: {username}, Password: {password}")

    driver.get("https://business.jungopharm.com")
    login(driver, username, password)

    handle_modal(driver)
    sell_on_pos(driver)
    driver.quit()


def run_order_driver(username, password):
    print(f"Running driver for {username} at {datetime.datetime.now().strftime('%H:%M:%S')}")
    global us
    global passw
    us = username
    passw = password
    chrome_option = selectprofile(username)
    driver = webdriver.Chrome(options=chrome_option)
    print(f"Email: {username}, Password: {password}")

    driver.get("https://business.jungopharm.com")
    login(driver, username, password)

    handle_modal(driver)
    makeorder(driver)


def generate_random_times(num_actions, start_hour, end_hour):
    # Calculate the total minutes in the time range
    total_minutes = (end_hour - start_hour) * 60

    times = set()
    while len(times) < num_actions:
        # Generate a random minute offset within the range
        random_minute = random.randint(0, total_minutes - 1)

        # Calculate the actual time
        time = (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=start_hour))
                + datetime.timedelta(minutes=random_minute)).time()

        # Format and add to the set
        times.add(time.strftime('%H:%M'))

    return list(times)


def schedule_drivers():
    df = pd.read_csv('jungo_users.csv')
    email_list = df['email'].tolist()
    ca = certifi.where()
    connection_string = "mongodb://archer:malingu@ac-r0bcexe-shard-00-00.h5wj3us.mongodb.net:27017,ac-r0bcexe-shard-00-01.h5wj3us.mongodb.net:27017,ac-r0bcexe-shard-00-02.h5wj3us.mongodb.net:27017/?ssl=true&replicaSet=atlas-gvmkrc-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(connection_string, tlsCAFile=ca)
    db = client['JungoUsers']
    users_collection = db['users']
    schedules_collection = db['schedules']  # A new collection for schedules

    users = users_collection.find()
    num_actions_per_user = random.randint(4, 20)

    for user in users:
        # Generate random times for each user
        times = generate_random_times(num_actions_per_user, 16, 21)

        for time in times:
            # Create a unique identifier for the task
            task_id = ObjectId()

            # Schedule the driver to run at each specified time
            schedule.every().day.at(time).do(run_driver, user['Emails'], '12345678')
            print(f"Scheduled for {user['Emails']} at {time}")

            # Save the schedule in MongoDB
            schedules_collection.insert_one({
                '_id': task_id,
                'email': user['Emails'],
                'scheduled_time': time
            })


def get_todays_schedule(db):
    today = date.today()
    return list(db['schedules'].find({"date": today.strftime("%Y-%m-%d")}))


def create_daily_schedule(users_collection, schedules_collection):
    users = users_collection.find()
    num_actions_per_user = random.randint(4, 20)
    today = date.today()

    for user in users:
        times = generate_random_times(num_actions_per_user, 16, 21)
        for time in times:
            task_id = ObjectId()
            schedules_collection.insert_one({
                '_id': task_id,
                'email': user['email'],
                'scheduled_time': time,
                'date': today.strftime("%Y-%m-%d"),
                'completed': False
            })


def schedule_tasks(db):
    todays_schedule = get_todays_schedule(db)
    if not todays_schedule:
        create_daily_schedule(db['users'], db['schedules'])
        todays_schedule = get_todays_schedule(db)

    for task in todays_schedule:
        if not task['completed']:
            schedule.every().day.at(task['scheduled_time']).do(run_task, task['_id'], task['email'], '12345678')


def run_task(task_id, username, password):
    run_driver(username, password)
    db['schedules'].update_one({'_id': task_id}, {'$set': {'completed': True}})


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    ca = certifi.where()
    connection_string = "mongodb://archer:malingu@ac-r0bcexe-shard-00-00.h5wj3us.mongodb.net:27017,ac-r0bcexe-shard-00-01.h5wj3us.mongodb.net:27017,ac-r0bcexe-shard-00-02.h5wj3us.mongodb.net:27017/?ssl=true&replicaSet=atlas-gvmkrc-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = MongoClient(connection_string, tlsCAFile=ca)
    db = client['JungoUsers']

    schedule_tasks(db)
    run_scheduled_tasks()
