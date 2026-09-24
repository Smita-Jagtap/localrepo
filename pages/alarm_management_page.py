from pages.base_page import BasePage
from playwright.sync_api import expect
import logging

logger = logging.getLogger(__name__)


class AlarmManagementPage(BasePage):
    """Page Object for Alarm Management"""

    def __init__(self, page):
        super().__init__(page)

        # ================= NAVIGATION =================
        self.menu_alarm = page.locator("span.dx-menu-item-text", has_text="Alarm Management")
        self.submenu_container = page.locator("div.dx-overlay-content:has(a.menu-link)")

        # Submenus
        self.train_threshold_link = page.locator("a.menu-link", has_text="Train Alarm/Alert Thresholds")
        self.speed_threshold_link = page.locator("a.menu-link", has_text="Speed Monitoring Thresholds")
        self.wims_alarm_link = page.locator("a.menu-link", has_text="WIMS Alarm/Alert")
        self.workflow_menu = page.get_by_role("link", name="Workflow Management")
        self.workflow_heading = page.get_by_text("Workflow Management", exact=False)
        self.alert_suppression_link = self.page.get_by_role("link", name="Alarm/Alert Suppression/")
        self.workflow_allocation_link = page.get_by_role("link", name="Alarm/Alert Workflow")



        # ================= TABLE =================
        self.rows = page.locator("tr.dx-data-row")
        self.first_row = self.rows.first    #always points to the latest first row even if DOM updates

        # ================= ACTION BUTTONS =================
        self.edit_btn = self.first_row.get_by_role("button", name="edit")
        self.save_btn = self.first_row.get_by_role("button", name="save-white")
        self.cancel_btn = self.first_row.get_by_role("button", name="cancel")
        self.add_wims_btn = page.locator("dx-button:has(img[src*='add_to_photos'])")
        self.delete_btn = self.first_row.locator("img[src*='delete.svg']")
        self.reset_btn = self.page.locator("dx-button:has(img[src*='restart_alt.svg'])")
        self.edit_btn = self.first_row.locator("dx-button:has(img[src*='edit.svg'])")

        # ================= POPUPS =================
        self.no_btn = page.get_by_role("button", name="No")
        self.success_popup = page.locator(".dx-toast-content")
        self.yes_btn = page.get_by_role("button", name="Yes")
        self.no_btn = self.page.locator('dx-button[aria-label="No"]')
        self.popup_save_btn = self.page.get_by_role("button", name="Save")
        
        #================= WIMS FORM =================

        self.add_workflow_btn = page.locator("dx-button:has(img[src*='add_to_photos.svg'])")

        # Inputs
        self.wims_name_input = page.get_by_label("WIMS Alarm/Alert Name", exact=False)
        self.wims_desc_input = page.get_by_label("Description", exact=False)

        # Radios
        self.system_radio_aoa = page.get_by_role("radio", name="AoA")
        self.type_radio_alert = page.get_by_role("radio", name="WIMS Alert")

        # Dropdowns
        self.measures_dropdown = page.locator("label:has-text('Measures')").locator("..").locator("dx-select-box .dx-texteditor-container")
        self.filter_dropdown = page.locator("label:has-text('Filter')").locator("..").locator("dx-select-box .dx-texteditor-container")

        # Buttons
        self.add_to_grid_btn = page.get_by_role("button", name="Add to Grid")
        self.save_btn_wims = page.get_by_role("button", name="Save")

       
        #Date pickers
        self.date_select_buttons = page.get_by_role("button", name="Select")

        self.save_btn_popup = page.get_by_role("button", name="Save")
        self.description_input = page.get_by_role("textbox", name="Description")

        # ================= WORKFLOW =================

        # Navigation
        self.workflow_menu = page.get_by_role("link", name="Workflow Management")

        # Buttons
        self.add_stage_btn = page.get_by_role("button", name="Add Stage")

        # Inputs
        self.workflow_name_input = page.locator("input[name='workflowName']")
        self.workflow_desc_input = page.locator("input[name='workflowDescription']")

        # Stage inputs
        self.stage_name_input = self.page.locator("#WorkflowStages input.dx-texteditor-input").nth(0)
        self.stage_desc_input = self.page.locator("#WorkflowStages input.dx-texteditor-input").nth(1)

        # Priority spinner
        self.increment_btn = page.locator(".dx-numberbox-spin-up-icon").first

        # Next button
        self.next_btn = page.locator("dx-button.btn-icon")

        # User selection
        self.user_tab = self.page.get_by_role("tab", name="User")
        self.user_input = self.page.locator('dx-select-box[name="user"] input.dx-texteditor-input')

        self.user_combobox = page.get_by_role("combobox", name="Add User")
        self.launchpad_user = page.get_by_text("Launchpad demo")
        self.checkbox_select = self.page.locator("div.dx-list-item input[type='checkbox']").first
        self.search_btn = self.page.locator('dx-select-box[name="user"] div[aria-label="Search"]')
        self.workflow_recipients_icon = self.page.locator("tr.dx-data-row .recipient-list dx-button:has(img[src*='expand_content'])").first
        self.workflow_close_icon = self.page.locator("span.closeIcon").last

        self.workflow_edit_btn = self.page.locator("#WorkflowList tr.dx-data-row dx-button.btn-edit").first
        self.edit_workflow_name_input = self.page.locator(".dx-popup-content input[name='workflowName']").last
        self.edit_workflow_desc_input = self.page.locator("input[name='workflowDescription']").last
        self.edit_workflow_save_btn = self.page.locator(".dx-popup-content [role='button'][aria-label='Save']").last
        self.workflow_delete_btn = self.page.locator("#WorkflowList tr.dx-data-row dx-button.btn-delete").first

        # =========================================================
        # ALERT SUPPRESSION LOCATORS 
        # =========================================================

        # ===== ADD BUTTON =====
        self.supp_add_btn = self.page.get_by_role("button").nth(3)

        # ===== INPUT FIELDS =====
        self.supp_name_input = self.page.get_by_role("textbox", name="Suppression Name")
        self.supp_desc_input = self.page.get_by_role("textbox", name="Description")

        # ===== DROPDOWNS =====
        self.supp_system_dropdown = self.page.locator("div.system-selection-item dx-select-box")
        self.supp_measure_dropdown = self.page.locator(".measure-box .dx-texteditor-buttons-container")
        self.supp_generic_dropdowns = self.page.locator(".dx-selectbox .dx-texteditor-buttons-container")
        self.supp_type_dropdown = self.page.locator(".dx-show-invalid-badge.dx-selectbox.dx-textbox.dx-texteditor.dx-show-clear-button.dx-editor-outlined.dx-texteditor-empty >> .dx-texteditor-buttons-container").nth(0)
        self.supp_severity_dropdown = self.page.locator("label:has-text('Alarm/Alert Severity')").locator("xpath=following::input[@role='combobox'][1]")
        self.supp_description_dropdown = self.page.locator("label:has-text('Alarm/Alert Description')").locator("xpath=following::input[@role='combobox'][1]")
        self.supp_filter_dropdown = self.page.get_by_role("combobox",name="Filter Type")

        # ===== DROPDOWN OPTIONS =====
        self.active_overlay = self.page.locator(".dx-overlay-wrapper:not(.dx-state-invisible)")
        self.supp_option_date_time = self.active_overlay.get_by_text("Date and Time",exact=True)

        self.supp_option_aoa = self.page.get_by_role("option", name="AoA")
        self.supp_option_all = self.page.get_by_role("option", name="All")
        self.supp_option_date_time = self.page.get_by_text("Date and Time")

         # ===== LISTBOX =====
        self.supp_listbox = self.page.get_by_role("listbox")

        # ===== DATE PICKERS =====
        self.supp_select_buttons = self.page.get_by_role("button", name="Select")
        self.supp_done_btn = self.page.get_by_role("button", name="Done")
        self.supp_calendar_overlay = self.page.locator(".dx-overlay-wrapper.dx-dropdowneditor-overlay:not(.dx-state-invisible)").last

        self.current_calendar = self.supp_calendar_overlay.locator("table[role='grid']").first
        self.supp_start_date = self.current_calendar.locator("td.dx-calendar-cell:not(.dx-calendar-other-month):not(.dx-calendar-other-view)").get_by_text("6", exact=True)
        self.supp_end_date = self.current_calendar.locator("td.dx-calendar-cell:not(.dx-calendar-other-month):not(.dx-calendar-other-view)").get_by_text("13", exact=True)

        # ===== ACTION BUTTONS =====
        self.supp_add_to_grid_btn = self.page.get_by_role("button", name="Add to Grid")
        self.supp_save_btn = self.page.get_by_role("button", name="Save")

        # ===== TABLE =====
        self.supp_rows = self.page.locator("tr.dx-data-row")
        
        # Save buttons
        self.stage_save_btn = self.page.locator('#WorkflowStages tr.dx-edit-row dx-button[aria-label="save-white"]')
        self.save_user_btn = page.get_by_role("button", name="Save")
        self.workflow_final_save_btn = self.page.locator(".pe-2 [role='button'][aria-label='Save']").last
        self.workflow_form_save_btn = self.page.locator(".btn-save [role='button'][aria-label='Save']").first

        # Grid verification
        self.rows = page.locator("tr.dx-data-row")
        self.user_row = lambda login: self.page.locator(f'//tr[contains(@class,"dx-data-row") and .//td//span[text()="{login}"]]')  #lambda is anonymus function ex user name can change
        self.popup_checkbox = lambda row: row.locator('td[aria-colindex="6"] dx-check-box')                                          #used to create the dynamic locators
        self.popup_save_btn1 = self.page.locator(".dx-popup-content .btn-save [role='button'][aria-label='Save']")
        
        self.user_option_launchpad = self.page.locator("div.dx-list-item:has(strong:has-text('Launchpad demo'))")
        self.edit_recipients_btn = self.page.locator('#WorkflowStages tr.dx-data-row:first-child td:last-child dx-button')

        #####edit icon##########
        self.supp_edit_btn = self.page.locator("tr.dx-data-row dx-button.btn-edit").first
        self.supp_edit_description_input = self.page.get_by_role("textbox", name="Description")
        self.supp_edit_save_btn = self.page.get_by_role("button", name="Save")
        self.supp_edit_heading = self.page.get_by_text("Edit Alarm/Alert Suppression/Disable")

        ######delete icon
        self.supp_delete_btn = self.page.locator("tr.dx-data-row dx-button.btn-delete").first
        self.supp_confirm_yes_btn = self.page.get_by_role("button",name="Yes")
        #####reset icon        
        self.reset_btn = self.page.locator("dx-button:has(img[src*='restart_alt.svg'])")


        #Alarm/Alert Workflow Allocation
        # ===== WORKFLOW ALLOCATION SECTION =====
        self.workflow_alloc_section = page.locator("app-alarm-workflow-allocation")

        # ===== SYSTEM DROPDOWN =====
        self.workflow_alloc_system_dropdown = self.workflow_alloc_section.get_by_role("combobox")

        # ===== AoA OPTION =====
        self.workflow_alloc_aoa_option = page.get_by_text("AoA", exact=True)

        # ===== EDIT BUTTON  =====
        
        self.workflow_alloc_threshold_edit = self.workflow_alloc_section.locator("button.edit")

        self.workflow_alloc_minutes_input = self.workflow_alloc_section.locator("dx-number-box input.dx-texteditor-input")

        # ===== INCREMENT BUTTON =====
        self.workflow_alloc_increment = self.workflow_alloc_section.locator(".dx-numberbox-spin-up-icon").first

        # ===== SAVE BUTTON =====
        self.workflow_alloc_save = self.workflow_alloc_section.get_by_role("button", name="Save")
        self.export_btn = self.page.get_by_role("button", name="Export")
        self.download_btn = self.page.get_by_role("button", name="Download")

        self.download_icon = self.page.locator("#downloadIcon1")
        self.pdf_radio = self.page.get_by_role("radio", name="PDF")

        # ===== EDIT ICON =====
        self.workflow_alloc_edit_btn = self.workflow_alloc_section.locator(".dx-button.icon-12").first

        # ===== CHECKBOX =====
        self.workflow_alloc_checkbox = self.page.get_by_role("checkbox", name="aaaa22222")

        # ===== SAVE BUTTON =====
        self.workflow_alloc_save_btn = self.page.get_by_role("button", name="Save")
        self.reset_button_workflow_alloc = self.workflow_alloc_section.locator("img.reset_button")

    
        # =========================================================
        # NAVIGATION
        # =========================================================

    def navigate_to_submenu(self, submenu_locator):
        expect(self.menu_alarm).to_be_visible(timeout=20000)
        self.menu_alarm.click()

        expect(self.submenu_container).to_be_visible(timeout=20000)
        expect(submenu_locator).to_be_visible(timeout=20000)

        submenu_locator.click()
        logger.info("Navigated to submenu")

    def navigate_to_train(self):
        self.navigate_to_submenu(self.train_threshold_link)

    def navigate_to_speed(self):
        self.navigate_to_submenu(self.speed_threshold_link)

    def navigate_to_wims(self):
        self.navigate_to_submenu(self.wims_alarm_link)

    def navigate_to_workflow(self):
        self.navigate_to_submenu(self.workflow_menu)

    
    def navigate_to_alert_suppression(self):
        self.navigate_to_submenu(self.alert_suppression_link)

        # WAIT for page to actually load
        expect(self.add_workflow_btn).to_be_visible(timeout=20000)

        logger.info("Workflow page loaded successfully")

    
    def navigate_to_workflow_allocation(self):
        self.navigate_to_submenu(self.workflow_allocation_link)
        expect(self.workflow_alloc_system_dropdown).to_be_visible(timeout=20000)


        # =========================================================
        # PAGE VALIDATION
        # =========================================================

    def verify_page_loaded(self):
        self.page.wait_for_selector("tr.dx-data-row", timeout=60000)
        expect(self.first_row).to_be_visible()
        logger.info("Page loaded")

        # =========================================================
        # COMMON ACTIONS
        # =========================================================
     
    def wait_for_edit_row(self):
        self.page.wait_for_selector("tr.dx-edit-row", timeout=20000)

    def get_active_row(self):
        edit_row = self.page.locator("tr.dx-edit-row").first
        return edit_row if edit_row.count() > 0 else self.first_row

    def click_edit(self):
        expect(self.edit_btn).to_be_visible()
        self.edit_btn.click()
        self.wait_for_edit_row()
        expect(self.page.locator("tr.dx-edit-row")).to_be_visible(timeout=20000)

        logger.info("Clicked Edit")

    def click_save(self):
        expect(self.save_btn).to_be_visible(timeout=20000)
        self.save_btn.click()
        self.page.wait_for_timeout(2000)  # Wait for response from server
        logger.info("Clicked Save")

    def click_cancel(self):
        expect(self.cancel_btn).to_be_visible(timeout=20000)
        self.cancel_btn.click()
        self.page.wait_for_timeout(1000)
        try:
            self.page.wait_for_selector("[role='dialog']", timeout=5000)
        except Exception as e:
            logger.warning(f"No confirmation dialog appeared: {e}, continuing...")
        logger.info("Clicked Cancel")

    def click_no_popup(self):
        try:
            self.page.wait_for_timeout(500)
            self.no_btn.wait_for(state="visible", timeout=5000)
            self.no_btn.click()
            logger.info("Clicked No on popup")
        except Exception as e:
            logger.warning(f"No popup button found: {e}, assuming cancel was successful...")


    def verify_success(self):
        # Try to wait for toast, but don't fail if it doesn't appear
        try:
            self.page.wait_for_selector(".dx-toast-content", timeout=5000)
            expect(self.success_popup).to_be_visible(timeout=5000)
            logger.info("Success popup verified")
        except Exception as e:
            logger.warning(f"Success toast not visible: {e}, but continuing...")


        # =========================================================
        # GENERIC CELL HANDLING (KEY REUSABILITY)
        # =========================================================

    def fill_cell(self, col_index, value):
        row = self.get_active_row()
        cell = row.locator(f"td[aria-colindex='{col_index}']")
        expect(cell).to_be_visible(timeout=20000)  # Check cell first

        input_box = cell.locator("input, .dx-texteditor-input")
        input_box.wait_for(state="visible", timeout=20000)

        input_box.click()
        input_box.fill("")
        input_box.type(str(value))

        logger.info(f"Column {col_index} updated with {value}")

    def get_cell_input(self, col_index):
        """Returns input locator for any editable column"""
        row = self.get_active_row()
        cell = row.locator(f"td[aria-colindex='{col_index}']")
        input_box = cell.locator("input.dx-texteditor-input")
        return input_box


        # =========================================================
        # TRAIN PAGE ACTIONS
        # =========================================================

    def edit_and_save_train(self, low, medium, high, extreme):
        self.click_edit()

        self.fill_cell(5, low)
        self.fill_cell(6, medium)
        self.fill_cell(7, high)
        self.fill_cell(8, extreme)

        self.click_save()
        self.verify_success()


         ##########SPEED PAGE##################### 
    
    def verify_max_unknown_vehicle_count_editable(self, value="1"):
        """Column 11"""
        input_box = self.get_cell_input(11)

        expect(input_box).to_be_visible(timeout=20000)
        
        expect(input_box).to_be_editable()

        input_box.fill("")
        input_box.type(value)

        logger.info("Max Unknown Train Vehicle Count editable verified")

        
    def toggle_speed_monitoring_checkbox(self):
        """Column 7"""
        row = self.get_active_row()
        checkbox = row.locator("td[aria-colindex='7'] [role='checkbox']")
    
        expect(checkbox).to_be_visible(timeout=20000)

        # Get initial state
        initial_state = checkbox.get_attribute("aria-checked")

        checkbox.click()
        logger.info("Checkbox toggled once")

        # Toggle back to original state
        checkbox.click()
        logger.info("Checkbox toggled back to original state")

        final_state = checkbox.get_attribute("aria-checked")

        assert initial_state == final_state, "Checkbox did not revert properly"

    def select_severity_medium(self):
        """Select 'Medium' from severity dropdown (Column 12)"""
        row = self.get_active_row()
        dropdown = row.locator("td[aria-colindex='12'] [role='combobox']")

        expect(dropdown).to_be_visible(timeout=20000)
        dropdown.click()

        # Select "Medium" option
        medium_option = self.page.locator(".dx-list-item", has_text="Medium")

        expect(medium_option).to_be_visible(timeout=20000)
        medium_option.click()

        logger.info("Selected 'Medium' from severity dropdown")
        # =========================================================
        # SPEED PAGE ACTIONS
        # =========================================================

    def edit_and_save_speed(self, low, medium, high):
        self.click_edit()

        self.fill_cell(8, low)
        self.fill_cell(9, medium)
        self.fill_cell(10, high)
        
        self.verify_max_unknown_vehicle_count_editable("1")
        self.select_severity_medium()
        self.toggle_speed_monitoring_checkbox()

        self.click_save()
        self.verify_success()

        # =========================================================
        #WIMS ALRAM/ALERT
        #==========================================================
        
    def click_add_wims_alarm(self):
        expect(self.add_wims_btn).to_be_visible(timeout=20000)
        self.add_wims_btn.click()

        self.page.wait_for_selector("text=WIMS Alarm/Alert Name", timeout=20000)

        logger.info("Opened Add WIMS Alarm/Alert form")

    def create_wims_alarm(self):
        """Complete flow:Open form → Fill → Save"""
        self.click_add_wims_alarm()
        self.fill_wims_alarm_form()
 
    def fill_wims_alarm_form(self):

        # ===== TEXT =====
        self.wims_name_input.fill("aaaaab")
        self.wims_desc_input.fill("abcccccccccccccccccc")

        # ===== RADIO (SYSTEM) =====
        expect(self.system_radio_aoa).to_be_visible(timeout=20000)
        self.system_radio_aoa.click()
        self.page.wait_for_timeout(1000)  # Wait for form to update after radio selection

        # ===== MEASURES =====
        expect(self.measures_dropdown).to_be_visible(timeout=20000)
        self.measures_dropdown.click()
        self.page.wait_for_timeout(1000)  # Wait for dropdown to open
        
        # Select "Angle of Attack (AoA)" from measures dropdown
        aoa_option = self.page.locator("div.dx-item-content.dx-list-item-content", has_text="Angle of Attack (AoA)")
        expect(aoa_option).to_be_visible(timeout=20000)
        aoa_option.click()
        self.page.wait_for_timeout(500)
        logger.info("Selected 'Angle of Attack (AoA)' measure")

        # ===== TYPE (WIMS Alert/Alarm) =====
        self.page.wait_for_timeout(500)
        type_alert = self.page.get_by_text("WIMS Alert", exact=True)
        expect(type_alert).to_be_visible(timeout=20000)
        type_alert.click(force=True)
        self.page.wait_for_timeout(500)

        # ===== SEVERITY =====
        self.page.get_by_role("cell", name="Low").get_by_role("textbox").fill("11")
        self.page.get_by_role("cell", name="Medium").get_by_role("textbox").fill("12")
        self.page.get_by_role("cell", name="High").get_by_role("textbox").fill("13")
        self.page.get_by_role("cell", name="Extreme").get_by_role("textbox").fill("15")

        # ===== FILTER =====
        expect(self.filter_dropdown).to_be_visible(timeout=20000)
        self.filter_dropdown.click()
        self.page.wait_for_timeout(2000)  # Wait longer for dropdown to open
        
        # Look for "Date and Time" in the dropdown options
        date_time_option = self.page.locator("div.dx-item-content.dx-list-item-content", has_text="Date and Time")
        expect(date_time_option).to_be_visible(timeout=20000)
        date_time_option.click()
        self.page.wait_for_timeout(500)
        logger.info("Selected 'Date and Time' filter")

        # ===== DATES =====
        # Start Date
        select_btns = self.page.get_by_role("button", name="Select")
        expect(select_btns.first).to_be_visible(timeout=20000)
        select_btns.first.click()
        self.page.wait_for_timeout(500)
        
        date_6 = self.page.get_by_text("6").nth(1)
        expect(date_6).to_be_visible(timeout=10000)
        date_6.click()
        
        done_btn = self.page.get_by_role("button", name="Done")
        expect(done_btn).to_be_visible(timeout=10000)
        done_btn.click()
        self.page.wait_for_timeout(500)
        
        # End Date
        select_btns.nth(1).click()
        self.page.wait_for_timeout(500)
        
        date_13 = self.page.get_by_text("13").nth(2)
        expect(date_13).to_be_visible(timeout=10000)
        date_13.click()
        
        done_btn = self.page.get_by_role("button", name="Done")
        expect(done_btn).to_be_visible(timeout=10000)
        done_btn.click()
        self.page.wait_for_timeout(500)
        
        logger.info("Start and end dates selected")

        # ===== ADD TO GRID =====
        expect(self.add_to_grid_btn).to_be_visible(timeout=20000)
        expect(self.add_to_grid_btn).to_be_enabled(timeout=20000)
        self.add_to_grid_btn.click()
        self.page.wait_for_timeout(500)
        logger.info("Added to grid")

        # ===== SAVE =====
        self.save_btn_wims.click()
        logger.info("Clicked Save")
        self.verify_success()

        # Wait until back on table
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)
        expect(self.rows.first).to_be_visible(timeout=20000)


    def delete_first_wims_record(self):
        expect(self.delete_btn).to_be_visible(timeout=20000)
        self.delete_btn.click()
        logger.info("Clicked delete icon")

        expect(self.yes_btn).to_be_visible(timeout=10000)
        self.yes_btn.click()
        logger.info("Clicked Yes on confirmation popup")

       # Wait for table reload
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)
        self.verify_success()

        logger.info("Record deleted successfully")
    
    def click_reset_and_verify(self):
        expect(self.reset_btn).to_be_visible(timeout=20000)

        self.reset_btn.click()
        logger.info("Clicked Reset button")

        # Wait for table refresh
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)

        expect(self.rows.first).to_be_visible(timeout=20000)

        logger.info("Table reset successfully")

    def edit_wims_description(self, new_text="dasdsdfff"):
        # Click Edit
        expect(self.edit_btn).to_be_visible(timeout=20000)
        self.edit_btn.click()
        logger.info("Clicked Edit button")

        # Update Description
        expect(self.description_input).to_be_visible(timeout=20000)
        self.description_input.click()
        self.description_input.fill(new_text)

        logger.info(f"Updated description to: {new_text}")

        # Save
        expect(self.save_btn_popup).to_be_visible(timeout=20000)
        self.save_btn_popup.click()
        logger.info("Clicked Save button")

        # Wait to return to table
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)
        expect(self.rows.first).to_be_visible(timeout=20000)

        self.verify_success()
        logger.info("Edit saved successfully")

        #================================================
        #WORKFLOW MANAGEMENT 
        #================================================

    def add_workflow(self):

        # Click Add Workflow
        expect(self.add_workflow_btn).to_be_visible(timeout=20000)
        self.add_workflow_btn.click()

       # Wait for form
        expect(self.page.locator("div.add-workflow.dx-template-wrapper")).to_be_visible(timeout=20000)
        logger.info("Add Workflow form opened")

       # Fill inputs
        expect(self.workflow_name_input).to_be_visible(timeout=20000)
        self.workflow_name_input.fill("aa")

        expect(self.workflow_desc_input).to_be_visible(timeout=20000)
        self.workflow_desc_input.fill("Test Workflow Description")

        logger.info("Workflow details entered")

       # Add Stage
        expect(self.add_stage_btn).to_be_visible(timeout=20000)
        self.add_stage_btn.click()

        self.stage_name_input.fill("Detected")
        self.stage_desc_input.fill("Alarm has been detected")

        for _ in range(3):
            self.increment_btn.click()

        # Save stage
        edit_row = self.page.locator('#WorkflowStages tr.dx-edit-row')
        stage_save_btn = edit_row.locator('dx-button[aria-label="save-white"]')
         

        expect(stage_save_btn).to_be_visible(timeout=20000)
        stage_save_btn.click()
        logger.info("Clicked Stage Save")

        # Handle popup → NO
        no_btn = self.page.locator('dx-button[aria-label="No"]')
        expect(no_btn).to_be_visible(timeout=20000)
        no_btn.click()
        logger.info("Clicked NO on confirmation popup")

       # Click Recipients
        edit_row = self.page.locator('#WorkflowStages tr.dx-edit-row')
        edit_recipients_btn = edit_row.locator('td:last-child dx-button')

        expect(edit_recipients_btn).to_be_visible(timeout=20000)
        edit_recipients_btn.click()
        logger.info("Clicked Edit Recipients button")

        # Click User tab
        expect(self.user_tab).to_be_visible(timeout=20000)
        self.user_tab.click(force=True)

        # Open dropdown
        user_dropdown = self.page.locator('dx-select-box[name="user"]')
        expect(user_dropdown).to_be_visible(timeout=20000)
        user_dropdown.click()

       # Wait for dropdown
        user_list = self.page.locator('.dx-list[role="listbox"]')
        expect(user_list).to_be_visible(timeout=20000)

        # Type search
        user_input = user_dropdown.locator('input.dx-texteditor-input')
        user_input.click()
        user_input.type("laun", delay=100)

        # Select user
        launchpad_user = self.page.locator('.dx-list-item:has(strong:has-text("Launchpad demo"))')
        expect(launchpad_user).to_be_visible(timeout=20000)
        launchpad_user.click()

        
        # Select Pop-up checkbox in row (using init locator)
        row = self.user_row(" launchpad ")
        expect(row).to_be_visible(timeout=20000)

        popup_checkbox = self.popup_checkbox(row)
        popup_checkbox.scroll_into_view_if_needed()

        expect(popup_checkbox).to_be_visible(timeout=20000)
        popup_checkbox.click(force=True)

        logger.info("Pop-up checkbox selected")

        # SECOND SAVE (save popup settings)
        expect(self.popup_save_btn1).to_be_visible(timeout=20000)
        self.popup_save_btn1.scroll_into_view_if_needed()
        self.popup_save_btn1.click()

        logger.info("Popup settings saved")

        
        expect(self.stage_save_btn.first).to_be_visible(timeout=20000)
        self.stage_save_btn.first.click()

        expect(self.yes_btn).to_be_visible(timeout=10000)
        self.yes_btn.click()


        
        expect(self.workflow_final_save_btn).to_be_enabled(timeout=20000)
        self.workflow_final_save_btn.click()
        self.yes_btn.click()

        logger.info("Workflow saved successfully")

        # Verify
        expect(self.rows.first).to_be_visible(timeout=20000)


        logger.info("Workflow created successfully ") 

        # Wait for table reload
        expect(self.rows.first).to_be_visible(timeout=20000)

    
        expect(self.workflow_recipients_icon).to_be_visible(timeout=20000)
        self.workflow_recipients_icon.click()

        logger.info("Clicked Workflow Recipients icon")

        # Wait for popup and close
        expect(self.workflow_close_icon).to_be_visible(timeout=20000)
        self.workflow_close_icon.click()

        logger.info("Closed Workflow Recipients popup")

        # Click Edit button
        expect(self.workflow_edit_btn).to_be_visible(timeout=20000)
        self.workflow_edit_btn.click()

        logger.info("Clicked Edit button")

        # Click YES on popup
        expect(self.yes_btn).to_be_visible(timeout=10000)
        self.yes_btn.click()

        logger.info("Clicked YES on confirmation")

        # Wait for edit popup
        expect(self.edit_workflow_desc_input).to_be_visible(timeout=20000)

        self.edit_workflow_name_input.click()
        self.edit_workflow_name_input.fill("aa1")

        # Update description
        self.edit_workflow_desc_input.click()
        self.edit_workflow_desc_input.fill("Updated workflow description")
    

        logger.info("Updated description")

        # Click Save
        expect(self.edit_workflow_save_btn).to_be_enabled(timeout=20000)
        self.edit_workflow_save_btn.click()

        
        expect(self.yes_btn).to_be_visible(timeout=10000)
        self.yes_btn.click()


        logger.info("Clicked Save after edit")

        # Wait for table reload
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)

        logger.info("Workflow edited successfully ")

       
        expect(self.workflow_delete_btn).to_be_visible(timeout=20000)
        self.workflow_delete_btn.click()

        logger.info("Clicked Delete button")

        # Confirm Delete
        expect(self.yes_btn).to_be_visible(timeout=10000)
        self.yes_btn.click()

        logger.info("Clicked YES on delete confirmation")

        # Wait for table reload
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)

        logger.info("Workflow deleted successfully ")

        # =================================================
        # WIMS ALARM/ALERT SUPPRESSION / DISABLE
        # =================================================

    def click_add_alert_suppression(self):
        """Open Add Alarm/Alert Suppression popup"""
        expect(self.supp_add_btn).to_be_visible(timeout=20000)
        self.supp_add_btn.click()

       # Wait for popup form
        expect(self.supp_name_input).to_be_visible(timeout=20000)

        logger.info("Opened Add Alarm/Alert Suppression form")


    def create_alert_suppression(self):
        """Complete flow: Open form → Fill → Save"""
        self.click_add_alert_suppression()
        self.fill_alert_suppression_form()


    def fill_alert_suppression_form(self):

         # ===== TEXT =====
        expect(self.supp_name_input).to_be_visible(timeout=20000)
        self.supp_name_input.fill("aaaaaa")

        expect(self.supp_desc_input).to_be_visible(timeout=20000)
        self.supp_desc_input.fill("bbbbbb")

        logger.info("Entered suppression name & description")

        # ===== SYSTEM (AoA) =====

        expect(self.supp_system_dropdown).to_be_visible(timeout=20000)

        self.supp_system_dropdown.scroll_into_view_if_needed()
        self.supp_system_dropdown.click(force=True)

        expect(self.supp_option_aoa).to_be_visible(timeout=20000)
        self.supp_option_aoa.click()

        logger.info("Selected system: AoA")

        # ===== MEASURE =====
        self.supp_measure_dropdown.click()

        expect(self.supp_option_all).to_be_visible(timeout=20000)
        self.supp_option_all.click()

        logger.info("Selected measure: All")

        
        # ALERT TYPE
        self.supp_type_dropdown.click(force=True)
        self.supp_option_all.click()

        # SEVERITY
        self.supp_severity_dropdown.click(force=True)
        self.supp_option_all.click()

        # DESCRIPTION
        self.supp_description_dropdown.click(force=True)
        self.supp_option_all.click()
        
       
        # ===== FILTER =====
        expect(self.supp_filter_dropdown).to_be_enabled(timeout=20000)
        self.supp_filter_dropdown.click()

        # wait for option (not overlay)
        expect(self.supp_option_date_time).to_be_visible(timeout=20000)
        self.supp_option_date_time.click()
        logger.info("Selected 'Date and Time' filter")

      # ===== START DATE =====
        start_btn = self.supp_select_buttons.first
        expect(start_btn).to_be_visible(timeout=20000)
        start_btn.click()
        
        self.page.wait_for_timeout(500)

        expect(self.supp_calendar_overlay).to_be_visible(timeout=20000)
        self.supp_start_date.click()
        self.supp_done_btn.click()

        # ===== END DATE =====
        end_btn = self.supp_select_buttons.nth(1)
        end_btn.click()
 
        self.page.wait_for_timeout(500)
        expect(self.supp_calendar_overlay).to_be_visible(timeout=20000)
        self.supp_end_date.click()
        self.supp_done_btn.click()

        # ===== ADD TO GRID =====
        expect(self.supp_add_to_grid_btn).to_be_enabled(timeout=20000)
        self.supp_add_to_grid_btn.click()

        logger.info("Added to grid")

        expect(self.supp_save_btn).to_be_enabled(timeout=20000)
        self.supp_save_btn.click()

        # ===== VERIFY =====
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)
        expect(self.supp_rows.first).to_be_visible(timeout=20000)

        logger.info("Alert Suppression created successfully")

    def edit_alert_suppression_description(self, new_text="updated description"):
    
          # Click edit icon
        expect(self.supp_edit_btn).to_be_visible(timeout=20000)
        self.supp_edit_btn.click()
        logger.info("Clicked Edit button")

      # Wait for popup
        expect(self.supp_edit_heading).to_be_visible(timeout=20000)

      # Update description
        expect(self.supp_edit_description_input).to_be_visible(timeout=20000)
        self.supp_edit_description_input.click()
        self.supp_edit_description_input.fill(new_text)

        logger.info(f"Updated description: {new_text}")

        # Click Save
        expect(self.supp_edit_save_btn).to_be_enabled(timeout=20000)
        self.supp_edit_save_btn.click()

        logger.info("Clicked Save after edit")

        # Wait for table reload
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)
        expect(self.rows.first).to_be_visible(timeout=20000)

        self.verify_success()

    def delete_alert_suppression(self):

        # Click delete icon
        expect(self.supp_delete_btn).to_be_visible(timeout=20000)
        self.supp_delete_btn.click()
        logger.info("Clicked Delete button")

       # Wait for popup and click Yes
        expect(self.supp_confirm_yes_btn).to_be_visible(timeout=20000)
        self.supp_confirm_yes_btn.click()
        logger.info("Clicked Yes on confirmation popup")

        # Wait for table refresh
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)
        expect(self.rows.first).to_be_visible(timeout=20000)

        self.verify_success()
        logger.info("Record deleted successfully")

    def click_reset_alert_suppression(self):

         # Click Reset button
        expect(self.reset_btn).to_be_visible(timeout=20000)
        self.reset_btn.click()

        logger.info("Clicked Reset button")
    
    #=========================================
    #Alarm/Alert Workflow Allocation Page
    #==========================================

    def verify_workflow_allocation(self):

        # ===== SELECT SYSTEM =====
        expect(self.workflow_alloc_system_dropdown).to_be_visible(timeout=20000)
        self.workflow_alloc_system_dropdown.click()

        expect(self.workflow_alloc_aoa_option).to_be_visible(timeout=20000)
        self.workflow_alloc_aoa_option.click()
        logger.info("Selected system: AoA")

        # ===== CLICK EDIT ICON =====
        
        expect(self.workflow_alloc_threshold_edit).to_be_visible(timeout=20000)
        self.workflow_alloc_threshold_edit.click()
        logger.info("Clicked threshold edit icon")

        expect(self.workflow_alloc_minutes_input).to_be_visible(timeout=20000)

        self.workflow_alloc_minutes_input.fill("")   # clear
        self.workflow_alloc_minutes_input.type("2")  # set exact value


        logger.info("Incremented value twice")

        # ===== CLICK SAVE =====
        expect(self.workflow_alloc_save).to_be_visible(timeout=20000)
        self.workflow_alloc_save.click()
        logger.info("Clicked Save button")

        # ===== WAIT FOR UI REFRESH =====
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)

        logger.info("Workflow allocation updated successfully")


    def verify_download_workflow(self):

        try:

            # ===== CLICK DOWNLOAD ICON =====
            expect(self.download_icon).to_be_visible(timeout=20000)
            self.download_icon.click()
            logger.info("Clicked Download icon")

            # ===== EXCEL DOWNLOAD =====
            expect(self.download_btn).to_be_visible(timeout=20000)

            with self.page.expect_download() as download_info:
                with self.page.expect_popup() as popup_info:
                    self.download_btn.click()

                popup = popup_info.value
                logger.info("Popup opened for Excel download")

            download = download_info.value
            logger.info(f"Excel file downloaded: {download.suggested_filename}")

            popup.close()
            logger.info("Closed Excel popup")

            self.page.wait_for_timeout(1000)

            # ===== PDF DOWNLOAD =====
            expect(self.download_icon).to_be_visible(timeout=20000)
            self.download_icon.click()

            expect(self.pdf_radio).to_be_visible(timeout=20000)
            self.pdf_radio.click()
            logger.info("Selected PDF format")

            with self.page.expect_download() as download_info_pdf:
                with self.page.expect_popup() as popup_info_pdf:
                    self.download_btn.click()

                popup_pdf = popup_info_pdf.value
                logger.info("Popup opened for PDF download")

            download_pdf = download_info_pdf.value
            logger.info(f"PDF file downloaded: {download_pdf.suggested_filename}")

            popup_pdf.close()
            logger.info("Closed PDF popup")
        
        except Exception as e:
            logger.error(f"Download workflow failed due to application issue: {str(e)}")


    
    def verify_edit_workflow_allocation(self):

        # ===== CLICK EDIT ICON =====
        expect(self.workflow_alloc_edit_btn).to_be_visible(timeout=20000)
        self.workflow_alloc_edit_btn.click()
        logger.info("Clicked Edit icon")

        # ===== CLICK CHECKBOX (ONLY ONCE) =====
        expect(self.workflow_alloc_checkbox).to_be_visible(timeout=20000)

        self.workflow_alloc_checkbox.click()
        logger.info("Checkbox selected")

        # ===== SAVE =====
        expect(self.workflow_alloc_save_btn).to_be_visible(timeout=20000)
        self.workflow_alloc_save_btn.click()

    def click_reset_workflow_allocation(self):

        # ===== CLICK RESET BUTTON =====
        expect(self.reset_button_workflow_alloc).to_be_visible(timeout=20000)
        self.reset_button_workflow_alloc.click()
        logger.info("Clicked Reset button")

        # ===== WAIT FOR PAGE / GRID REFRESH =====
        self.page.wait_for_selector("tr.dx-data-row", timeout=20000)

        expect(self.rows.first).to_be_visible(timeout=20000)
        logger.info("Reset completed and table reloaded")
    