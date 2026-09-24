import pytest
from playwright.sync_api import expect
from pages.reports_page import ReportsPage
from pages.login_page import LoginPage
from utils.helpers import export_simple_download


@pytest.mark.sanity
# verifying all options visible
def test_reports_hover_options(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page
    reports.reports_menu.hover()
    # Assertions in test case
    expect(page.locator("a[href*='canned-reports-list']")).to_be_attached()
    expect(page.locator("a:has-text('Export Download History')")).to_be_attached()
    expect(page.locator("text=Tableau")).to_be_attached()


# ---------CANNED REPORTS------------------


@pytest.mark.sanity
# Verify the title of canned reports page
def test_open_canned_reports(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()
    expect(reports.page.locator("span.title", has_text="Canned Reports List")).to_be_visible()


@pytest.mark.sanity
# Adding new report
def test_add_new_canned_report(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.add_new_reports(
        title="Its a Title!",
        description="Added new report",
        link="link"
    )
    reports.save_report()

    assert reports.is_report_added_successfully()
    reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# Verifying upload functionality with image(<5MB)
def test_upload_image(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.add_new_reports(
        title="Image Upload Test",
        description="Image thumbnail test",
        link="https://www.google.com/"
    )
    # Upload image (<5MB)
    reports.upload_thumbnail("C:/All_document/POC/Launchpad_POC/tests/group2/test_files/small_file.png")
    reports.save_report()
    assert reports.is_report_added_successfully()
    reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# Verifying upload functionality with image(>5MB)
def test_upload_image_more_than_5mb(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.add_new_reports(
        title="Large Image Upload",
        description="Negative image upload test",
        link="https://example.com"
    )

    reports.upload_thumbnail("C:/All_document/POC/Launchpad_POC/tests/group2/test_files/large_file.png")
    reports.save_report()

    #  Expect validation error
    
    error_toast = reports.page.locator("text=5 MB")
    # error_toast = reports.page.locator(".notifications-response",has_text="Invalid Thumbnail image format. Please upload in JPG, JPEG or PNG format.")
    # error_toast.wait_for(state="visible", timeout=10000)
    # assert error_toast.is_visible()
    expect(error_toast).to_be_visible(timeout=10000)
    # reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# Verifying upload functionality with pdf
def test_upload_pdf(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.add_new_reports(
        title="PDF Upload Test",
        description="PDF thumbnail test",
        link="https://example.com"
    )

    reports.upload_thumbnail("C:/All_document/POC/Launchpad_POC/tests/group2/test_files/WAMS_User_Manual.pdf")

    reports.save_report()
    error_toast = reports.page.locator(".notifications-response", has_text="Invalid Thumbnail image format")
    error_toast.wait_for(state="visible", timeout=10000)
    assert error_toast.is_visible()


@pytest.mark.sanity
# Verifying upload functionality with excel
def test_upload_excel(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.add_new_reports(
        title="Excel Upload Test",
        description="Excel thumbnail test",
        link="https://example.com"
    )

    reports.upload_thumbnail("C:/All_document/POC/Launchpad_POC/tests/group2/test_files/WAMS_User_Manual.pdf")

    reports.save_report()
    error_toast = reports.page.locator(".notifications-response", has_text="Invalid Thumbnail image format")
    error_toast.wait_for(state="visible", timeout=10000)
    assert error_toast.is_visible()


@pytest.mark.sanity
# Verify Delete functionality ->NO
def test_delete_report_no(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.delete_first_report()
    reports.confirm_delete_no()

    assert not reports.page.locator(".notifications-response",has_text="deleted successfully").is_visible()


@pytest.mark.sanity
# Verify Delete functionality ->YES
def test_delete_report_yes(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    reports.delete_first_report()
    reports.confirm_delete_yes()

    toast = reports.page.locator(".notifications-response",has_text="deleted successfully")
    toast.wait_for(state="visible", timeout=10000)
    assert toast.is_visible()
    reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# Click->Edit , verify popup title
def test_edit_popup_opens(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()

    # Click edit on first row
    reports.click_edit_first_report()

    # Assert edit popup opened
    expect(reports.page.locator("text=Edit Canned Report")).to_be_visible()
    reports.save_edit()


@pytest.mark.sanity
# verify the popup message after editing report ->save option
def test_edit_report_save(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page

    reports.open_canned_reports()

    # Open Edit
    reports.click_edit_first_report()
    reports.wait_for_edit_popup()

    # Update description
    reports.edit_report_description("Edited via automation")

    # Save
    reports.save_edit()

    # Assert success message
    toast = page.locator(".notifications-response",has_text="Canned Report has been updated successfully")
    toast.wait_for(state="visible", timeout=10000)
    assert toast.is_visible()
    reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# verify the popup message no editing report ->save option
def test_no_edit_report_save(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page

    reports.open_canned_reports()

    # Open Edit
    reports.click_edit_first_report()
    reports.wait_for_edit_popup()
    # Save
    reports.save_edit()

    # Assert success message
    toast = page.locator(".notifications-response",has_text="Canned Report has been updated successfully")
    toast.wait_for(state="visible", timeout=10000)
    assert toast.is_visible()
    reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# verify X button confirmation popup
def test_close_button_confirmation(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page
    reports.open_canned_reports()
    reports.click_edit_first_report()
    close_btn = reports.page.locator(".dx-overlay-content span",has_text="×")

    # Assertion - click button is visible and clickable
    expect(close_btn).to_be_visible()
    close_btn.click(force=True)
    reports.wait_for_cancel_confirmation()

    # Assertion - confirmation popup yes/no
    expect(page.locator("text=Yes")).to_be_visible()
    expect(page.locator("text=No")).to_be_visible()
    # cleanup
    reports.confirm_cancel_yes()


@pytest.mark.sanity
# Verify X button confirmation popup - NO option
def test_edit_close_no(login_wims_application):
    reports = ReportsPage(login_wims_application)

    reports.open_canned_reports()
    reports.click_edit_first_report()
    reports.wait_for_edit_popup()

    # Click X
    reports.click_edit_close_x()
    reports.wait_for_cancel_confirmation()

    # Click No
    reports.confirm_cancel_no()

    # Still on Edit popup
    expect(reports.page.locator("text=Edit Canned Report")).to_be_visible()
    # Cleanup (close popup)
    reports.click_edit_close_x()
    reports.confirm_cancel_yes()


@pytest.mark.sanity
# Verify X button confirmation popup - YES  option
def test_edit_close_yes(login_wims_application):
    reports = ReportsPage(login_wims_application)

    reports.open_canned_reports()
    reports.click_edit_first_report()
    reports.wait_for_edit_popup()

    # Click X
    reports.click_edit_close_x()
    reports.wait_for_cancel_confirmation()

    # Click Yes
    reports.confirm_cancel_yes()

    # Back to list page
    expect(reports.page.locator("span.title", has_text="Canned Reports List")).to_be_visible()


@pytest.mark.sanity
# Verify cancel button  confirmation popup and yes button
def test_edit_cancel_confirmation_yes(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()
    reports.click_edit_first_report()
    reports.wait_for_edit_popup()
    reports.cancel_edit()
    reports.wait_for_cancel_confirmation()
    # Assertions
    expect(reports.page.locator("text=Yes")).to_be_visible()
    expect(reports.page.locator("text=No")).to_be_visible()

    # CLEANUP
    reports.confirm_cancel_yes()

    # Verify back on list
    expect(reports.page.locator("span.title", has_text="Canned Reports List")).to_be_visible()


@pytest.mark.sanity
# Verify cancel button confirmation popup - NO  option
def test_edit_cancel_no(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_canned_reports()
    reports.click_edit_first_report()
    reports.wait_for_edit_popup()
    reports.cancel_edit()
    reports.wait_for_cancel_confirmation()
    reports.confirm_cancel_no()
    # Still on Edit popup
    expect(reports.page.locator("text=Edit Canned Report")).to_be_visible()
    reports.save_edit()


@pytest.mark.sanity
# Verify Export options visible (PDF, Excel, Download)
def test_export_options_visible(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page

    reports.open_canned_reports()

    # Export icon
    expect(reports.export_icon).to_be_visible()
    expect(reports.export_icon).to_be_enabled()

    reports.export_icon.click(force=True)
    expect(reports.export_modal).to_be_visible()

    # Excel & PDF options
    expect(page.locator(".dx-overlay-content div.dx-item-content", has_text="Excel")).to_be_visible()
    expect(page.locator(".dx-overlay-content div.dx-item-content", has_text="PDF")).to_be_visible()
    # Download button
    expect(reports.download_button).to_be_visible()


@pytest.mark.sanity
# Verify Excel downloaded -> assert popup
def test_export_excel_download(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page

    reports.open_canned_reports()

    # Open Export popup
    reports.export_icon.click(force=True)
    reports.export_modal.wait_for(state="visible", timeout=10000)

    #  Use helper
    downloaded_files = export_simple_download(page, "Excel")

    # Assert success message
    toast = page.locator(".notifications-response", has_text="Canned Report")
    toast.wait_for(state="visible", timeout=10000)
    assert toast.is_visible()

    reports.wait_for_toast_to_disappear()


@pytest.mark.sanity
# Verify PDF downloaded -> assert popup
def test_export_pdf_download(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page

    reports.open_canned_reports()

    reports.export_icon.click(force=True)
    reports.export_modal.wait_for(state="visible",timeout=10000)

    # Select PDF
    downloaded_files = export_simple_download(page, "PDF")

    toast = page.locator(".notifications-response", has_text="Canned Report")
    toast.wait_for(state="visible", timeout=10000)
    assert toast.is_visible()

    reports.wait_for_toast_to_disappear()

# ---------------EXPORT DOWNLOAD-----------------


@pytest.mark.sanity
# Verify Export download history title when opened
def test_export_download_history(login_wims_application):
    reports = ReportsPage(login_wims_application)
    reports.open_export_history()
    assert "Export Download History" in reports.page.title()


@pytest.mark.sanity
# Verify whether page has file if yes->download , no-> skip
def test_export_download_history_file_download(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page

    # Step 1: Open Export Download History page
    reports.open_export_history()

    # Step 2: Locate download icons
    download_icons = page.locator("img[src*='file-download.svg']")
    file_count = download_icons.count()

    # Step 4: Conditional behavior
    if file_count == 0:
        #  Valid scenario: no files available
        print("No export files available for download")
        pytest.skip("No export files available in Export Download History")

    first_download = download_icons.first
    # Assertion - download option is visible
    expect(first_download).to_be_visible()
    expect(first_download).to_be_enabled()

    # Files available: download first file
    with page.expect_download() as download_info:
        download_icons.first.click(force=True)

        download = download_info.value

        # Step 5:  assertion
        assert download.suggested_filename is not None

# --------------TABLEAU ------------------------


@pytest.mark.sanity
# Verify Tableau opens in new tab and close
def test_tableau_link(login_wims_application):
    reports = ReportsPage(login_wims_application)
    page = reports.page
    context = page.context
    reports.open_reports_menu()

    # Capture current pages
    existing_pages = context.pages.copy()

    # Click Tableau
    reports.open_tableau()

    # open a tab
    page.wait_for_timeout(2000)

    # Check if a NEW tab opened
    new_pages = context.pages
    new_tab = None

    for p in new_pages:
        if p not in existing_pages:
            new_tab = p
            break

    if new_tab:
        # Tableau opened in new tab
        new_tab.wait_for_load_state()
        new_tab.close()

        # Return to parent
        page.bring_to_front()
    else:
        # Tableau opened in same tab
        assert "tableau" in page.url.lower() or "report" in page.url.lower()

        # Go back to Wims
        page.go_back()
        page.wait_for_load_state()

    # Final assertion on parent page
    assert "WIMS" in page.title()


@pytest.mark.sanity
# Logout
def test_logout(login_wims_application):
        page = login_wims_application
        login_page = LoginPage(page)
        login_page.account_icon = login_page.account_icon.first
        login_page.logout_user()