import logging
import re
from pages.base_page import BasePage
from playwright.sync_api import expect
from utils.helpers import verify_tooltip


class ConfigurationPage(BasePage):
    """
    Page Object for the Configuration section.
    """

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    # ==================================================
    # LOCATORS
    # ==================================================

    @property
    def configuration_menu(self):
        return self.page.get_by_text("Configuration", exact=True)

    @property
    def active_data_schema_tab(self):
        return self.page.get_by_role("link", name="Active Data Schema")

    @property
    def notification_gateway_tab(self):
        return self.page.get_by_role("link", name="Notification Gateway")

    @property
    def site_properties_tab(self):
        return self.page.get_by_role("link", name="Site Properties")

    @property
    def subscription_tab(self):
        return self.page.get_by_role("link", name="Wayside Data Subscription")

    @property
    def reference_docs_tab(self):
        return self.page.get_by_role("link", name="Reference Documents and Web")

    # Reference Documents
    @property
    def add_reference_button(self):
        return self.page.get_by_role("button").nth(3)

    @property
    def reference_title_input(self):
        return self.page.get_by_role("textbox", name=re.compile("Title"))

    @property
    def reference_description_input(self):
        return self.page.get_by_role("textbox", name=re.compile("Description"))

    @property
    def reference_link_input(self):
        return self.page.get_by_role("textbox", name=re.compile("Link"))

    @property
    def reference_save_button(self):
        return self.page.get_by_role("button", name="Save")

    @property
    def reference_group_dropdown(self):
        return self.page.get_by_role("combobox", name=re.compile("Group Name"))

    @property
    def reference_group_listbox(self):
        return self.page.get_by_role("listbox")

    @property
    def reference_modal(self):
        return self.page.get_by_role("dialog").filter(
            has_text=re.compile("Add Reference", re.I)
        )

    # Subscription
    @property
    def add_subscription_button(self):
        return self.page.get_by_role("button").nth(3)

    @property
    def subscription_modal(self):
        return self.page.locator(".dx-overlay-content").filter(
            has_text="Add Subscription Details"
        )

    @property
    def subscription_name_input(self):
        return self.page.get_by_role("textbox", name=re.compile("Subscription Name"))

    @property
    def start_date_input(self):
        return self.page.get_by_role("combobox", name=re.compile("Start Date"))

    @property
    def end_date_input(self):
        return self.page.get_by_role("combobox", name=re.compile("End Date"))

    @property
    def subscription_excel_checkbox(self):
        return self.page.get_by_role("checkbox", name="EXCEL")

    @property
    def subscription_aoa_checkbox(self):
        return self.page.get_by_role("checkbox", name="AoA")

    @property
    def subscription_email_checkbox(self):
        return self.page.get_by_role("checkbox", name="Email")

    @property
    def recipient_email_dropdown(self):
        return self.page.get_by_role("combobox", name="Recipient Emails")

    @property
    def recipient_option(self):
        return self.page.get_by_text("akula tharun")

    @property
    def owner_dropdown(self):
        return self.page.get_by_role("combobox", name="Owner")

    @property
    def add_owner_button(self):
        return self.page.get_by_role("button", name="Add")

    # Site Properties
    @property
    def export_button(self):
        return self.page.locator(".form-check")

    @property
    def site_properties_first_data_row(self):
        return self.page.get_by_role("row").nth(1)

    @property
    def site_properties_row_edit_action(self):
        return self.page.locator(".commandTemplate").first

    @property
    def site_properties_cancel_button(self):
        return self.page.get_by_role("button", name=re.compile("cancel", re.I))

    @property
    def site_properties_cancel_yes(self):
        return self.page.get_by_role("button", name="Yes")

    @property
    def site_properties_tooltips(self):
        return [
            ("Site", "Site/Location"),
            ("System", "Wayside System Type"),
            ("Track", "Track"),
            ("Kilometrage (km)", "Track Kilometrage"),
            ("Station End", "Station End Closest to Site"),
            ("GPS Location (Lat., Long.)", "Site GPS Locations"),
            ("General", "General Speed Board"),
            ("Medium", "Medium Speed Board"),
            ("High", "High Speed Board"),
        ]

    # ==================================================
    # NAVIGATION
    # ==================================================

    def open_configuration_menu(self):
        self.logger.info("Opening Configuration menu")
        self.configuration_menu.click()

    def go_to_active_data_schema(self):
        self.logger.info("Navigating to Active Data Schema")
        self.open_configuration_menu()
        self.active_data_schema_tab.click()

    def go_to_site_properties(self):
        self.logger.info("Navigating to Site Properties")
        self.open_configuration_menu()
        self.site_properties_tab.click()

    def go_to_subscription_details(self):
        self.logger.info("Navigating to Wayside Subscription")
        self.open_configuration_menu()
        self.subscription_tab.click()


    def go_to_reference_documents(self):
        self.logger.info("Navigating to Reference Documents")
        self.open_configuration_menu()
        self.reference_docs_tab.click()

        # ADD THIS (CRITICAL)
        expect(self.add_reference_button).to_be_visible()


    # ==================================================
    # ACTIONS
    # ==================================================

    def toggle_theme(self):
        self.logger.info("Toggling application theme")
        self.page.locator("#theme-switch").click()

    def select_live_schema(self):
        self.logger.info("Selecting Live schema")
        self.page.get_by_role("radio", name=re.compile("Live")).click()

    def select_archived_schema(self):
        self.logger.info("Selecting Archived schema")
        self.page.get_by_role("radio", name=re.compile("Archived")).click()

    def increase_retention_days(self, times=1):
        self.logger.info(f"Increasing retention days by {times}")
        for _ in range(times):
            self.page.locator(".dx-numberbox-spin-up-icon").click()

    def decrease_retention_days(self, times=1):
        self.logger.info(f"Decreasing retention days by {times}")
        for _ in range(times):
            self.page.locator(".dx-numberbox-spin-down-icon").click()

    def save_configuration(self):
        self.logger.info("Saving configuration changes")

        save_button = self.page.get_by_role("button", name="Save")

        expect(save_button).to_be_visible()

        if not save_button.is_enabled():
            self.logger.warning("Save button is disabled - no changes detected")
            return  # skip safely

        save_button.click()

    def select_reference_group(self, group_name: str):
        self.logger.info(f"Selecting reference group: {group_name}")

        expect(self.reference_group_dropdown).to_be_visible()
        self.reference_group_dropdown.click()

        expect(self.reference_group_listbox).to_be_visible()
        self.reference_group_listbox.get_by_text(group_name, exact=True).click()

    def add_reference_document(self, group_name, title, description, link):
        self.logger.info("Adding reference document")

        expect(self.add_reference_button).to_be_visible()
        expect(self.add_reference_button).to_be_enabled()
        self.add_reference_button.click()

        # wait for actual usable element (NOT container)
        expect(self.reference_title_input).to_be_visible(timeout=10000)

        self.select_reference_group(group_name)

        self.logger.info(f"Filling reference details: {title}")
        self.reference_title_input.fill(title)
        self.reference_description_input.fill(description)
        self.reference_link_input.fill(link)

        self.logger.info("Saving reference document")
        expect(self.reference_save_button).to_be_visible()
        self.reference_save_button.click()

    def add_wayside_subscription(self, sub_data: dict) -> bool:
        try:
            self.logger.info("Starting wayside subscription creation")

            self.add_subscription_button.click()
            expect(self.subscription_modal).to_be_visible(timeout=5000)

            self.logger.info(f"Entering subscription name: {sub_data['name']}")
            self.subscription_name_input.fill(sub_data["name"])

            self.logger.info("Setting subscription dates")
            self.start_date_input.fill("27/05/2026")
            self.end_date_input.fill("30/05/2026")

            if sub_data["formats"].get("excel"):
                self.logger.info("Selecting EXCEL format")
                self.subscription_excel_checkbox.check()

            if sub_data["formats"].get("aoa"):
                self.logger.info("Selecting AOA format")
                self.subscription_aoa_checkbox.check()

            self.logger.info("Selecting email recipient")
            self.subscription_email_checkbox.check()
            self.recipient_email_dropdown.click()
            self.recipient_option.click()

            self.logger.info("Selecting subscription owner")
            self.owner_dropdown.click()
            self.owner_dropdown.press("ArrowDown")
            self.page.get_by_role("option", name="_ All").click()
            self.add_owner_button.click()

            self.logger.info("Saving subscription")
            save_btn = self.subscription_modal.get_by_role("button", name="Save")
            expect(save_btn).to_be_visible()
            expect(save_btn).to_be_enabled()
            save_btn.click()

            expect(self.subscription_modal).not_to_be_visible(timeout=5000)
            self.logger.info("Subscription created successfully")
            return True

        except Exception as e:
            self.logger.error(f"Subscription creation failed: {e}")
            return False

    # ==================================================
    # VALIDATIONS
    # ==================================================

    def is_active_schema_visible(self):
        self.logger.info("Checking Active Data Schema tab visibility")
        return self.active_data_schema_tab.is_visible()

    def is_notification_gateway_visible(self):
        self.logger.info("Checking Notification Gateway tab visibility")
        return self.notification_gateway_tab.is_visible()

    def is_site_properties_visible(self):
        self.logger.info("Checking Site Properties tab visibility")
        return self.site_properties_tab.is_visible()

    def is_subscription_details_visible(self):
        self.logger.info("Checking Subscription tab visibility")
        return self.subscription_tab.is_visible()

    def is_reference_documents_visible(self):
        self.logger.info("Checking Reference Documents tab visibility")
        return self.reference_docs_tab.is_visible()

    def verify_site_properties_tooltips(self):
        self.logger.info("Verifying Site Properties tooltips")
        verify_tooltip(self.page, self.site_properties_tooltips)
        return True

    def is_site_properties_edit_action_available(self):
        self.logger.info("Validating Site Properties edit functionality")

        expect(self.site_properties_first_data_row).to_be_visible()

        self.site_properties_first_data_row.hover()
        expect(self.site_properties_row_edit_action).to_be_visible()

        self.site_properties_row_edit_action.click()

        expect(self.site_properties_cancel_button).to_be_visible()
        self.site_properties_cancel_button.click()
        self.site_properties_cancel_yes.click()

        self.logger.info("Edit action verified successfully")
        return True

    def is_reference_document_save_successful(self):
        self.logger.info("Validating reference document save operation")

        dialog = self.page.get_by_text(
            "Add Reference Documents and Web Pages", exact=False
        )
        return not dialog.is_visible()