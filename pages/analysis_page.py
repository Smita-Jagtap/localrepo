from pages.base_page import BasePage
from playwright.sync_api import expect
import logging

logger = logging.getLogger(__name__)

class AnalysisPage(BasePage):
    """Page Object for the Analysis Page."""

    def __init__(self, page):
        super().__init__(page)
        # Locators
        # To navigate to required pages
        self.menu_analysis = page.get_by_role("menuitem", name="Analysis")
        self.step_change_vehicles_link = page.get_by_role("link", name="Step Change Vehicles")
        self.BAM_link = page.get_by_role("link", name="BAM")
        self.speed_distribution_graph_link = page.get_by_role("link", name="Speed Distribution Graph")

        self.heading_vehicles = page.locator("app-wild-step-change-vehicles").get_by_text("Step Change Vehicles")
        #For Step Change Vehicles Table:
        self.system=page.get_by_role("combobox").nth(1)
        self.optionWILD=page.get_by_role("option", name="WILD")
        self.optionBAM = page.get_by_role("option", name="BAM")
        self.show_element = page.get_by_role("combobox").nth(2)

        self.options = [
            ("All", page.get_by_role("option", name="All")),
            ("Active", page.get_by_role("option", name="Active")),
            ("Clear", page.get_by_role("option", name="Clear")),
            #("Never Set",page.get_by_role("option", name="Never Set")),
        ]

        self.apply_button = page.locator("dx-button[aria-label='Apply']")
        self.table = page.locator("dx-data-grid#StepChange")
        #to  help in scrolling inside the table as rows are not present in the DOM until the rows view is rendered and activated.
        #DevExtreme virtual scrolling
        self.rows_view = page.locator("#StepChange .dx-datagrid-rowsview")
        self.rows = page.locator("#StepChange tr.dx-data-row")

        #  History button locator
        self.history_button = page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.btn-icon.icon-16-f"
        ).first

        #  VPHG button (icon in last column)
        self.vphg_button = page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.btn-icon.icon-16-f"
        ).nth(-1)

        # Export Locators
        self.export_button = page.locator("#downloadIcon4")
        self.excel_radio_button = page.get_by_role("radio", name="Excel")
        self.pdf_radio_button = page.get_by_role("radio", name="PDF")
        self.export_download_button = page.get_by_role("button", name="Download")
        self.export_success_popup = page.get_by_text("Export Completed")

        #For Speed Distribution Graph Page
        self.heading_graph = page.get_by_text("Speed Distribution Graph")
        self.dropdowns = page.locator(".filters-list [role='combobox']")
        self.add_to_grid_btn = page.get_by_text("Add To Grid")
        #page.get_by_role("button", name="ADD TO GRID") - this also works


    # Navigate to step_change_vehicles
    def navigate_to_step_change_vehicles(self):
        self.menu_analysis.hover()
        self.step_change_vehicles_link.wait_for(state="visible", timeout=10000)
        self.step_change_vehicles_link.hover()
        self.BAM_link.wait_for(state="visible", timeout=10000)
        self.BAM_link.click()

    def verify_step_change_vehicles(self):
        """Verifies heading elements are visible on Step Change Vehicles Page."""
        expect(self.heading_vehicles).to_be_visible()
        logger.info('Heading elements are visible on Step Change Vehicles Page')
    
    #DevExtreme adds non-data rows to support virtual scrolling, free space height, layout alignment.
    #So, if we do not filter the rows properly, the count of rows will be incorrect as it will be
    #counting the non data rows.
    def get_actual_table_rows(self):
        raw_rows = self.rows.all_inner_texts()
        return [row.strip() for row in raw_rows if row.strip()]
        # The above line removes empty strings, "\t", "\xa0", layout-only rows.



    ### Helper Methods

    def validate_show_options_for_system(self, system_name: str):
        for option_name, option in self.options:
            #option_text = option.inner_text().strip()
            self.show_element.click()
            option.click()
            self.apply_button.click()
            logger.info(f"Checking {system_name} with {option_name}")
            self.validate_table_has_data(system_name, option_name)

    def validate_table_has_data(self, system_name, option_name):
        # Ensure table is visible
        expect(self.table).to_be_visible()

        # Trigger DevExtreme virtual rendering(scrolling)
        self.rows_view.hover()
        self.page.mouse.wheel(0, 1)

        actual_rows = self.get_actual_table_rows()

        assert actual_rows, (
            f"Step Change table is empty for "
            f"System: {system_name}, Show filter: {option_name}"
        )

    def verify_step_change_table(self):
        """
        Validates Step Change table data for all Show options
        under BAM and WILD systems.
        """
        # Default system (BAM)
        self.validate_show_options_for_system("BAM")

        # Switch to WILD system
        self.system.click()
        self.optionWILD.click()

        self.validate_show_options_for_system("WILD")



    def click_history_button(self):
        """Click History button and return popup page"""

        logger.info("Checking History button in Step Change Vehicles Table")
        # Ensure button is visible and clickable
        expect(self.history_button).to_be_visible()
        expect(self.history_button).to_be_enabled()  # ensures the button is clickable,not disabled

        # Capture popup
        with self.page.expect_popup() as popup_info:  # The next click is expected to open a new window
            self.history_button.click()

        history_page = popup_info.value  # Extracts the actual popup page object.

        logger.info('History button is visible on Step Change Vehicles Table.')

        # Wait for history page to load
        history_page.wait_for_load_state("domcontentloaded")  # Waits until the popup page’s DOM is fully loaded.

        return history_page

    def click_vphg_button(self):
        """Click VPHG button and return popup page"""

        logger.info("Checking VPHG button in Step Change Vehicles Table")
        # Ensure button is ready
        expect(self.vphg_button).to_be_visible()  # Ensures the VPHG button is visible on the UI.
        self.vphg_button.hover()

        # Capture popup page
        with self.page.expect_popup() as popup_info:  # The next user action is expected to open a new browser window or tab.
            self.vphg_button.click()

        vphg_page = popup_info.value
        vphg_page.wait_for_load_state("domcontentloaded")  # Waits until the popup page’s DOM is fully loaded.

        logger.info('History button is visible on Step Change Vehicles Table.')

        return vphg_page

    def export_site_properties_excel(self):
        """
        Trigger Excel export for Site Properties and return Download object.
        """
        logger.info("Exporting Site Properties - Excel")

        self.export_button.click()
        self.excel_radio_button.click()

        # Listen for both the popup window and the file download
        # The download is triggered by clicking the Download button
        with self.page.expect_download() as download_info:
            with self.page.expect_popup() as popup_info:
                self.export_download_button.click()

        popup_page = popup_info.value
        popup_page.close()

        download = download_info.value  
        # extract here
        #Log where Playwright stored the file temporarily
        try:
            file_path = download.path()
            logger.info(f"Excel file downloaded to temporary path: {file_path}")
        except Exception:
            # Happens if Playwright hasn't written the file yet
            logger.warning("Excel download path not available yet")

        return download
    
    def export_site_properties_pdf(self):
        """
        Trigger PDF export for Site Properties and return Download object.
        """
        logger.info("Exporting Site Properties - PDF")

        self.export_button.click()
        self.pdf_radio_button.click()
        
        # Listen for both the popup window and the file download
        # The download is triggered by clicking the Download button
        with self.page.expect_download() as download_info:
            with self.page.expect_popup() as popup_info:
                self.export_download_button.click() 

        popup_page = popup_info.value
        popup_page.close()

        download = download_info.value

        #Log where Playwright stored the file temporarily
        try:
            file_path = download.path()
            logger.info(f"PDF file downloaded to temporary path: {file_path}")
        except Exception:
            logger.warning("PDF download path not available yet")

        return download
    
    # Navigate to speed_distribution_graph
    def navigate_to_speed_distribution_graph(self):
        self.menu_analysis.hover()
        self.speed_distribution_graph_link.wait_for(state="visible", timeout=10000)
        self.speed_distribution_graph_link.click()

    def verify_speed_distribution_graph(self):
            """Verifies heading elements are visible on Speed Distribution Graph Page."""
            expect(self.heading_graph).to_be_visible()
            logger.info('Heading elements are visible on Speed Distribution Graph Page')


    #Helper function to help select all required fields in the dropdown in Speed Distribution Graph
    def select_by_index(self, index, value):
        """
        Index representation:
        0 = Filter Type
        1 = First dynamic dropdown (System / Owner)
        2 = Second dropdown (Site / All)
        3 = Third dropdown (Track / All)
        """

        dropdown = self.dropdowns.nth(index)

        current_value = dropdown.input_value() or ""
        if current_value.strip().lower() == value.strip().lower():
            return

        dropdown.click()

        # DevExtreme-safe: select by visible text in overlay
        overlay = self.page.locator(
            ".dx-overlay-content:visible"
        )
        #the above code returns a playwright locator that represents the active dropdown popup.
        # Scope is narrowed to just that popup
        #DevExtreme often keeps old overlays hidden in the DOM, so 'visible' is necessary
        # as Playwright may find: hidden dropdowns, previous dropdown instances.

        overlay.locator(
            f".dx-list-item:has-text('{value}')"
        ).first.click()


    def verify_speed_distribution_graph_filters(self):
        """Select all 4 dropdowns in order in Speed Distribution Graph Page"""

        self.select_by_index(0, "System/Site/Track")
        self.select_by_index(1, "BBT")
        self.select_by_index(2, "KWD")
        self.select_by_index(3, "Up")
        self.add_to_grid_btn.click()
        logger.info('System/Site/Track -> BBT -> KWD -> Up has been added to Grid')

        # ---------------- Scenario 2 ----------------
        self.select_by_index(0, "OOM")
        self.select_by_index(1, "All")  # System → Owner (handled)
        self.select_by_index(2, "All")
        self.select_by_index(3, "All")
        self.add_to_grid_btn.click()
        logger.info('OOM -> All -> All -> All has been added to Grid')

        # ---------------- Scenario 3 ----------------
        self.select_by_index(0, "Speed Board")
        self.select_by_index(1, "All")
        self.add_to_grid_btn.click()
        logger.info('Speed Board -> All has been added to Grid')

        self.assert_expected_filters_present()

    def assert_expected_filters_present(self):
        filter_type_cells = self.page.locator(
            "#selectedFiltersTable tr.dx-row.dx-data-row td:nth-child(2)"
        )

        expect(filter_type_cells).to_contain_text(
            [
                "System/Site/Track",
                "OOM",
                "Speed Board",
            ],
            timeout=10000
        )