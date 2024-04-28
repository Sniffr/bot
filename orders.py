import os
import random
import time
from datetime import datetime
import datetime as date_time
import certifi
import schedule
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import functools
import time


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
        print(f"Logging in user: {username}")
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




def handle_modal(driver):
        print("Checking for modal...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root"))
        )
        random_delay(1, 2)

        dismiss_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Dismiss')]")))
        human_like_click(dismiss_button, driver)




def select_belea_pharma(driver):
        print("Attempting to select BelEa Pharma...")
        belea_pharma_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Belea Pharmaceuticals Limited')]"))
        )
        belea_pharma_element.click()
        print("BelEa Pharma selected.")


def add_order_items_to_cart(driver):
    print("Adding order items to cart...")
    add_button_icon = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button.MuiIconButton-root svg[data-testid='AddIcon']")
        )
    )
    number_to_add = random.randint(2, 8)
    buttons = random.sample(add_button_icon, number_to_add)

    for button in buttons:
        time.sleep(2)
        x = button.location['x']
        y = button.location['y']
        driver.execute_script("window.scrollTo({}, {});".format(x, y - 100))
        ActionChains(driver).move_to_element(button).click().perform()
        quantity_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "quantity"))
        )
        quantity_input.clear()
        quantity_input.send_keys(random.randint(3, 10))
        add_to_cart_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Add To Cart')]"))
        )
        add_to_cart_button.click()


def checkout_order(driver):
        print("Proceeding to checkout...")
        checkout_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Checkout')]"))
        )
        x = checkout_button.location['x']
        y = checkout_button.location['y']
        driver.execute_script("window.scrollTo({}, {});".format(x, y - 100))
        checkout_button.click()
        cash_option = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'M-Pesa on delivery')]"))
        )
        driver.execute_script("arguments[0].click();", cash_option)

        print("Setting delivery date to tomorrow...")
        delivery_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Delivery date')]/following-sibling::div//input"))
        )
        delivery_input.click()

        tomorrow = datetime.now() + date_time.timedelta(days=1)
        # Extract the day of the month from tomorrow's date
        tomorrow_day = tomorrow.day

        calendar_container = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiDayPicker-slideTransition"))
        )
        day_buttons = calendar_container.find_elements(By.CSS_SELECTOR, "button:not(.Mui-disabled)")
        for button in day_buttons:
            if button.text == str(tomorrow_day):
                button.click()  # Click the button to select tomorrow's date
                break  # Exit the loop once the correct day has been clicked

        ok_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK')]"))
        )
        ok_button.click()

        # set the value of the delivery here without read only

        print("Selecting delivery slot...")
        morning_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "MORNING"))
        )
        afternoon_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "MID_MORNING"))
        )
        midday_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "AFTERNOON"))
        )
        option = random.choice([morning_option, afternoon_option, midday_option])
        option.click()

        confirm_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Place Order')]"))
        )
        confirm_button.click()
        print("Order placed successfully.")



def makeorder(driver):
    print("Making an order...")
    orders_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Order Products')]"))
    )
    orders_button.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.MuiIconButton-root"))
    )
    select_belea_pharma(driver)
    add_order_items_to_cart(driver)
    checkout_order(driver)


def selectprofile(username):
    print(f"Selecting profile for {username}")
    base_profile_dir = os.path.abspath('./profiles')
    profile_path = os.path.join(base_profile_dir, username)
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
    chrome_options = Options()
    min_width, min_height = 1600, 720
    max_width, max_height = 1920, 1440
    random_width = random.randint(min_width, max_width)
    random_height = random.randint(min_height, max_height)
    chrome_options.add_argument(f"--window-size={random_width},{random_height}")
    print(f"Window size: {random_width}x{random_height}")
    return chrome_options


def run_order_driver(username, password):
    print(f"Running order driver for {username} at {date_time.datetime.now().strftime('%H:%M:%S')}")
    chrome_option = selectprofile(username)
    driver = webdriver.Chrome(options=chrome_option)
    driver.maximize_window()
    print(f"Email: {username}, Password: {password}")
    driver.get("https://business.jungopharm.com/")
    login(driver, username, password)
    handle_modal(driver)
    makeorder(driver)
    time.sleep(30)
    driver.quit()


def schedule_orders(users_list):
    print(f"Scheduling orders for {len(users_list)} users...")
    accounts_once = random.sample(list(users_list), random.randint(60, 90))
    for account in accounts_once:
        users_list.remove(account)
    accounts_twice = random.sample(list(users_list), 0)
    accounts = [{"username": account['email'], "password": "12345678", "order_twice": False} for account in
                accounts_once]
    accounts.extend(
        [{"username": account['email'],
          "password": "12                                                           pph 345678", "order_twice": True}
         for account in accounts_twice])
    for account in accounts:
        num_orders = 2 if account['order_twice'] else 1
        for _ in range(num_orders):
            scheduled_time = random_time_within_business_hours()
            orders_collection.insert_one({
                "username": account['username'],
                "password": account['password'],
                "scheduled_time": scheduled_time,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "completed": False
            })


def random_time_within_business_hours():
    hour = random.randint(datetime.now().hour, 22)
    minute = random.randint(1, 59)
    return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)


def run_task(task):
    print(f"Executing task for {task['username']} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        run_order_driver(task['username'], task['password'])
        orders_collection.update_one({"_id": task['_id']}, {"$set": {"completed": True}})
    except Exception as e:
        print(f"Error occurred while executing task for {task['username']}: {str(e)}")
        reschedule_task(task)


def run_one_task(username, password):
    run_order_driver(username, password)


def schedule_task(task):
    schedule_time = task['scheduled_time'].strftime('%H:%M')
    print(f"Scheduling task for {task['username']} at {schedule_time}")
    schedule.every().day.at(schedule_time).do(run_task, task)


def schedule_all_tasks():
    tasks = orders_collection.find({"completed": False, "date": datetime.now().strftime("%Y-%m-%d")})
    for task in tasks:
        schedule_task(task)


def is_schedule_made_for_today():
    """
    Check if a schedule is already made for today.
    """
    print("Checking if schedule is made for today...")
    today = datetime.now().strftime("%Y-%m-%d")
    return orders_collection.count_documents({"date": today}) > 0


def reschedule_incomplete_tasks():
    """Reschedules tasks scheduled for today and by the current time but not completed to a random future time within business hours."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # Find tasks for today that are not completed and update their scheduled_time to a random future time within business hours
    tasks_to_reschedule = orders_collection.find(
        {
            "date": today_str,  # Tasks scheduled for today
            "scheduled_time": {"$lt": now},  # Tasks whose scheduled time is earlier than the current time
            "completed": False  # Tasks that are not yet completed
        }
    )

    for task in tasks_to_reschedule:
        future_time = random_time_within_business_hours()
        orders_collection.update_one(
            {"_id": task['_id']},
            {
                "$set": {
                    "scheduled_time": future_time
                }
            }
        )

    print(f"Rescheduled tasks to random times within business hours.")


def run_scheduled_tasks():
    if not is_schedule_made_for_today():
        print("No schedule made for today. Making schedule...")
        schedule_orders(list(users))

    # Reschedule incomplete tasks before starting the scheduling loop
    reschedule_incomplete_tasks()

    print("Starting...")
    schedule_all_tasks()
    while True:
        schedule.run_pending()
        time.sleep(1)
def reschedule_task(task):
    future_time = random_time_within_business_hours()
    orders_collection.update_one(
        {"_id": task['_id']},
        {
            "$set": {
                "scheduled_time": future_time,
                "completed": False
            }
        }
    )
    print(f"Rescheduled task for {task['username']} to {future_time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    ca = certifi.where()
    connection_string = ("mongodb://archer:malingu@ac-r0bcexe-shard-00-00.h5wj3us.mongodb.net:27017,"
                         "ac-r0bcexe-shard-00-01.h5wj3us.mongodb.net:27017,"
                         "ac-r0bcexe-shard-00-02.h5wj3us.mongodb.net:27017/?ssl=true&replicaSet=atlas-gvmkrc-shard-0"
                         "&authSource=admin&retryWrites=true&w=majority")
    client = MongoClient(connection_string, tlsCAFile=ca)
    db = client['JungoUsers']
    orders_collection = db['orders']
    users_collection = db['users']
    users = users_collection.find({})
    run_scheduled_tasks()
