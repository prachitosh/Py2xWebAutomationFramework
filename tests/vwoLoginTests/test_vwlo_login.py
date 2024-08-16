import time

import allure
import pytest
from selenium import webdriver
from tests.pageObjects.loginPage import LoginPage
from tests.pageObjects.DashboardPage import DashboardPage


# Assertions


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    # ChromeOptions
    driver.maximize_window()
    driver.get("https://app.vwo.com")
    return driver


@allure.epic("VWO Login Test")
@allure.feature("TC#0 - VWO App Negative Test")
@pytest.mark.negative
def test_vwo_login_negative(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="admin@admin@gmail.com", pwd="admin")
        time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Yours email, password, IP address or location did not match"
    except Exception as e:
        pytest.xfail("Failed")
        print(e)


@allure.epic("VWO Login Test")
@allure.feature("TC#1 - VWO App Positive Test")
@pytest.mark.positive
def test_vwo_login_positive(setup):
    driver = setup
    loginPage = LoginPage(driver)
    loginPage.login_to_vwo(usr="prachitoshnayak19@gmail.com", pwd="Password@1234")
    time.sleep(10)
    dashboardPage = DashboardPage(driver)
    assert "Dashboard" in driver.title
    assert "Prachitosh Nayak" in dashboardPage.user_logged_in_text()


# Invalid Email Format Test
@allure.epic("VWO Login Test")
@allure.feature("TC#2 - VWO App Negative Testcase")
@pytest.mark.negative
def test_vwo_login_negative(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="usr=admin@", pwd="admin")
        time.sleep(10)
        error_message = loginPage.get_error_message_text()
        assert error_message == "please enter valid email address"

    except Exception as e:
        pytest.xfail("Failed")
    print(e)


# Empty Email and Password Fields Test

@allure.epic("VWO Login Test")
@allure.feature("TC#3 - VWO App Negative Testcase")
@pytest.mark.negative
def test_vwo_login_negative(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="", pwd="")
        time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Your email, password, IP address or location did not match"

    except Exception as e:
        pytest.xfail("Failed")
        print(e)


# Incorrect Password Test
@allure.epic("VWO Login Test")
@allure.feature("TC#4 - VWO Negative Testcase")
@pytest.mark.negative
def test_vwo_login_negative(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="prachitoshnayak19@gmail.com", pwd="Password@123")
        time.sleep(10)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Your email, password, IP address or location did not match"
    except Exception as e:
        pytest.xfail("Failed")
        print(e)


# Invalid character in Email Test
@allure.epic("VWO Login Test")
@allure.feature("TC#5 - VWO Negative Testcase ")
@pytest.mark.negative
def test_vwo_login_negative(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="prachitosh@hhhan@gmail@", pwd="Password@1234")
        time.sleep(10)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Your email, password, IP address or location did not match"

    except Exception as e:
        pytest.xfail("Failed")
        print("e")


# SQL Injection Attempt Test
@allure.epic("VWO Login Test")
@allure.feature("TC#6 - VWO Negative Testcase ")
@pytest.mark.negative
def test_vwo_login_sql_injection(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="admin' OR 1=1--", pwd="admin")
        time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Yours email, password, IP address or location did not match"
    except Exception as e:
        pytest.xfail("Failed")
        print(e)


# Login with Invalid Email Domain Test
@allure.epic("VWO Login Test")
@allure.feature("TC#7 - VWO App Negative Test - Invalid Email Domain")
@pytest.mark.negative
def test_vwo_login_invalid_email_domain(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="prachitoshnayak19@invalid_domain.com", pwd="Password@1234")
        time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Please enter a valid email address"
    except Exception as e:
        pytest.xfail("Failed")
        print(e)


#  Login with Excessively Long Email Address Test
@allure.epic("VWO Login Test")
@allure.feature("TC#8 - VWO App Negative Test - Excessively Long Email Address")
@pytest.mark.negative
def test_vwo_login_long_email(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        long_email = "a" * 255 + "@gmail.com"  # Example of a very long email address
        loginPage.login_to_vwo(usr=long_email, pwd="Password@1234")
        time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Email address is too long"
    except Exception as e:
        pytest.xfail("Failed")
        print(e)


# Login with Correct Email but Incorrect Password Multiple Times Test
@allure.epic("VWO Login Test")
@allure.feature("TC#9 - VWO App Negative Test - Account Lockout After Multiple Failed Attempts")
@pytest.mark.negative
def test_vwo_login_account_lockout(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        for _ in range(5):  # Simulate 5 incorrect login attempts
            loginPage.login_to_vwo(usr="prachitoshnayak19@gmail.com", pwd="WrongPassword")
            time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Your account has been locked due to multiple failed login attempts. Please try again later."
    except Exception as e:
        pytest.xfail("Failed")
        print(e)


# Login with Expired Password Test

@allure.epic("VWO Login Test")
@allure.feature("TC#10 - VWO App Negative Test - Expired Password")
@pytest.mark.negative
def test_vwo_login_expired_password(setup):
    try:
        driver = setup
        loginPage = LoginPage(driver)
        loginPage.login_to_vwo(usr="prachitoshnayak19@gmail.com", pwd="ExpiredPassword")
        time.sleep(5)
        error_message = loginPage.get_error_message_text()
        assert error_message == "Your password has expired. Please reset your password."
    except Exception as e:
        pytest.xfail("Failed")
        print(e)
