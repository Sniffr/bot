import csv
import datetime
import os
import random
import threading
from datetime import date, timedelta

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
        email_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        type_like_human(email_field, username)
        random_delay(1, 2)

        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        type_like_human(password_field, password)
        random_delay(1, 2)

        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        )
        human_like_click(login_button, driver)

    except Exception as e:
        print("error logging in ", e)
        driver.quit()

def handle_modal(driver):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root"))
        )
        random_delay(1, 2)

        dismiss_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Dismiss')]")))
        human_like_click(dismiss_button, driver)

    except Exception as e:
        print("No modal found or other error:", e)
        driver.quit()

def sell_on_pos(driver):
    try:
        pos_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Point Of Sale')]"))
        )
        pos_button.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.MuiIconButton-root"))
        )
        add_random_items_to_cart(driver)
        checkout(driver)
    except Exception as e:
        print("Initial POS action failed:", e)
        try:
            menu_icon = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/div/button[1]"))
            )
            human_like_click(menu_icon, driver)
            sell_on_pos(driver)
        except Exception as e:
            print("Error clicking menu icon:", e)
            driver.quit()

def checkout(driver):
    try:
        checkout_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue to Payment')]"))
        )
        checkout_button.click()

        cash_option = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'CASH')]"))
        )
        driver.execute_script("arguments[0].click();", cash_option)

        confirm_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()

        close_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div[1]/div[2]/button"))
        )
        close_button.click()

    except Exception as e:
        print("Error during checkout:", e)

def add_random_items_to_cart(driver):
    try:
        svg_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.MuiIconButton-root svg[data-testid='AddIcon']")
            )
        )

        add_buttons = [driver.execute_script("return arguments[0].parentNode;", svg) for svg in svg_elements]

        num_items_to_add = random.randint(2, 8)
        if len(add_buttons) >= num_items_to_add:
            selected_buttons = random.sample(add_buttons, num_items_to_add)
            for button in selected_buttons:
                num_clicks = random.randint(1, 3)
                for _ in range(num_clicks):
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    random_delay(0.5, 1)
        else:
            print("Not enough items to add to cart.")

    except Exception as e:
        print("Error adding items to cart:", e)

def selectprofile(username):
    base_profile_dir = os.path.abspath('./profiles')
    print(f"Base Profile Directory: {base_profile_dir}")

    if not os.path.exists(base_profile_dir):
        os.makedirs(base_profile_dir)
        print(f"Created base directory at {base_profile_dir}")

    profile_path = os.path.join(base_profile_dir, username)
    print(f"Profile Path: {profile_path}")

    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
        print(f"Created profile directory at {profile_path}")

    chrome_options = Options()
    min_width, min_height = 1400, 1000
    random_width = random.randint(min_width, min_width)
    random_height = random.randint(min_height, min_height)

    chrome_options.add_argument(f"--window-size={random_width},{random_height}")
    chrome_options.add_argument("--start-minimized")

    return chrome_options

def run_driver(username, password):
    print(f"Running driver for {username} at {datetime.datetime.now().strftime('%H:%M:%S')}")
    chrome_option = selectprofile(username)
    driver = webdriver.Chrome(options=chrome_option)
    print(f"Email: {username}, Password: {password}")

    driver.get("https://jng-main-2-72c5t.ondigitalocean.app/")
    login(driver, username, password)

    handle_modal(driver)
    sell_on_pos(driver)
    driver.quit()

def generate_random_times(num_actions, start_hour, end_hour):
    total_minutes = (end_hour - start_hour) * 60
    times = set()
    while len(times) < num_actions:
        random_minute = random.randint(0, total_minutes - 1)
        time_comb = (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=start_hour))
                     + datetime.timedelta(minutes=random_minute)).time()
        times.add(time_comb.strftime('%H:%M'))

    return list(times)

def get_todays_schedule(db):
    today = date.today()
    return list(db['schedules'].find({"date": today.strftime("%Y-%m-%d")}))

def create_daily_schedule(users_collection, schedules_collection):
    users = users_collection.find()
    today = date.today()
    scheduled_times = {}

    for user in users:
        num_actions_per_user = random.randint(5, 15)  # Increased range for more sales
        scheduled_for_user = 0

        while scheduled_for_user < num_actions_per_user:
            times = generate_random_times(num_actions_per_user - scheduled_for_user, 7, 21)

            for c_time in times:
                if scheduled_times.get(c_time, 0) < 8:  # Increased limit per time slot
                    task_id = ObjectId()
                    schedules_collection.insert_one({
                        '_id': task_id,
                        'email': user['email'],
                        'scheduled_time': c_time,
                        'date': today.strftime("%Y-%m-%d"),
                        'completed': False
                    })
                    scheduled_times[c_time] = scheduled_times.get(c_time, 0) + 1
                    scheduled_for_user += 1
                    print(f"Scheduled sale for {user['email']} at {c_time}")

def schedule_tasks(db):
    todays_schedule = get_todays_schedule(db)
    if not todays_schedule:
        create_daily_schedule(db['users'], db['schedules'])
        todays_schedule = get_todays_schedule(db)

    print("\nToday's Scheduled Sales:")
    for task in todays_schedule:
        if not task['completed']:
            print(f"User: {task['email']}, Time: {task['scheduled_time']}")
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
    connection_string = ("mongodb://archer:malingu@ac-r0bcexe-shard-00-00.h5wj3us.mongodb.net:27017,"
                         "ac-r0bcexe-shard-00-01.h5wj3us.mongodb.net:27017,"
                         "ac-r0bcexe-shard-00-02.h5wj3us.mongodb.net:27017/?ssl=true&replicaSet=atlas-gvmkrc-shard-0"
                         "&authSource=admin&retryWrites=true&w=majority")
    client = MongoClient(connection_string, tlsCAFile=ca)
    db = client['JungoUsers']

    # Start scheduling tasks in the main thread
    schedule_tasks(db)

    # Start running scheduled tasks
    run_scheduled_tasks()