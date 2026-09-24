from playwright.sync_api import expect

class ViewsPage:
    VIEWS_MENU = "text=Views"

    def __init__(self, page):
        self.page = page

        self.views_menu = page.get_by_text("Views")
        self.train_pass_view_link = page.get_by_role(
            "link", name="Train Pass View"
        )
        self.operations_alarm_view_link = page.get_by_text(
            "Operations Alarm Monitoring View"
        )
        self.train_pass_view_title = page.get_by_text(
            "Train Pass View", exact=True
        )
        self.operations_alarm_view_title = page.get_by_text(
            "Operations Alarm Monitoring View", exact=True
         )
        # Page elements → must use self.
        self.wims_processing = page.get_by_text("WIMS Processing")
        self.oss_connectivity = page.get_by_text("OSS Connectivity")
        self.trims_connectivity = page.get_by_text("TRIMS Connectivity")
        self.treg_operational = page.get_by_text("TREG Operational")
        self.email_services = page.get_by_text("Email Services")
        self.sms_services = page.get_by_text("SMS Services")
        self.database_performance = page.get_by_text("Database Performance")
        self.equip_connectivity = page.get_by_text("EQUIP Connectivity")

        # Tooltip container
        self.tooltip = page.locator(".dx-tooltip")
        self.table_container = page.get_by_label(
            "Train Alarm /Alert List - 24 hr"
        )

        # Date/Time column
        self.date_time_header = self.table_container.get_by_text("Date/Time")

        # Save button 
        self.save_button = page.get_by_role("button").nth(5)

        # Reset button 
        self.reset_button = page.locator("dx-button").nth(3)

        # Confirmation popup
        self.confirm_popup = page.get_by_text("WIMS Confirmation Message")

        # Yes button
        self.yes_button = page.get_by_role("button", name="Yes")

        # Success message
        self.success_message = page.get_by_text(
            "Filter preference saved successfully."
        )
        #  Train Pass List Save button (YOUR locator)
        self.train_pass_save_button = page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-16.btn-icon.dx-state-hover"
        ).nth(0)  

        #  Confirmation popup
        self.confirm_popup = page.get_by_text("WIMS Confirmation Message")

        # Yes button
        self.yes_button = page.get_by_role("button", name="Yes")

        #  Success message
        self.success_message = page.get_by_text(
            "Filter preference saved successfully."
        )

        # ✅ EXPORT LOCATORS

        # Export button
        self.export_button = page.get_by_role("button").nth(3)

        # Export popup container
        self.export_popup = page.locator(".dx-overlay-content")

        # Start & End date buttons
        self.start_date_btn = page.get_by_role("button", name="Select").first
        self.end_date_btn = page.get_by_role("button", name="Select").nth(1)

        # Format radio buttons
        self.excel_radio = page.get_by_role("radio", name="Excel")
        self.pdf_radio = page.get_by_role("radio", name="PDF")

        # Train Pass List Section
        self.train_pass_section = page.get_by_label("Train Pass List")

        #  Export button (REMOVE dx-state-hover)
        self.train_pass_export_btn = self.train_pass_section.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-16.btn-icon"
        ).nth(0)  

        #  Popup container 
        self.export_popup = page.locator(".dx-overlay-content")

         # Toggle switch
        self.toggle_switch = page.locator("#switchTable")

        #RELIABLE identifier → any table row
        self.alarm_table_rows = page.locator("tbody tr")

        #  THIS MUST BE INSIDE __init__
        self.column_button = page.get_by_role("button").nth(4)
           
    # GET CURRENT VISIBLE POPUP (IMPORTANT FIX)
    def get_active_popup(self):
        return self.page.locator(".dx-overlay-content:visible")

    # OPEN POPUP
    def open_column_popup(self):
        print("DEBUG: column_button exists ->", hasattr(self, "column_button"))
        self.column_button.wait_for(state="visible", timeout=20000)
        self.column_button.click()

        popup = self.get_active_popup()
        popup.wait_for(state="visible", timeout=20000)
        return popup
    
        self.export_button = page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-16.btn-icon"
        ).nth(0) 

        # All toolbar buttons
        self.toolbar_buttons = page.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.icon-16.btn-icon"
        )

        # Save button 
        self.save_button = self.toolbar_buttons.nth(2)

        #  Popup elements
        self.confirm_popup = page.get_by_text("WIMS Confirmation Message")
        self.yes_button = page.get_by_role("button", name="Yes")
        self.success_message = page.get_by_text(
            "Filter preference saved successfully."
        )
    
      # 2nd menu exportlocator
        self.export_button = page.get_by_role("button").nth(3)
      #  2nd menu save button
        self.save_button = page.get_by_role("button").nth(5)


    def click_save_operation_alarm(self):

        # ✅ locate both sections
        sections = self.page.locator("text=Operations Alarm Monitoring List")

        # ✅ pick SECOND section (important)
        second_section = sections.nth(1).locator("..").locator("..")

        # ✅ find SAVE button (adjust index if needed)
        save_btn = second_section.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-16.btn-icon:visible"
        ).nth(2)

        save_btn.wait_for(state="visible", timeout=20000)
        save_btn.scroll_into_view_if_needed()
        save_btn.hover()
        save_btn.click(force=True)

        
        self.section =self.page.get_by_text("Operations Alarm Monitoring List - 24 hr") \
              .locator("..").locator("..")

        add_remove_btn = self.section.get_by_role("button").nth(4)

        self.section = self.page.get_by_text("Operations Alarm Monitoring List") \
              .nth(1).locator("..").locator("..")

        add_remove_btn = self.section.locator(
    ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.icon-16.btn-icon"
).nth(4)

        
       
    # ---------------- Actions ----------------
    def hover_on_views_menu(self):
        self.views_menu.hover()

    def click_train_pass_view(self):
        self.train_pass_view_link.click()

    def hover_on_wims_status(self, status_element):
        """Hover on a WIMS status element"""
        status_element.scroll_into_view_if_needed()
        status_element.hover(force=True)

    def click_save_button(self):
        """Click Save filter button"""
        self.save_button.wait_for(state="visible", timeout=20000)
        self.save_button.click()

    def click_yes(self):
        self.yes_button.wait_for(state="visible", timeout=20000)
        self.yes_button.click()

    def click_reset_button(self):
        """Click Reset column filters and sorts"""
        self.reset_button.wait_for(state="visible", timeout=20000)
        self.reset_button.click()
 
    
    def click_train_pass_save_button(self):
        """Click Train Pass Save icon"""
        self.train_pass_save_button.wait_for(state="attached", timeout=20000)
        self.train_pass_save_button.scroll_into_view_if_needed()
        self.train_pass_save_button.click()

    def click_yes(self):
        self.yes_button.wait_for(state="visible", timeout=20000)
        self.yes_button.click()

    #  ACTION: Open Export Popup train alaram/alert
    def open_export_popup(self):
        self.export_button.wait_for(state="visible", timeout=20000)
        self.export_button.click()

        # Critical: wait for popup
        self.export_popup.last.wait_for(state="visible", timeout=20000)

    # ==================================================
    # FIX: Make calendar usable 
    # ==================================================
    def prepare_calendar_for_helper(self):
        """
        Ensures start/end date controls work for helper
        """
        # Wait for buttons
        self.start_date_btn.wait_for(state="visible", timeout=20000)
        self.end_date_btn.wait_for(state="visible", timeout=20000)

        #  Activate calendar once
        self.start_date_btn.click(force=True)

        #  Wait until calendar appears
        calendar = self.page.locator(".dx-calendar").last
        calendar.wait_for(state="visible", timeout=20000)

        #  Close calendar
        self.page.keyboard.press("Escape")

        #  Slight delay for stability
        self.page.wait_for_timeout(500)

    # ==================================================
    #  STEP 1: Open Export popup (Train Pass List)
    # ==================================================
    def open_train_pass_export_popup(self):

        # hover section (needed for DevExtreme)
        self.train_pass_section.hover()

        self.train_pass_export_btn.hover()
        self.train_pass_export_btn.click()

        #  store CURRENT popup (important fix)
        self.export_popup = self.page.locator(".dx-overlay-content").last
        self.export_popup.wait_for(state="visible", timeout=20000)

    #  STEP 2: Prepare calendar 
   
    def prepare_calendar_for_helper(self):

        # USE POPUP CONTEXT (IMPORTANT)
        start_btn = self.export_popup.get_by_role("button", name="Select").first

        start_btn.wait_for(state="visible", timeout=20000)

        # Activate calendar once
        start_btn.click(force=True)

        #  WAIT calendar INSIDE popup
        calendar = self.export_popup.locator(".dx-calendar").last
        calendar.wait_for(state="visible", timeout=20000)
        
        # close it 
        self.page.keyboard.press("Escape")

        # small stabilization delay
        self.page.wait_for_timeout(500)

        #CLICK TOGGLE 
    def click_toggle_switch(self):

        self.toggle_switch.wait_for(state="visible", timeout=20000)

        box = self.toggle_switch.bounding_box()

        #  Click RIGHT side knob
        self.page.mouse.click(
            box["x"] + box["width"] - 8,
            box["y"] + box["height"] / 2
        )

        # wait a little for UI transition
        self.page.wait_for_timeout(1000)

    # ==================================================
    #  VERIFY SWITCH 
    # ==================================================
    def verify_switched_to_alarm_list(self):
        expect(self.alarm_list_grid).to_be_visible(timeout=20000)

    def click_export_alarm(self):
        self.export_button.wait_for(state="visible", timeout=20000)
        self.export_button.hover()
        self.export_button.click()
    

    def click_select_all(self, popup):
        btn = popup.get_by_role("button", name="Select All", exact=True)
        btn.wait_for(state="visible", timeout=20000)
        btn.click()

    def click_deselect_all(self, popup):
        btn = popup.get_by_role("button", name="Deselect All")
        btn.wait_for(state="visible", timeout=20000)
        btn.click()

    def click_default(self, popup):
        btn = popup.get_by_role("button", name="Default")
        btn.wait_for(state="visible", timeout=20000)
        btn.click()

    def click_apply(self, popup):
        btn = popup.get_by_role("button", name="Apply")
        btn.wait_for(state="visible", timeout=20000)
        btn.click()
    
    # save after toggle
    def click_save(self):
        self.save_button.wait_for(state="visible", timeout=20000)
        self.save_button.hover()
        self.save_button.click()

    def click_yes(self):
        self.yes_button.wait_for(state="visible", timeout=20000)
        self.yes_button.click()

    def click_operation_alarm_menu(self):
        self.operations_alarm_view_link.click()

    
    # ACTION: CLICK EXPORT
    def click_export1_alarm(self):
        self.export_button.wait_for(state="visible", timeout=20000)

        # ✅ hover helps DevExtreme buttons activate
        self.export_button.hover()
        self.export_button.click()

     
    def click_export_operation_alarm(self):
        sections = self.page.locator("text=Operations Alarm Monitoring List")

        second_section = sections.nth(1).locator("..").locator("..")

        export_btn = second_section.locator(
            ".dx-widget.dx-button.dx-button-mode-contained.dx-button-normal.icon-16.btn-icon:visible"
        ).nth(0)

        export_btn.wait_for(state="visible", timeout=20000)
        export_btn.scroll_into_view_if_needed()
        export_btn.hover()
        export_btn.click()


    def click_export_operation_alarm(self):

        sections = self.page.locator("text=Operations Alarm Monitoring List")

        second_section = sections.nth(1).locator("..").locator("..")

        export_btn = second_section.locator(
            ".dx-widget.dx-button.dx-button-mode-contained."
            "dx-button-normal.icon-16.btn-icon:visible"
        ).nth(0)

        export_btn.wait_for(state="visible", timeout=20000)
        export_btn.hover()
        export_btn.click(force=True)


    # FIX FOR BOTH START & END CALENDARS
    def prepare_start_and_end_calendar(self):

        self.page.get_by_role("button", name="Select").first.click()

        calendar = self.page.locator(".dx-calendar:visible").last
        calendar.wait_for(state="visible", timeout=20000)

        # Navigate backwards to 2024
        for _ in range(3):
            calendar.locator(".dx-prev-button").click()

        self.page.get_by_role("button", name="Select").nth(1).click()

        calendar = self.page.locator(".dx-calendar:visible").last
        calendar.wait_for(state="visible", timeout=20000)

        # Move forward to 2026
        for _ in range(3):
            calendar.locator(".dx-next-button").click()

    def click_yes(self):
        yes_btn = self.page.get_by_role("button", name="Yes")
        yes_btn.wait_for(state="visible", timeout=20000)
        yes_btn.click()




    
    # ---------------- Verifications ----------------
    def verify_views_submenus_visible(self):
        """
        ✅ TC‑1 sanity:
        Verify both submenus appear on hover
        """
        expect(self.train_pass_view_link).to_be_visible()
        expect(self.operations_alarm_view_link).to_be_visible()

    def verify_train_pass_view_page_loaded(self):
        """
         Verify Train Pass View page is loaded
        """
        expect(self.train_pass_view_title).to_be_visible(timeout=30000)


    def is_wims_status_red(self, status_element) -> bool:
        """
        Check if WIMS status indicator is RED
        """
        classes = status_element.get_attribute("class") or ""
        return "red" in classes.lower() or "danger" in classes.lower()

    def verify_tooltip_visible_if_status_red(self, status_element):
        """
        Tooltip must be visible ONLY if status is RED
        """
        if self.is_wims_status_red(status_element):
            self.hover_on_wims_status(status_element)
            expect(self.tooltip).to_be_visible(timeout=10000)

    def verify_confirmation_popup(self):
        expect(self.confirm_popup).to_be_visible(timeout=20000)

    def verify_success_popup(self):
        expect(self.success_message).to_be_visible(timeout=20000)

    def verify_date_time_descending(self):
        """
         Verify Date/Time sorted descending
        """
        expect(self.date_time_header).to_be_visible(timeout=20000)

        # Check sort indicator class
        expect(self.date_time_header).to_have_class(
            lambda cls: "dx-sort-down" in cls or "desc" in cls.lower()
        )


    def verify_confirmation_popup(self):
        expect(self.confirm_popup).to_be_visible(timeout=20000)

    def verify_success_popup(self):
        expect(self.success_message).to_be_visible(timeout=20000)

    #=======Toggle=====================
    def verify_switched_to_alarm_list(self):
        """
        Verify ANY row appears after switching
        """
        expect(self.alarm_table_rows.first).to_be_visible(timeout=20000)

    

      #  VERIFICATIONS
    def verify_all_checkboxes_selected(self, popup):
        checkboxes = popup.get_by_role("checkbox")
        self.page.wait_for_timeout(500)

        for cb in checkboxes.all():
            expect(cb).to_be_checked()

    def verify_all_checkboxes_unselected(self, popup):
        checkboxes = popup.get_by_role("checkbox")
        self.page.wait_for_timeout(500)

        for cb in checkboxes.all():
            expect(cb).not_to_be_checked()

    def verify_error_popup(self):
        error_popup = self.page.locator(".dx-toast-content")
        expect(error_popup).to_be_visible(timeout=20000)
        self.page = page

        
#  VERIFY POPUP OPENED
    def verify_popup_opened(self, popup):
        expect(popup).to_be_visible(timeout=20000)

        
    #  ASSERTIONS for save after toggle
    def verify_confirmation_popup(self):
        self.confirm_popup.wait_for(state="visible", timeout=20000)

    def verify_success_message(self):
        self.success_message.wait_for(state="visible", timeout=20000)

    def verify__operation_alarm_page_loaded(self):
        expect(self.operations_alarm_view_title).to_be_visible(timeout=30000)   

    def verify_confirmation_popup(self):
        expect(self.page.get_by_text("WIMS Confirmation Message")).to_be_visible()

    def verify_success_message(self):
        expect(
            self.page.get_by_text("Filter preference saved successfully")
        ).to_be_visible()     

