from pages.base_page import BasePage
from playwright.sync_api import expect
import logging
import re
from datetime import datetime
from utils.helpers import export_simple_download
from utils.helpers import export_with_date_range

logger = logging.getLogger(__name__)


class DashboardPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        
        ################### Start of Navigation Locators ####################
        self.menu_dashboards = page.get_by_role("menuitem", name="Dashboards")
        self.rolling_stock_monitoring_link = page.get_by_role("link", name="Rolling Stock Monitoring")
        self.weather_monitoring_link = page.get_by_role("link", name="Weather Monitoring")
        self.management_overview_link = page.get_by_role("link", name="Management Overview")
        self.system_health_link = page.get_by_role("link", name="System Health & Fault Monitoring")
        self.system_health_dashboards_link = page.get_by_role("link", name="Dashboard")
        ################### End of Navigation Locators ######################
        
        ##################### Management Overview Page Locator Start######################
        # Overview of Alarms and Responses Times table 
        self.alarm_responses_table = page.locator("dx-data-grid#alarmResponseTimes")
        self.alarm_responses_rows = page.locator("#alarmResponseTimes tr.dx-data-row")
        self.first_row = page.locator(".dx-data-row[aria-rowindex='1']")

        # WIMS and Wayside Systems Operational Status
        self.bam_spindown = page.get_by_role("row", name="BAM spindown All All 0 0 0").get_by_label("spindown")

        # This finds the currently expanded (visible) master‑detail row and
        # then finds the dx‑data‑grid inside it.
        #not(.dx-state-invisible) -> this ensures: Only the row that's expanded (e.g., BAM) is selected.
        self.bam_detail_grid = page.locator("tr.dx-master-detail-row:not(.dx-state-invisible) dx-data-grid")

        #This gets all the actual data rows inside the BAM detail grid.
        # tbody - Targets data, not headers.
        #tr.dx-row.dx-data-row -> real rows containing values like KWD, MIN, PNS.
        self.bam_detail_rows = self.bam_detail_grid.locator("tbody tr.dx-row.dx-data-row")

        # Monthly Alarms by Severity 
        self.monthly_filter_button = page.locator(".monthly-alarms-severity-card .dx-button-text img[src*='filter_alt']")
        self.six_month_option = page.get_by_role("radio", name="6 months")
        self.twelve_month_option = page.get_by_text("12 Months")
        self.apply_filter_button = page.get_by_role("button", name="Apply")
        self.graph_footer = page.locator(".monthly-alarms-severity-card .graph-footer")

        # Weekly Alarms by Severity
        self.weekly_filter_button = page.locator(".weekly-alarms-operator-card .dx-button-text img[src*='filter_alt']")
        self.weekly_dd = page.locator(".graph-filter-modal-template .dx-texteditor-input")
        self.weekly_filters = page.locator("#dx-493bb844-85dc-40da-41aa-51232c468e88 .dx-item.dx-list-item")
        self.weekly_section = page.locator(".weekly-alarms-operator-card")
        
        # Export Locators
        self.export_button = page.locator("#downloadIcon1")
        self.excel_radio_button = page.get_by_role("radio", name="Excel")
        self.pdf_radio_button = page.get_by_role("radio", name="PDF")
        self.export_download_button = page.get_by_role("button", name="Download")
        self.export_success_popup = page.get_by_text("Export Completed")
        
        # Export date range button
        self.export_date_button = page.get_by_role("button").nth(3)
 
        # Export popup container
        self.export_popup = page.locator(".dx-overlay-content")
 
        # Start & End date buttons
        self.start_date_button = page.get_by_role("button", name="Select").first
        self.end_date_button = page.get_by_role("button", name="Select").nth(1)
 
        # Format radio buttons
        self.excel_radio = page.get_by_role("radio", name="Excel")
        self.pdf_radio = page.get_by_role("radio", name="PDF")
        # Overview of Alarms and Responses Times Section
        self.alarms_responses_times_section = page.get_by_label(" Overview of Alarms and Responses Times (Today)")
        #  Export button
        self.alarms_responses_times_pass_export_button = self.alarms_responses_times_section.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-16.btn-icon"
        ).nth(0)
        

        #################### End of Management Overview Page Locators ############
        ################# Rolling Stock Monitoring Page Locators Start ###########
        
        #  Headings
        self.heading_rolling_stock_monitoring = page.locator("text=Rolling Stock Monitoring")

        # Train Alarm Locators
        self.heading_train_alarm_alert_list = page.locator(".widget-title span", has_text="Train Alarm/Alert List")
        self.tal_rows = page.locator("#TAL24-RSD .dx-data-row")
        self.tal_no_data = page.locator("#TAL24-RSD .dx-datagrid-nodata")
        self.train_alarm_responses_rows = page.locator("#alarmResponseTimes tr.dx-data-row")
        self.first_row_train_alarm= self.tal_rows.first

        #  Monitoring
        self.monitoring_table = page.locator("dx-data-grid#MonitoringListOther")
        self.monitoring_rows = page.locator("#MonitoringListOther .dx-data-row")

        #  WIMS
        self.wims_section = self.page.locator("div:has-text('WIMS Processing')")
        self.status_items = {
            "WIMS Processing": page.locator("text=WIMS Processing"),
            "OSS Connectivity": page.locator("text=OSS Connectivity"),
            "TRIMS Connectivity": page.locator("text=TRIMS Connectivity"),
            "EQUIP Connectivity": page.locator("text=EQUIP Connectivity"),
            "Email Services": page.locator("text=Email Services"),
            "SMS Services": page.locator("text=SMS Services"),
            "Database Performance": page.locator("text=Database Performance"),
        }    
        ################# Rolling Stock Monitoring Page Locators End ######
        
        ############# System Health and Fault Monitoring - Dashboard & System faults Locators Start #######

        #Toggle button for Summary <-> Detailed view
        self.summary_toggle = page.locator("#switchTable")
        # Wayside System Health 
        self.wayside_system_health_table = page.locator(".wayside-system-health-card")
        self.aoa_dropdown = page.get_by_role("gridcell", name="AoA spindown").get_by_label("spindown")
        self.aoa_detail_grid = page.locator("tr.dx-master-detail-row:not(.dx-state-invisible) dx-data-grid")
        self.aoa_detail_rows = self.aoa_detail_grid.locator("tbody tr.dx-row.dx-data-row")

        # AV Report icon (image inside first column) Alarm Verification List
        self.av_report_icon = page.locator("tr.dx-data-row td[aria-colindex='1'] img")
        
        #system_faults
        self.system_health_menu = page.get_by_role("link", name="System Health & Fault Monitoring")
        self.system_faults_link = page.get_by_role("link", name="System Faults")
        self.rows = page.locator("tr.dx-data-row")
        ############# System Health and Fault Monitoring - Dashboard & System faults Locators End #######

        ################# Weather Monitoring Page Locators Start ##########
        
        #  Headings
        self.weather_monitoring_heading = page.locator("text=Weather Monitoring")

        # weatherStationStatus
        self.weather_station_status = page.locator("#weatherStationStatus")
        self.weather_station_status_rows = page.locator("#weatherStationStatus tr.dx-row.dx-data-row")
        self.no_data = page.locator("#weatherStationStatus .dx-datagrid-nodata")
        
        # Weather Data Table Locators
        self.weather_data_section = page.locator(".weather-data-table")
        self.weather_data_table = page.locator("#weatherData")
        self.weather_data_rows = page.locator("#weatherData tr.dx-row.dx-data-row")
        self.weather_data_no_data = page.locator("#weatherData .dx-datagrid-nodata")
    ###################### Weather Monitoring Page Locators End ##########

    ################# Management Overview Page Start #####################

    # Navigate to management_overview
    def navigate_to_management_overview(self):
         """Helps to navigate to Management Overview Page"""
         self.menu_dashboards.hover()
         self.management_overview_link.wait_for(state="visible", timeout=10000)
         self.management_overview_link.click()
        """Helps to navigate to Management Overview Page"""
        self.menu_dashboards.hover()
        self.management_overview_link.wait_for(state="visible", timeout=10000)
        self.management_overview_link.click()


    def verify_alarms_and_responses_times_table(self):
        """Verifies Overview of Alarms and Responses Times (Today) table's functionality."""

        #Verify that the table is visible
        expect(self.alarm_responses_table).to_be_visible()
        #Verify that the table should have at least one row present
        expect(self.alarm_responses_rows.first).to_be_visible(timeout=5000)

        # Wait for new page before clicking
        with self.page.expect_popup() as alarm_page_info:
            # Double clicking first row to open a new window.
            self.first_row.dblclick()
        alarm_page = alarm_page_info.value
        # Correct validation
        expect(alarm_page).to_have_url(re.compile("https://inmumvm26325635/wims/pop-up/alarm-alert-details*"))  # Uses regex because URL contains dynamic values
        alarm_page.close()

    #  Open Export Popup on Overview of Alarms and Responses Times table
    def open_export_popup(self):
        self.export_date_button.wait_for(state="visible", timeout=20000)
        self.export_date_button.click()
        self.export_popup.last.wait_for(state="visible", timeout=20000)

    def prepare_calendar_for_helper(self):

        start_button = self.export_popup.get_by_role("button", name="Select").first
        start_button.wait_for(state="visible", timeout=20000)

        start_button.click(force=True)

        calendar = self.export_popup.locator(".dx-calendar").last
        calendar.wait_for(state="visible", timeout=20000)

        self.page.keyboard.press("Escape")

    # Open Export popup
    def open_alarms_and_responses_times_table_export_popup(self):

        self.alarms_responses_times_pass_export_button.hover()
        self.alarms_responses_times_pass_export_button.click()
        self.export_popup = self.page.locator(".dx-overlay-content").last
        self.export_popup.wait_for(state="visible", timeout=20000)

    # Prepare calendar
    def prepare_calendar_for_helper(self):

        start_button = self.export_popup.get_by_role("button", name="Select").first
        start_button.wait_for(state="visible", timeout=20000)
        # Activate calendar once
        start_button.click(force=True)
        #  WAIT calendar INSIDE popup
        calendar = self.export_popup.locator(".dx-calendar").last
        calendar.wait_for(state="visible", timeout=20000)
        
        # close it 
        self.page.keyboard.press("Escape")

        # small stabilization delay
        self.page.wait_for_timeout(500)

    def expand_bam(self):
        """Expands BAM master-detail row with explicit wait."""
        self.bam_spindown.click()
        self.bam_detail_grid.wait_for(state="visible", timeout=5000)

    def get_bam_detail_sites(self):
        """Returns list of Site values from BAM detail grid."""

        #wait until data rows load
        expect(self.bam_detail_rows).to_have_count(1, timeout=5000)

        sites = self.bam_detail_rows.locator('td[aria-colindex="5"] span.tooltip-wrapper').all_text_contents()

        return [s.strip() for s in sites]

    def verify_sites_in_bam(self, expected_sites):
        """Verifies BAM detail grid contains ONLY expected sites. Example: expected_sites=["KWD"]"""
        self.expand_bam()
        actual_sites = self.get_bam_detail_sites()

        assert actual_sites == expected_sites, (
            f"Expected sites {expected_sites}, but found {actual_sites}"
        )
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
    

    def open_monthly_alarm_filter(self):
        self.monthly_filter_button.click()
        expect(self.six_month_option).to_be_visible(timeout=5000)

    def apply_month_filter(self, months: int):
        """Helper method to apply either 6 month or 12 month filter in Monthly Alarms by Severity"""
        self.open_monthly_alarm_filter()

        if months == 6:
            self.six_month_option.click()
        elif months == 12:
            self.twelve_month_option.click()
        else:
            raise ValueError("Only 6 or 12 months supported")

        self.apply_filter_button.click()

        #wait for chart to refresh (footer text updates)
        expect(self.graph_footer.first).to_be_visible(timeout=5000)

    def get_monthly_alarm_date_range(self) -> str:
        return self.graph_footer.first.inner_text().strip()

    def verify_monthly_alarm_filters(self, months: int):
        """Verifies Monthly Alarms by Severity table"""
        self.apply_month_filter(months)
        date_range = self.get_monthly_alarm_date_range()

        assert " - " in date_range, "Invalid date range format"

        start_str, end_str = [d.strip() for d in date_range.split(" - ")]

        # Convert "Dec 25" → datetime
        start_date = datetime.strptime(start_str, "%b %y")
        end_date = datetime.strptime(end_str, "%b %y")

        # Calculate month difference
        diff_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        #Assertion
        assert diff_months == months - 1, (
        f"Expected {months} month range, but got {diff_months + 1}"
        )
    def get_week_label_count(self):
        return self.weekly_section.locator(
            ".graph-group.first g.dxc-arg-elements text"
        ).count()

    def verify_weekly_alarm_filters(self, weeks: int):
        """Verifies Weekly Alarms by Operator table"""
        initial_count = self.get_week_label_count()

        self.weekly_filter_button.click()
        self.weekly_dd.click()
        self.page.get_by_role("option", name=f"{weeks} weeks").click()
        self.apply_filter_button.click()

        # Wait until count stabilizes (chart re-render)
        self.page.wait_for_timeout(1000)

        updated_count = self.get_week_label_count()


        # Wait until count stabilizes (chart re-render)
        self.page.wait_for_timeout(1000)

        updated_count = self.get_week_label_count()

        assert updated_count > 0, "Chart did not render any week labels"
        assert updated_count <= weeks, (
            f"Chart label count {updated_count} exceeds selected weeks {weeks}"
        )
################# Management Overview Page End #####################


################# Rolling Stock Monitoring Page Start ########################
        # Navigation
    def navigate_to_rolling_stock_monitoring(self):
        logger.info("Navigating to Rolling Stock Monitoring")
        self.menu_dashboards.hover()
        self.rolling_stock_monitoring_link.wait_for(state="visible", timeout=10000)
        self.rolling_stock_monitoring_link.click()
        logger.info("Navigation completed")

    # Page Verification

    def verify_rolling_stock_monitoring(self):
        logger.info("Verifying Rolling Stock Monitoring page")
        expect(self.heading_rolling_stock_monitoring.first).to_be_visible()

    def verify_weather_monitoring(self):
        logger.info("Verifying Weather Monitoring page")
        expect(self.weather_monitoring_heading.first).to_be_visible()

    #  Train Alarm Table
    def verify_train_alarm_alert_list_table(self):
        logger.info("Verifying Train Alarm/Alert List table")

    # Verify section is visible
        expect(self.heading_train_alarm_alert_list.first).to_be_visible(timeout=5000)
    # Wait for table rows to load
        expect(self.tal_rows.first).to_be_visible(timeout=10000)
    # Handle popup on double-click
        with self.page.expect_popup() as train_alarm_page_info:
            self.first_row_train_alarm.dblclick()
        train_alarm_page = train_alarm_page_info.value
    # Validate URL (handles dynamic values)
        expect(train_alarm_page).to_have_url(re.compile(r"https://inmumvm26325635/wims/pop-up/alarm-alert-details.*"))
        train_alarm_page.close()
        
    #  Monitoring Table
    def verify_monitoring_list_table(self):
        logger.info("Verifying Monitoring List table")
        expect(self.monitoring_table.first).to_be_visible()

    #  WIMS
    def verify_wims_status_header_visible(self):
        
        #  Wait for stable WIMS item instead of header
        logger.info("Waiting for WIMS section")
        self.page.wait_for_selector("text=WIMS Processing", timeout=10000)
        logger.info("WIMS section visible")

        expect(self.wims_section.first).to_be_visible()

    def verify_available_wims_status_items_visible(self):
        logger.info("Verifying WIMS items")
    def verify_wims_processing_tooltip(self):
        logger.info("Hover on WIMS Processing")
        self.status_items["WIMS Processing"].hover()

    def verify_oss_connectivity_tooltip(self):
        logger.info("Hover on OSS Connectivity")
        self.status_items["OSS Connectivity"].hover()

    def verify_equip_connectivity_tooltip(self):
        logger.info("Hover on EQUIP Connectivity")
        self.status_items["EQUIP Connectivity"].hover()
    
    ################## Rolling Stock Monitoring Page End #######################

    ####### System Health and Fault Monitoring Dashboard - Dashboard Page Start####

    def navigate_to_system_health_dashboard(self):
        """Navigates to System Health and Fault Monitoring Dashboard - Dashboard Page"""
        self.menu_dashboards.hover()
        self.system_health_link.wait_for(state="visible", timeout=10000)
        self.system_health_link.hover()
        self.system_health_dashboards_link.wait_for(state="visible", timeout=10000)
        self.system_health_dashboards_link.click()

    def expand_aoa(self):
        """Expands AoA master-detail row with explicit wait."""
        self.aoa_dropdown.click()
        self.aoa_detail_grid.wait_for(state="visible", timeout=5000)

    def get_aoa_detail_sites(self):
        """Returns list of Site values from AoA detail grid."""

        # wait until data rows load
        expect(self.aoa_detail_rows).to_have_count(1, timeout=5000)

        sites = self.aoa_detail_rows.locator('td[aria-colindex="3"] span.tooltip-wrapper').all_text_contents()

        return [s.strip() for s in sites]

    def verify_wayside_system_health(self,expected_sites):
        """Verifies Wayside System Health table - Summary View(default selected)"""
        expect(self.wayside_system_health_table).to_be_visible()
        self.expand_aoa()
        actual_sites = self.get_aoa_detail_sites()
        print(actual_sites)
        assert actual_sites == expected_sites, (
            f"Expected sites {expected_sites}, but found {actual_sites}"
        )

    def click_summary_toggle(self):
        """Click Summary ↔ Detailed toggle"""

        self.summary_toggle.wait_for(state="visible")

        # capture state before click
        state_before = self.summary_toggle.get_attribute("aria-pressed")
        logger.info(f"Toggle state before click: {state_before}")

        self.summary_toggle.click()

        # capture state after click
        state_after = self.summary_toggle.get_attribute("aria-pressed")
        logger.info(f"Toggle state after click: {state_after}")

        assert state_before != state_after, "Toggle state did NOT change!"


    def verify_wayside_system_health_detailed(self,expected_sites):
        self.click_summary_toggle()
        self.verify_wayside_system_health(expected_sites)

    def click_av_report(self):
        """Click AV Report icon and close the report"""
 
        # wait for rows
        self.page.wait_for_selector("tr.dx-data-row", timeout=60000)
 
        # handle new tab
        with self.page.context.expect_page() as new_page_info:
            self.av_report_icon.first.click()
 
        av_report_page = new_page_info.value
        av_report_page.wait_for_load_state()
 
        logger.info("AV Report opened")
 
        # wait if needed (optional)
        av_report_page.wait_for_timeout(3000)
 
        expect(av_report_page).to_have_url(re.compile("https://inmumvm26325635/wims/pop-up/alarm-verification-report*"))  # Uses regex because URL contains dynamic values
        av_report_page.close()
        logger.info("AV Report closed successfully")

    #  Open Export Popup on Alarms and verification table
    def open_export_popup(self):
        self.export_date_button.wait_for(state="visible", timeout=20000)
        self.export_date_button.click()
        self.export_popup.last.wait_for(state="visible", timeout=20000)

    def prepare_calendar_for_system_dafault(self):

        start_button = self.export_popup.get_by_role("button", name="Select").first
        start_button.wait_for(state="visible", timeout=20000)

        start_button.click(force=True)

        calendar = self.export_popup.locator(".dx-calendar").last
        calendar.wait_for(state="visible", timeout=20000)

        self.page.keyboard.press("Escape")

    #  STEP 1: Open Export popup
    def open_alarm_verification_list_export_popup(self):

        # hover section (needed for DevExtreme)
        self.alarms_verification_list_section.hover()

        self.alarms_verification_list_section.hover()
        self.alarms_verification_list_section.click()

        #  store CURRENT popup
        self.export_popup = self.page.locator(".dx-overlay-content").last
        self.export_popup.wait_for(state="visible", timeout=20000)

    #  STEP 2: Prepare calendar 
    def prepare_calendar_for_system_default(self):

        # USE POPUP CONTEXT
        start_button = self.export_popup.get_by_role("button", name="Select").first

        start_button.wait_for(state="visible", timeout=20000)

        # Activate calendar once
        start_button.click(force=True)

        #  WAIT calendar INSIDE popup
        calendar = self.export_popup.locator(".dx-calendar").last
        calendar.wait_for(state="visible", timeout=20000)
        
        # close it 
        self.page.keyboard.press("Escape")

        # small stabilization delay
        self.page.wait_for_timeout(500)
    
        
    ####### system-faults 

    def navigate_to_system_faults(self):
        """Navigate to System Faults page"""
 
        self.menu_dashboards.hover()
        self.system_health_menu.wait_for(state="visible", timeout=20000)
        self.system_health_menu.hover()
 
        self.system_faults_link.wait_for(state="visible", timeout=20000)
        self.system_faults_link.click()
 
        logger.info("Navigated to System Faults page")

    def verify_system_faults_loaded(self):
        """Verify System Faults table is loaded"""
        expect(self.rows.first).to_be_visible()
        logger.info("System Faults table loaded successfully")


####### System Health and Fault Monitoring Dashboard - Dashboard Page End ####

################### Weather Monitoring Page Start ###########################
    
    # Navigate to weather monitoring page
    def navigate_to_weather_monitoring(self):
        logger.info("Navigating to Weather Monitoring")
        self.menu_dashboards.hover()
        self.weather_monitoring_link.wait_for(state="visible", timeout=20000)
        self.weather_monitoring_link.click()

    
    #  Weather Station Status Table
    
    def verify_weather_station_status_table(self):
        logger.info("Verifying weather station status table")   

        # Ensure table is visible
        expect(self.weather_station_status).to_be_visible()

        # Get first row reference
        row = self.weather_station_status_rows.first

        # Wait until row is attached to DOM (important for DevExtreme)
        row.wait_for(state="attached", timeout=10000)

        # Scroll into view (grid is scrollable)
        row.scroll_into_view_if_needed()

        # Now safely check visibility
        expect(row).to_be_visible()

        logger.info(" Weather Station Status table verified successfully")
    
    
    # weather data table
    
    def verify_weather_data_table(self):
        logger.info("Verifying Weather Data table")
        # section visible (outer container)
        expect(self.weather_data_section).to_be_visible()
        # table visible
        expect(self.weather_data_table).to_be_visible()
        # reference first row
        row = self.weather_data_rows.first
        try:
        # wait for row (DevExtreme fix)
            row.wait_for(state="attached", timeout=15000)

        # scroll into view (grid has scroll)
            row.scroll_into_view_if_needed()

        # verify visible
            expect(row).to_be_visible()

            logger.info("Weather Data table rows are visible")

        except:
            logger.info(" No rows found, verifying No Data message")

            expect(self.weather_data_no_data).to_be_visible()
################## Weather Monitoring Page End ###########################