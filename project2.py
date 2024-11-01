from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Initialize the WebDriver (assuming chromedriver is in the system PATH)
driver = webdriver.Chrome()
driver.maximize_window()

# Define the URL for OrangeHRM
url = "http://orangehrm-url.com"  # Replace with actual OrangeHRM URL

# Helper function to log in as Admin
def login_as_admin(username="Admin", password="admin_password"):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txtUsername")))
        
        driver.find_element(By.ID, "txtUsername").send_keys(username)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        driver.find_element(By.ID, "btnLogin").click()
        
        print("Logged in as Admin.")
        time.sleep(2)
    except TimeoutException:
        print("Login fields not found or timed out.")

# Test Case 1: Launch URL and Click Forgot Password
def test_forget_password():
    driver.get(url)
    try:
        forgot_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot your password?"))
        )
        forgot_password.click()
        print("Forgot Password link clicked successfully.")
    except TimeoutException:
        print("Forgot Password link not found.")

# Test Case 2: Validate Menu Options on Admin Page
def validate_admin_menus():
    expected_menus = ["Admin", "PIM", "Leave", "Time", "Recruitment",
                      "My Info", "Performance", "Dashboard", "Directory",
                      "Maintenance", "Buzz"]
    try:
        menu_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='mainMenuFirstLevelUnorderedList']/li"))
        )
        displayed_menus = [menu.text for menu in menu_elements]
        
        for menu in expected_menus:
            assert menu in displayed_menus, f"{menu} menu option is missing!"
        print("All main menu options are displayed on the Admin page.")
    except (TimeoutException, AssertionError) as e:
        print(f"Menu validation error: {e}")

# Test Case 3: Validate Submenus Under Admin
def validate_admin_submenus():
    try:
        driver.find_element(By.ID, "menu_admin_viewAdminModule").click()
        time.sleep(2)
        
        expected_submenus = ["User Management", "Job", "Organization", "Qualifications",
                             "Nationalities", "Corporate Banking", "Configuration"]
        submenu_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='menu']/ul/li/a"))
        )
        displayed_submenus = [submenu.text for submenu in submenu_elements]
        
        for submenu in expected_submenus:
            assert submenu in displayed_submenus, f"{submenu} submenu option is missing!"
        print("All Admin submenus are displayed correctly.")
    except (TimeoutException, AssertionError) as e:
        print(f"Submenu validation error: {e}")

# Run all test cases
try:
    # Test 1: Click Forgot Password
    test_forget_password()
    
    # Test 2: Login as Admin
    login_as_admin()
    
    # Test 3: Validate main Admin page menu options
    validate_admin_menus()
    
    # Test 4: Validate Admin page submenus
    validate_admin_submenus()

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    driver.quit()
