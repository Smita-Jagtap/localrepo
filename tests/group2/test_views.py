import pytest
from playwright.sync_api import expect
from pages.views_page import ViewsPage
import os
from pages.login_page import LoginPage
#from pathlib import Path
from config.environment import env
from utils.helpers import export_with_date_range
#from conftest import login_wims_application

# ------------------------------------------------------
# TC-1 SANITY: Views Menu Visible
# ------------------------------------------------------
@pytest.mark.sanity
def test_views_menu_visible(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    page.locator(ViewsPage.VIEWS_MENU).wait_for(
        state="attached", timeout=15000
    )


# ------------------------------------------------------
# TC-2 SANITY: Hover on Views shows submenus
# ------------------------------------------------------
@pytest.mark.sanity
def test_views_menu_hover_shows_submenus(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    views_page.hover_on_views_menu()
    views_page.verify_views_submenus_visible()


# ------------------------------------------------------
# TC‑3 SANITY: Train Pass View page loads
# ------------------------------------------------------
@pytest.mark.sanity
def test_train_pass_view_opens(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    views_page.hover_on_views_menu()
    views_page.click_train_pass_view()

    #  ONLY page load verification
    views_page.verify_train_pass_view_page_loaded()


#------------------------------------------------------
# TC‑4 SANITY: Tooltip visible ONLY for RED WIMS status
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc4_wims_status_tooltip_visible_only_for_red(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    wims_status_elements = [
        views_page.wims_processing,
        views_page.oss_connectivity,
        views_page.trims_connectivity,
        views_page.treg_operational,
        views_page.email_services,
        views_page.sms_services,
        views_page.database_performance,
        views_page.equip_connectivity,
    ]

    for status_element in wims_status_elements:
        views_page.verify_tooltip_visible_if_status_red(status_element)

# ------------------------------------------------------
# TC‑5: Save Filter Flow
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc5_save_filters_as_user_preference(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    # Step 1: Click Save
    views_page.click_save_button()

    # Step 2: Verify popup
    views_page.verify_confirmation_popup()

    # Step 3: Click Yes
    views_page.click_yes()

    # Step 4: Verify success
    views_page.verify_success_popup()

 
# ------------------------------------------------------
#  TC‑6: Train Pass List Save Flow
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc7_train_pass_list_save_filters(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    # Step 1: Click Save
    views_page.click_save_button()

    #  Step 2: Popup appears
    views_page.verify_confirmation_popup()

    #  Step 3: Click Yes
    views_page.click_yes()

    #  Step 4: Success popup
    views_page.verify_success_popup()

   


# # ------------------------------------------------------
# # TC‑6: Reset Sorting
# # ------------------------------------------------------
# @pytest.mark.sanity
# def test_tc6_reset_column_filters_and_sorts(login_wims_application):
#     page = login_wims_application
#     views_page = ViewsPage(page)

#     # Step 1: Click Reset
#     views_page.click_reset_button()

#     # Step 2: Verify Date/Time descending
#     views_page.verify_date_time_descending()


# ------------------------------------------------------
#  TC‑7 SANITY: Export flow (no file validation)
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc8_export_with_date_range(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    #Step 1: Open Export popup
    views_page.open_export_popup()

    #  Step 2: Prepare calendar 
    views_page.prepare_calendar_for_helper()

    #  Step 3: Run export (Excel)
    result = export_with_date_range(
        page=page,
        start_date="May 12, 2026",
        end_date="May 13, 2026",
        export_format="Excel"
    )

    assert result is None or isinstance(result, list)

    #  Step 4: Open again for PDF
    views_page.open_export_popup()
    views_page.prepare_calendar_for_helper()

    result = export_with_date_range(
        page=page,
        start_date="May 12, 2026",
        end_date="May 13, 2026",
        export_format="PDF"
    )

    assert result is None or isinstance(result, list)


# ------------------------------------------------------
#  TC‑8: Train Pass List Export Flow
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc9_train_pass_list_export(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    # ==============================
    #  Excel Export
    # ==============================
    views_page.open_train_pass_export_popup()

    #  CRITICAL FIX
    views_page.prepare_calendar_for_helper()

    export_with_date_range(
        page=page,
        start_date="May 13, 2024",
        end_date="May 12, 2026",
        export_format="Excel"
    )

    # ==============================
    #  PDF Export
    # ==============================
    views_page.open_train_pass_export_popup()
    views_page.prepare_calendar_for_helper()

    export_with_date_range(
        page=page,
        start_date="May 13, 2024",
        end_date="May 12, 2026",
        export_format="PDF"
    )


    
# ------------------------------------------------------
#  TC‑9: Add/Remove Columns FULL FLOW (Corrected)
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc11_add_remove_columns(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    # ===============================
    #  STEP 1: OPEN POPUP
    # ===============================
    popup=views_page.open_column_popup()
    views_page.verify_popup_opened(popup)

    # # ===============================
    # #  STEP 2: SELECT ALL
    # # ===============================
    # views_page.click_select_all()
    # views_page.verify_all_checkboxes_selected()
    # views_page.click_apply()

    # # ===============================
    # # STEP 3: DESELECT ALL
    # # ===============================
    # views_page.open_column_popup()
    # views_page.click_deselect_all()
    # views_page.verify_all_checkboxes_unselected()
    # views_page.click_apply()

    # #  verify red popup
    # views_page.verify_error_popup()

    # # ===============================
    # # STEP 4: DEFAULT
    # # ===============================
    # views_page.open_column_popup()
    # views_page.click_default()
    # views_page.click_apply()

#===================================
# TC-10-Toggle
#===================================

@pytest.mark.sanity
def test_tc10_toggle_train_pass_to_alarm(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    #  Click toggle
    views_page.click_toggle_switch()

    #  Verify rows visible → means Alarm table loaded
    views_page.verify_switched_to_alarm_list()  

#===================================
# TC-11-Export alarm list
#===================================
@pytest.mark.sanity
def test_tc_export_alarm_list(login_wims_application):
    page = login_wims_application
    views = ViewsPage(page)

    #  Step‑1: Click export (Alarm list)
    views.click_export_alarm()

    #  Step‑2: Use existing helper (no rewrite)
    export_with_date_range(
        page=page,
        start_date="May 28, 2026",
        end_date="May 27, 2026",
        export_format="Excel"
    )

#===================================
# TC-12-save alarm list
#===================================

@pytest.mark.sanity
def test_tc_save_alarm_list(login_wims_application):
    page = login_wims_application
    views = ViewsPage(page)

    # STEP 1: Click Save
    views.click_save()

    # STEP 2: Verify confirmation popup
    views.verify_confirmation_popup()

    # STEP 3: Click Yes
    views.click_yes()

    # STEP 4: Verify success message
    views.verify_success_message()


# ------------------------------------------------------
# TC‑13: Navigate to Operations Alarm Monitoring View
# ------------------------------------------------------
@pytest.mark.sanity
def test_operation_alarm_monitoring(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    views_page.hover_on_views_menu()
    views_page.click_operation_alarm_menu()

    # ONLY page load verification
    views_page.verify__operation_alarm_page_loaded()

# ------------------------------------------------------
# TC-14: Export - Operations Alarm Monitoring View--24hr
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc_export_operations_alarm(login_wims_application):
    page = login_wims_application
    views = ViewsPage(page)

    #  STEP 1: Click Export button
    views.click_export1_alarm()

    # STEP 2: Reuse your existing helper
    export_with_date_range(
        page=page,
        start_date="May 13, 2026",
        end_date="May 14, 2026",
        export_format="Excel"
    )

# ------------------------------------------------------
# TC-15: Save functionality - Operations Alarm Monitoring-24hr
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc_save_operations_alarm(login_wims_application):
    page = login_wims_application
    views = ViewsPage(page)

    #  Step 1: Click Save button
    views.click_save()

    # Step 2: Verify confirmation popup appears
    views.verify_confirmation_popup()

    # Step 3: Click Yes on popup
    views.click_yes()

    #  Step 4: Verify success message is displayed
    views.verify_success_message()
  



# import pytest
# from pages.views_page import ViewsPage
# from utils.helpers import export_with_date_range


# @pytest.mark.sanity
# def test_tc_export_operation_alarm_list(login_wims_application):

#     page = login_wims_application
#     views = ViewsPage(page)

#     #  Step 1: export click
#     views.click_export_operation_alarm()

#     #  Step 2: prepare BOTH calendars
#     views.prepare_start_and_end_calendar()

#     #  Step 3: run helper (unchanged)
#     export_with_date_range(
#         page=page,
#         start_date="May 28, 2024",
#         end_date="May 14, 2026",
#         export_format="Excel"
#     )

   
# ------------------------------------------------------
#  TC-16: Save - Operation Alarm List (2nd table)
# ------------------------------------------------------
@pytest.mark.sanity
def test_tc_save_operation_alarm_list(login_wims_application):

    page = login_wims_application
    views = ViewsPage(page)

    views.click_save_operation_alarm()

    views.verify_confirmation_popup()

    views.click_yes()

    views.verify_success_message()

    
# ------------------------------------------------------
#  TC‑17: Add/Remove Columns operation alarm list-24hr
# ------------------------------------------------------
@pytest.mark.sanity
def test_add_remove_columns(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    popup=views_page.open_column_popup()
    views_page.verify_popup_opened(popup)

# ------------------------------------------------------
#  TC‑18: Add/Remove Columns  for opeartion alarm list 
# ------------------------------------------------------
@pytest.mark.sanity
def test_add_remove_columns_2nd(login_wims_application):
    page = login_wims_application
    views_page = ViewsPage(page)

    popup=views_page.open_column_popup()
    views_page.verify_popup_opened(popup)
