#pages/user_management_page.py

import logging

from pages.base_page import BasePage
from utils.download_utils import clean_download_dir, get_download_dir


class UserManagementPage(BasePage):
    """
    Page Object aligned strictly with Playwright codegen behavior
    so that pytest test cases pass reliably.
    """

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    # ==================================================
    # NAVIGATION
    # ==================================================

    def go_to_groups(self):
        self.logger.info("Navigating to Groups")

        self.page.get_by_text("User Management").click()
        self.page.get_by_role("link", name="Groups").click()
        self.page.get_by_text("User Groups").wait_for()

    def go_to_users(self):
        self.logger.info("Navigating to Users")

        self.page.get_by_text("User Management").click()
        self.page.get_by_role("link", name="Users").click()
        self.page.get_by_text("Users").wait_for()

    # ==================================================
    # COMMON HELPERS
    # ==================================================

    def _complete_wizard(self):
        for _ in range(4):
            self.page.get_by_role("button", name="chevronright").click()

    # ==================================================
    # GRID
    # ==================================================

    @property
    def grid(self):
        return self.page.locator("dx-data-grid")

    # ==================================================
    # GROUP ACTIONS
    # ==================================================

    def add_group(self, name: str, description: str):
        self.logger.info(f"Adding group {name}")

        self.page.get_by_role("button", name="Add Group").click()
        self.page.get_by_role("textbox", name="Group Name").fill(name)
        self.page.get_by_role("textbox", name="Group Description").fill(description)

        self._complete_wizard()
        self.page.get_by_role("button", name="Save").click()

        self.page.get_by_text("is added").wait_for()

    def edit_first_group(self):
        self.logger.info("Editing first group")

        # Same selector codegen used
        self.page.get_by_role("button").nth(5).click()
        self._complete_wizard()
        self.page.get_by_role("button", name="Save").click()

        self.page.get_by_text("is updated").wait_for()

    def delete_first_group(self):
        self.logger.info("Deleting first group")

        self.page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.icon-12.btn-icon.btn-delete"
        ).first.click()

        self.page.get_by_role("button", name="Yes").click()
        self.page.get_by_text("is deleted").wait_for()

    # ==================================================
    # USER ACTIONS
    # ==================================================

    def add_user(self, user: dict):
        self.logger.info(f"Adding user {user['login_id']}")

        self.page.get_by_role("button").nth(4).click()

        self.page.get_by_role("textbox", name="Login ID").fill(user["login_id"])
        self.page.get_by_role("textbox", name="First Name").fill(user["first_name"])
        self.page.get_by_role("textbox", name="Last Name").fill(user["last_name"])
        self.page.get_by_role("textbox", name="Company").fill(user["company"])
        self.page.get_by_role("textbox", name="Title").fill(user["title"])
        self.page.get_by_role("textbox", name="Email Address").fill(user["email"])
        self.page.get_by_role("textbox", name="Mobile Phone Number").fill(
            user["mobile"]
        )
        self.page.get_by_role("textbox", name="Work Phone Number").fill(
            user["work_phone"]
        )

        self._complete_wizard()
        self.page.get_by_role("button", name="Save").click()

        self.page.get_by_text("is added").wait_for()

    def edit_first_user(self):
        self.logger.info("Editing first user")

        self.page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.icon-12"
        ).first.click()

        self._complete_wizard()
        self.page.get_by_role("button", name="Save").click()

        self.page.get_by_text("is updated").wait_for()

    def delete_first_user(self):
        self.logger.info("Deleting first user")

        self.page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.icon-12.btn-icon.btn-delete"
        ).first.click()

        self.page.get_by_role("button", name="Yes").click()
        self.page.get_by_text("is deleted").wait_for()

    # # ==================================================
    # # EXPORTS (Excel only – as per your tests)
    # # ==================================================

    def export_excel(self):
        self.logger.info("Exporting Excel")

        # clean_download_dir()

        self.page.get_by_role("button", name="Export").click()
        self.page.get_by_role("radio", name="Excel").click()

        with self.page.expect_download() as download_info:
            self.page.get_by_role("button", name="Download").click()

        download = download_info.value
        path = get_download_dir() / download.suggested_filename
        download.save_as(path)
        return path