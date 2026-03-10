"""
Selenium UI tests for the Notes application.
Run these tests with: python manage.py test notes.tests_selenium
or directly with: python selenium_tests.py
"""

from django.test import LiveServerTestCase, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


class SeleniumNoteTests(StaticLiveServerTestCase):
    """Selenium UI tests for Notes application."""

    @classmethod
    def setUpClass(cls):
        """Set up Selenium WebDriver for all tests."""
        super().setUpClass()
        # Configure Chrome options for headless mode (optional)
        options = webdriver.ChromeOptions()
        # Uncomment the next line to run in headless mode (no visible browser)
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            cls.driver = webdriver.Chrome(options=options)
        except Exception:
            # If Chrome is not available, try Firefox
            try:
                cls.driver = webdriver.Firefox()
            except Exception:
                raise Exception("Neither Chrome nor Firefox WebDriver is available. Please install one.")
        
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """Close the Selenium WebDriver."""
        cls.driver.quit()
        super().tearDownClass()

    def test_create_note_success(self):
        """Test successful note creation via UI."""
        # Navigate to create note page
        self.driver.get(f"{self.live_server_url}/create/")
        
        # Wait for form to be present
        wait = WebDriverWait(self.driver, 10)
        title_field = wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
        
        # Fill in the form
        title_field.send_keys("Selenium Test Note")
        
        description_field = self.driver.find_element(By.ID, 'id_description')
        description_field.send_keys("This is a test note created by Selenium UI automation tests.")
        
        # Submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Wait for redirect to note list
        wait.until(EC.url_changes(f"{self.live_server_url}/create/"))
        
        # Verify we're on the note list page
        self.assertIn("/", self.driver.current_url)
        
        # Verify the note appears in the list
        wait.until(EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'Selenium Test Note')]")))
        self.assertIn("Selenium Test Note", self.driver.page_source)

    def test_create_note_view_detail(self):
        """Test viewing note details after creation."""
        # Create a note
        self.driver.get(f"{self.live_server_url}/create/")
        wait = WebDriverWait(self.driver, 10)
        
        title_field = wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
        title_field.send_keys("Detail View Test Note")
        
        description_field = self.driver.find_element(By.ID, 'id_description')
        test_description = "This is a test note for checking the detail view functionality."
        description_field.send_keys(test_description)
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Wait for note list
        wait.until(EC.url_changes(f"{self.live_server_url}/create/"))
        
        # Click on the note to view details
        view_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='btn btn-sm btn-outline-primary']")
        ))
        view_button.click()
        
        # Verify detail page content
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertIn("Detail View Test Note", self.driver.page_source)
        self.assertIn(test_description, self.driver.page_source)

    def test_short_description_validation_error(self):
        """Test that form shows error when description is too short."""
        # Navigate to create note page
        self.driver.get(f"{self.live_server_url}/create/")
        
        wait = WebDriverWait(self.driver, 10)
        title_field = wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
        
        # Fill in form with short description
        title_field.send_keys("Short Title")
        
        description_field = self.driver.find_element(By.ID, 'id_description')
        description_field.send_keys("Short")  # Only 5 characters, less than 10
        
        # Submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Wait for error message to appear
        try:
            error_element = wait.until(
                EC.presence_of_element_located((By.ID, 'descriptionError'))
            )
            error_text = error_element.text
            self.assertIn("at least 10 characters", error_text)
        except TimeoutException:
            # Error might be displayed differently, check page source
            self.assertIn("at least 10 characters", self.driver.page_source)

    def test_empty_description_validation_error(self):
        """Test that form shows error when description is empty."""
        # Navigate to create note page
        self.driver.get(f"{self.live_server_url}/create/")
        
        wait = WebDriverWait(self.driver, 10)
        title_field = wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
        
        # Fill in only title, leave description empty
        title_field.send_keys("No Description Note")
        
        # Submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Look for error message
        page_source = self.driver.page_source
        # Should still be on create page with errors
        self.assertIn("This field is required", page_source or "at least 10 characters" in page_source)

    def test_empty_title_validation_error(self):
        """Test that form shows error when title is empty."""
        # Navigate to create note page
        self.driver.get(f"{self.live_server_url}/create/")
        
        wait = WebDriverWait(self.driver, 10)
        
        description_field = wait.until(EC.presence_of_element_located((By.ID, 'id_description')))
        description_field.send_keys("This is a valid description with enough characters.")
        
        # Don't fill title, submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Should still be on form with error
        page_source = self.driver.page_source
        self.assertIn("This field is required", page_source)

    def test_navigation_between_pages(self):
        """Test navigation between different pages."""
        # Go to home page
        self.driver.get(f"{self.live_server_url}/")
        
        wait = WebDriverWait(self.driver, 10)
        
        # Check navigation links exist
        create_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Create Note')]")
        ))
        self.assertTrue(create_link.is_displayed())
        
        # Click Create Note link
        create_link.click()
        
        # Verify we're on create page
        wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
        self.assertIn("/create/", self.driver.current_url)
        
        # Click back to All Notes
        all_notes_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'All Notes')]")
        ))
        all_notes_link.click()
        
        # Verify we're back on list page
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='All Notes']")))

    def test_create_multiple_notes(self):
        """Test creating multiple notes in sequence."""
        notes_to_create = [
            ("Note 1", "This is the first test note created by Selenium."),
            ("Note 2", "This is the second test note with more detailed content."),
            ("Note 3", "This is the third test note to verify multiple creations work correctly."),
        ]
        
        for title, description in notes_to_create:
            # Navigate to create page
            self.driver.get(f"{self.live_server_url}/create/")
            
            wait = WebDriverWait(self.driver, 10)
            title_field = wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
            
            # Fill and submit
            title_field.send_keys(title)
            description_field = self.driver.find_element(By.ID, 'id_description')
            description_field.send_keys(description)
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            # Wait for list page to load
            wait.until(EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{title}')]")))
        
        # Go to list page and verify all notes are there
        self.driver.get(f"{self.live_server_url}/")
        wait = WebDriverWait(self.driver, 10)
        
        for title, _ in notes_to_create:
            wait.until(EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{title}')]")))
            self.assertIn(title, self.driver.page_source)


class SeleniumFormFieldsTest(StaticLiveServerTestCase):
    """Test form fields and attributes."""

    @classmethod
    def setUpClass(cls):
        """Set up Selenium WebDriver."""
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            cls.driver = webdriver.Chrome(options=options)
        except Exception:
            cls.driver = webdriver.Firefox()
        
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """Close the WebDriver."""
        cls.driver.quit()
        super().tearDownClass()

    def test_form_field_placeholders(self):
        """Test that form fields have proper placeholders."""
        self.driver.get(f"{self.live_server_url}/create/")
        
        wait = WebDriverWait(self.driver, 10)
        title_field = wait.until(EC.presence_of_element_located((By.ID, 'id_title')))
        
        # Check placeholder text
        self.assertEqual(
            title_field.get_attribute('placeholder'),
            'Enter note title'
        )
        
        description_field = self.driver.find_element(By.ID, 'id_description')
        self.assertIn(
            'description',
            description_field.get_attribute('placeholder').lower()
        )

    def test_form_has_csrf_token(self):
        """Test that form includes CSRF protection."""
        self.driver.get(f"{self.live_server_url}/create/")
        
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, 'csrfmiddlewaretoken')))
        
        csrf_token = self.driver.find_element(By.NAME, 'csrfmiddlewaretoken')
        self.assertTrue(csrf_token.is_displayed() or csrf_token.get_attribute('type') == 'hidden')


if __name__ == '__main__':
    import unittest
    unittest.main()
