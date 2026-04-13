from playwright.sync_api import Page

class RegistrationPage:
    def __init__(self, page:Page):
        self.page = page
        # ===== Locators =====
        # Input fields
        self.txt_first_name = self.page.locator("#input-firstname")
        self.txt_lastname = self.page.locator('#input-lastname')
        self.txt_email = self.page.locator('#input-email')
        self.txt_password = self.page.locator('#input-password')

        # Checkbox and buttons
        self.chk_policy = self.page.locator("input[name='agree']")
        self.btn_continue = page.locator("button:has-text('Continue')")

        # Confirmation message (displayed after successful registration)
        self.msg_confirmation = self.page.locator("h1:has-text('Your Account Has Been Created!')")

    # ===== Action Methods =====
    def set_first_name(self, fname: str):
        """Enter the user's first name into the 'First Name' field."""
        self.txt_first_name.fill(fname)

    def set_last_name(self, lname: str):
        """Enter the user's last name into the 'Last Name' field."""
        self.txt_lastname.fill(lname)

    def set_email(self, email: str):
        """Enter the user's email address."""
        self.txt_email.fill(email)

    def set_password(self, pwd: str):
        """Enter the password."""
        self.txt_password.fill(pwd)

    def set_privacy_policy(self):
        """Select the 'Privacy Policy' checkbox."""
        self.chk_policy.check()

    def click_continue(self):
        """Click on the 'Continue' button to submit the registration form."""
        self.btn_continue.click()

    def get_confirmation_msg(self):
        """
        Return the confirmation message locator.
        This can be used to verify successful registration.
        """
        return self.msg_confirmation

    # ===== Combined Workflow =====

    def complete_registration(self, user_data: dict):
        """
        Complete the full registration process using provided user data.

        Example:
        user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "telephone": "9876543210",
            "password": "Test@123"
        }
        """
        self.set_first_name(user_data["firstName"])
        self.set_last_name(user_data["lastName"])
        self.set_email(user_data["email"])
        self.set_password(user_data["password"])
        self.set_privacy_policy()
        self.click_continue()

        # Return confirmation message element for validation
        return self.get_confirmation_msg()
