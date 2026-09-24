from playwright.sync_api import Page, expect

def wait_for_element_visible(page: Page, selector: str, timeout: int = 10000):
    """Wait for an element to be visible on the page."""
    element = page.locator(selector)
    expect(element).to_be_visible(timeout=timeout)
    return element

def wait_for_element_hidden(page: Page, selector: str, timeout: int = 10000):
    """Wait for an element to be hidden or removed from the DOM."""
    element = page.locator(selector)
    expect(element).to_be_hidden(timeout=timeout)
