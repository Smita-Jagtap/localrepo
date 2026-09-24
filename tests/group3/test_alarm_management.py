import pytest
from pages.alarm_management_page import AlarmManagementPage


# =========================================================
# TRAIN ALARM / ALERT THRESHOLDS (PRIMARY)
# =========================================================

@pytest.mark.sanity
def test_update_train_alarm_thresholds(login_wims_application):
    """
    Verify that Train thresholds can be edited and saved successfully
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.navigate_to_train()
    alarm_page.verify_page_loaded()

    # Edit + Save values
    alarm_page.edit_and_save_train(14, 25, 35, 40)   
   
@pytest.mark.sanity
def test_cancel_train_alarm_edit(login_wims_application):
    """
    Verify cancel functionality works on Train Threshold page
    """

    alarm_page = AlarmManagementPage(login_wims_application)


    alarm_page.click_edit()
    alarm_page.click_cancel()
    alarm_page.click_no_popup()


# =========================================================
# SPEED MONITORING THRESHOLDS (SECOND PHASE)
# =========================================================

@pytest.mark.sanity

def test_update_speed_thresholds(login_wims_application):
    """
    Verify Speed page full functionality:
    - Low/Medium/High fields editable
    - Max Unknown Vehicle Count editable
    - Severity dropdown selection
    - Enable Speed Monitoring checkbox toggle
    - Save success
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.navigate_to_speed()
    alarm_page.verify_page_loaded()

    alarm_page.edit_and_save_speed(15, 25, 35)

@pytest.mark.sanity
def test_cancel_speed_edit(login_wims_application):
    """
    Verify cancel functionality works on Speed Threshold page
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.click_edit()
    alarm_page.click_cancel()
    alarm_page.click_no_popup()

#================================================
# WIMS ALARM/ALERT
#=============#===================================
  
@pytest.mark.sanity
def test_wims_page_load(login_wims_application):
    """
    Verify that WIMS Alarm/Alert page loads successfully
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.navigate_to_wims()
    alarm_page.verify_page_loaded()

  
@pytest.mark.sanity
def test_create_wims_alarm(login_wims_application):
    alarm_page = AlarmManagementPage(login_wims_application)


    alarm_page.create_wims_alarm()
  
@pytest.mark.sanity
def test_edit_wims_description(login_wims_application):
    """
    Verify that WIMS Alarm/Alert description can be edited and saved
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.edit_wims_description("updated description")
 
@pytest.mark.sanity
def test_delete_wims_alarm(login_wims_application):
    """
    Verify that WIMS Alarm/Alert can be deleted successfully
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    # Delete first record
    alarm_page.delete_first_wims_record()

@pytest.mark.sanity
def test_reset_wims_table(login_wims_application):
    """
    Verify reset button clears filters/sorts and table remains visible
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.navigate_to_wims()
    alarm_page.verify_page_loaded()

    alarm_page.click_reset_and_verify()

#========================================================
#WORKFLOW MANAGEMENT 
#========================================================

@pytest.mark.sanity
def test_workflow_page_navigation(login_wims_application):
    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.navigate_to_workflow()
    alarm_page.verify_page_loaded()


@pytest.mark.sanity
def test_add_workflow(login_wims_application):
    alarm_page = AlarmManagementPage(login_wims_application)
    
    alarm_page.add_workflow()


#========================================================
#WIMS ALARM/ALERT SUPPRESSION
#========================================================

@pytest.mark.sanity
def test_alert_suppression_page_load(login_wims_application):
    """
    Verify that Alarm/Alert Suppression page loads successfully
    """

    alarm_page = AlarmManagementPage(login_wims_application)

    # Navigate to submenu
    alarm_page.navigate_to_alert_suppression()

    # Verify page loaded
    alarm_page.verify_page_loaded()

@pytest.mark.sanity
def test_create_alert_suppression(login_wims_application):
    alarm_page = AlarmManagementPage(login_wims_application)

    # Navigate to page
    alarm_page.navigate_to_alert_suppression()
    alarm_page.verify_page_loaded()

    # Create Alert Suppression
    alarm_page.create_alert_suppression()

@pytest.mark.sanity
def test_edit_alert_suppression(login_wims_application):

    alarm_page = AlarmManagementPage(login_wims_application)

    alarm_page.navigate_to_alert_suppression()
    alarm_page.verify_page_loaded()

    # just edit existing row
    alarm_page.edit_alert_suppression_description("updated description")

@pytest.mark.sanity
def test_delete_alert_suppression(login_wims_application):

    alarm_page = AlarmManagementPage(login_wims_application)
    alarm_page.delete_alert_suppression()


@pytest.mark.sanity
def test_reset_alert_suppression(login_wims_application):
    """
    Verify reset button clears filters/sorts and table remains visible
    """

    alarm_page = AlarmManagementPage(login_wims_application)
    alarm_page.click_reset_alert_suppression()

@pytest.mark.sanity
def test_workflow_allocation(login_wims_application):
    alarm_page = AlarmManagementPage(login_wims_application)
    alarm_page.navigate_to_workflow_allocation()
    alarm_page.verify_workflow_allocation()
    alarm_page.verify_download_workflow()
    alarm_page.verify_edit_workflow_allocation()
    alarm_page.click_reset_workflow_allocation()