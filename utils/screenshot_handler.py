import os
from datetime import datetime
from config.settings import settings
 
def capture_screenshot(page, test_name):
    """Captures a screenshot of the current page."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)
    screenshot_path = os.path.join(settings.SCREENSHOTS_DIR, f"{test_name}_{timestamp}.png")
    page.screenshot(path=screenshot_path, full_page=True)
    return screenshot_path