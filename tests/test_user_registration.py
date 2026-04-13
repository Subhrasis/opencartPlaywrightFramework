"""
Test Case: User Registration Functionality

===========================================
Test Steps
===========================================

1. Open the application in the browser.
2. Navigate to the "My Account" menu and click on "Register".
3. Enter user details:
   - First Name
   - Last Name
   - Email
   - Telephone Number
   - Password and Confirm Password
4. Accept the Privacy Policy checkbox.
5. Click on the "Continue" button.
6. Verify that the account creation confirmation message is displayed.

Expected Result:
----------------
After submitting valid details, the system should display the message:
"Your Account Has Been Created!"
"""

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utilities.random_data_util import RandomDataUtil
from playwright.sync_api import expect

def test_user_registration(page):
    '''
    Note that, the 'page' above is not the playwright fixture that we usually write as "page:Page".
        This is the 'page' that is returned from the page() method present in contest.py. That "page()"
        method is yielding or returning the page fixture.
    No need to write page.goto() here, as before returning the page, we are already doing page.goto().
    For this test we are interacting with 2 pages : home page and registration page. Thats why we have
        imported them.
    '''
    home_page = HomePage(page)                      # object of the HomePage class
    registration_page = RegistrationPage(page)      # object of the RegistrationPage class

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()                  # we will fill random texts from this script (faker)

    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    password = random_data.get_password()

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_password(password)

    registration_page.set_privacy_policy()
    registration_page.click_continue()

    '''
    Till here all the steps are automated. Now verification points
    '''

    # This will return confirmation message locator
    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_have_text("Your Account Has Been Created!")




