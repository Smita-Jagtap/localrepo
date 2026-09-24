import logging
from playwright.sync_api import expect
from pages.base_page import BasePage


class ReportsPage(BasePage):
    """Page Object for Reports section"""

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

        # ==================================================
        # LOCATORS
        # ==================================================

        self.reports_menu = self.page.get_by_text("Reports", exact=True)
        # self.canned_reports_link = self.page.locator("a:has-text('Canned Reports List')")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.delete_button = self.page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-12.btn-icon.btn-delete").first
        self.confirm_yes_button = self.page.get_by_role("button", name="Yes")
        self.add_canned_report_button = self.page.locator("dx-button:has(img[src*='add_to_photos'])")
        self.add_canned_report_modal = self.page.locator(".dx-overlay-content").filter(has_text="Add Canned Report")

        # ---- Create Report ----
        self.group_name_dropdown = self.add_canned_report_modal.locator("div.dx-dropdowneditor-button").first
        self.report_title_input = self.add_canned_report_modal.locator("input.dx-texteditor-input[name='title']")
        self.report_description_input = self.add_canned_report_modal.locator("textarea.dx-texteditor-input[name='desc']")
        self.report_link_input = self.add_canned_report_modal.locator("input.dx-texteditor-input[name='linkAddress']")

        # ---- Upload Thumbnail ----
        self.thumbnail_upload = self.page.locator("file-uploader[name='thumbnailUploader'] .dx-fileuploader-button")
        self.upload_error_message = self.page.locator(".dx-invalid-message-content")

        # ---- Export ----

        self.export_icon = self.page.locator( "dx-button:has(img[src*='download'])")
        self.export_modal = self.page.locator(".dx-overlay-content:has-text('Export to')")
        self.download_button = self.page.locator(".dx-overlay-content span.dx-button-text",has_text="Download")
        self.export_history_link = self.page.locator("a:has-text('Export Download History')")
        self.tableau_link = self.page.locator("text=Tableau")
        self.theme_switch = self.page.locator("#theme-switch")

    # ==================================================
    # ACTION METHODS
    # ==================================================

    def open_reports_menu(self):
        self.logger.info("Opening Reports menu")
        self.reports_menu.click(force=True)

    def hover_on_reports_menu(self):
        self.reports_menu.hover()

    def open_canned_reports(self):
        self.logger.info("Opening Canned Reports List")
        self.page.wait_for_selector("#light", state="hidden", timeout=15000) #added
        self.reports_menu.hover()
        self.page.locator("a[href*='home/reports/canned-reports-list']").click()
        # Wait for page content, NOT menu
        self.page.wait_for_selector("app-canned-list span.title",timeout=15000)

    def open_export_history(self):
        self.logger.info("Opening Export Download History")
        self.wait_for_toast_to_disappear()
        # Open Reports menu
        self.reports_menu.hover()
        self.reports_menu.click(force=True)

        # Click ONLY the visible menu item

        export_menu = self.page.locator("//a[normalize-space()='Export Download History']")
        export_menu.wait_for(state="visible", timeout=5000)
        export_menu.click(force=True)

        # Validate navigation
        self.page.wait_for_url("**/reports/export-downloading-history",timeout=20000)

    def open_tableau(self):
        self.tableau_link.wait_for(state="visible")
        self.tableau_link.click(force=True)
        self.page.wait_for_load_state("load")

    def delete_first_report(self):
        # Select ONLY actual data rows
        first_row = self.page.locator("tbody tr.dx-data-row").first
        first_row.wait_for(state="visible", timeout=10000)

        #  Required for DevExtreme action icons
        first_row.scroll_into_view_if_needed()
        first_row.hover()

        # Click the delete BUTTON (not img)
        delete_button = first_row.locator("dx-button:has(img[src*='delete.svg'])")
        delete_button.wait_for(state="visible", timeout=5000)
        delete_button.click(force=True)

    def _get_row(self, group, title):
        return self.page.locator("tr").filter(
            has=self.page.locator("td", has_text=group)
        ).filter(
            has=self.page.locator("td", has_text=title)
        )

    def confirm_delete_yes(self):
        yes_btn = self.page.locator(".dx-popup-content span.dx-button-text",has_text="Yes")
        yes_btn.wait_for(state="visible", timeout=10000)
        yes_btn.click(force=True)

    def confirm_delete_no(self):
        no_btn = self.page.locator(".dx-popup-content span.dx-button-text",has_text="No")
        no_btn.wait_for(state="visible", timeout=10000)
        no_btn.click(force=True)

    def is_report_present(self, group, title):
        return self._get_row(group, title).is_visible()

    def add_new_reports(self, title, description, link):
        # Open Add Canned Report modal
        self.add_canned_report_button.click(force=True)
        self.add_canned_report_modal.wait_for(state="visible", timeout=10000)

        # Open Group dropdown
        self.group_name_dropdown.click()

        #  Select SECOND available group dynamically
        first_group = self.page.locator(".dx-list-item").nth(1)
        first_group.wait_for(state="visible", timeout=5000)
        first_group.click(force=True)

        # Fill Report Title
        self.report_title_input.fill(title)

        # Fill Description
        self.report_description_input.fill(description)

        # Fill Link
        self.report_link_input.fill(link)

    def save_report(self):
        self.scroll_edit_modal_to_bottom()
        self.save_button.click()

    def set_input(self, locator, value: str):
        locator.evaluate(
            """(el, val) => {
                el.value = val;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.dispatchEvent(new Event('blur', { bubbles: true }));
            }""",
            value,
        )

    def upload_thumbnail(self, file_path: str):
        # Ensure modal is visible
        self.add_canned_report_modal.wait_for(state="visible", timeout=10000)

        # Scroll so Upload button is active
        self.scroll_edit_modal_to_bottom()

        upload_btn = self.page.locator(
            "dx-file-uploader[name='thumbnailUploader'] .dx-fileuploader-button"
        )

        # Fail fast if disabled
        expect(upload_btn).to_be_enabled()

        # Listen for file chooser BEFORE click
        with self.page.expect_file_chooser() as fc_info:
            upload_btn.click(force=True)

        # Set file
        fc_info.value.set_files(file_path)

    def is_report_added_successfully(self):
        toast = self.page.locator(".notifications-response",has_text="New Canned Report has been added successfully.")
        toast.wait_for(state="visible", timeout=10000)
        return toast.is_visible()

    def is_report_updated_successfully(self):
        toast = self.page.locator(".notifications-response",has_text="Canned Report has been updated successfully.")
        toast.wait_for(state="visible", timeout=15000)
        return toast.is_visible()

    def is_delete_success_message_visible(self, group, title):
        msg = f"{group} - {title} is deleted successfully."
        toast = self.page.locator(".notifications-response", has_text=msg)
        toast.wait_for(state="visible", timeout=10000)
        return toast.is_visible()

    # ---------- EDIT REPORT ----------

    def click_edit_first_report(self):
        # First actual data row (skip header)
        first_row = self.page.locator("tbody tr.dx-data-row").first
        first_row.wait_for(state="visible", timeout=10000)

        # Required for DevExtreme buttons
        first_row.scroll_into_view_if_needed()
        first_row.hover()

        # Correct edit button locator
        edit_button = first_row.locator("dx-button:has(img[src*='edit'])")
        edit_button.wait_for(state="visible", timeout=5000)
        edit_button.click(force=True)

    def wait_for_edit_popup(self):
        self.page.locator("text=Edit Canned Report").wait_for(state="visible", timeout=10000)
        self.scroll_edit_modal_to_bottom()

    def edit_report_description(self, new_description):
        desc = (
            self.page.locator(".dx-overlay-content")
            .filter(has_text="Edit Canned Report")
            .locator("textarea.dx-texteditor-input[name='desc']")
        )

        desc.wait_for(state="visible", timeout=15000)
        desc.click(force=True)
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        self.page.keyboard.type(new_description, delay=30)

    def save_edit(self):
        save_btn = self.page.locator(".dx-overlay-content span.dx-button-text",has_text="Save")
        save_btn.wait_for(state="visible", timeout=10000)
        save_btn.click(force=True)

    def cancel_edit(self):
        cancel_btn = self.page.locator(".dx-overlay-content span.dx-button-text",has_text="Cancel")
        cancel_btn.wait_for(state="visible", timeout=10000)
        cancel_btn.click(force=True)

    def confirm_cancel_yes(self):
        self.page.locator(".dx-overlay-content span.dx-button-text",has_text="Yes").click(force=True)

        # wait until navigation completes
        self.page.wait_for_selector("span.title:has-text('Canned Reports List')",timeout=15000)

    def confirm_cancel_no(self):
        self.page.locator(".dx-overlay-content span.dx-button-text",has_text="No").click(force=True)

    # Force Save / Cancel into view before clicking
    def scroll_edit_modal_to_bottom(self):
        self.page.evaluate("""
            () => {
                const modal = document.querySelector('.dx-overlay-content');
                if (modal) {
                    modal.scrollTop = modal.scrollHeight;
                }
            }
        """)

    def wait_for_cancel_confirmation(self):
        self.page.locator(
            "text=Do you want to cancel without saving the data?"
        ).wait_for(state="visible", timeout=10000)

    def click_edit_close_x(self):
        close_btn = self.page.locator(".dx-overlay-content span",has_text="×")
        close_btn.wait_for(state="visible", timeout=5000)
        close_btn.click(force=True)

    def wait_for_toast_to_disappear(self):
        toast = self.page.locator(".notifications-response")
        if toast.is_visible():
            toast.wait_for(state="hidden", timeout=10000)






