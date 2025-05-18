from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class NaukriAutoApply:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self, email, password):
        try:
            print("Opening Naukri.com...")
            self.driver.get("https://www.naukri.com/nlogin/login")
            print("Please wait while the page loads...")
            
            # Wait for and fill in email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "usernameField"))
            )
            email_field.send_keys(email)
            print("Email entered successfully")
            
            # Fill in password
            password_field = self.driver.find_element(By.ID, "passwordField")
            password_field.send_keys(password)
            print("Password entered successfully")
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_button.click()
            print("Login button clicked")
            
            # Wait for login to complete and redirect to homepage
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def search_jobs(self, keywords, locations, experience, sort_by="Recommended"):
        try:
            # Navigate to Naukri's homepage
            print("Navigating to Naukri homepage...")
            self.driver.get("https://www.naukri.com")
            time.sleep(5)  # Wait for page to load
            
            # Click on the search bar
            print("Clicking on search bar...")
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nI-gNb-sb__placeholder"))
            )
            self.driver.execute_script("arguments[0].click();", search_bar)
            print("Search bar clicked successfully")
            time.sleep(2)  # Wait for search interface to appear
            
            # Enter keywords (comma-separated)
            print("Entering keywords...")
            keyword_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter keyword / designation / companies']"))
            )
            keyword_input.clear()
            keyword_input.send_keys(keywords)
            print("Keywords entered successfully")
            
            # Enter experience
            print("Entering experience...")
            exp_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='experienceDD']"))
            )
            exp_input.click()
            time.sleep(1)
            
            # Find and click the experience option
            exp_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'dropdownPrimary')]//span[contains(text(), '{experience}')]"))
            )
            exp_option.click()
            print("Experience selected successfully")
            
            # Enter locations (comma-separated)
            print("Entering locations...")
            location_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter location']"))
            )
            location_input.clear()
            location_input.send_keys(locations)
            print("Locations entered successfully")
            
            # Click search button
            print("Clicking search button...")
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nI-gNb-sb__icon-wrapper"))
            )
            search_button.click()
            print("Search initiated")
            
            # Wait for results to load
            time.sleep(10)  # Wait for results to appear
            
            # Click on sort by dropdown using JavaScript
            print("Selecting sort order...")
            sort_by_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter-sort"))
            )
            self.driver.execute_script("arguments[0].click();", sort_by_element)
            time.sleep(2)
            
            # Select the desired sort option using JavaScript
            sort_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//li[@class='styles_ss__menu-item__T4rgB']//a[@data-id='filter-sort-{sort_by[0].lower()}']"))
            )
            self.driver.execute_script("arguments[0].click();", sort_option)
            print(f"Sorted by {sort_by}")
            
            # Wait for results to load
            time.sleep(5)
            
            # Lists to track different types of jobs
            easy_apply_jobs = []
            external_apply_jobs = []
            
            # Process all jobs on 3 pages
            print("Processing job listings...")
            total_jobs_processed = 0
            
            for page in range(1, 3):  # Process 3 pages
                try:
                    print(f"\nProcessing page {page}")
                    
                    # Get all job titles on current page
                    job_links = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'title')]")
                    
                    if not job_links:
                        print(f"No jobs found on page {page}")
                        break
                    
                    # Process all jobs on current page
                    for job_link in job_links:
                        try:
                            print(f"\nProcessing job {total_jobs_processed + 1}")
                            
                            # Store the current window handle
                            main_window = self.driver.current_window_handle
                            
                            # Get job title before clicking
                            job_title = job_link.text
                            
                            # Click the job link
                            job_link.click()
                            print("Clicked on job")
                            
                            # Wait for new tab to open
                            time.sleep(2)
                            
                            # Switch to the new tab
                            new_window = [window for window in self.driver.window_handles if window != main_window][0]
                            self.driver.switch_to.window(new_window)
                            
                            # Check for apply button type
                            try:
                                # First check for "Apply on company site" button
                                company_site_button = WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.ID, "company-site-button"))
                                )
                                print("Found 'Apply on company site' button - skipping")
                                external_apply_jobs.append({
                                    'title': job_title,
                                    'url': self.driver.current_url
                                })
                                
                            except:
                                # If no company site button, look for easy apply
                                try:
                                    apply_button = WebDriverWait(self.driver, 10).until(
                                        EC.element_to_be_clickable((By.ID, "apply-button"))
                                    )
                                    apply_button.click()
                                    print("Clicked Easy Apply button")
                                    easy_apply_jobs.append({
                                        'title': job_title,
                                        'url': self.driver.current_url
                                    })
                                    
                                    # Wait for 5 seconds after clicking apply
                                    time.sleep(5)
                                    
                                except Exception as e:
                                    print(f"Could not find any apply button: {str(e)}")
                            
                            # Close the current tab
                            self.driver.close()
                            
                            # Switch back to the main window
                            self.driver.switch_to.window(main_window)
                            print("Returned to search results")
                            
                            total_jobs_processed += 1
                            
                            # Wait for search results to load again
                            time.sleep(2)
                            
                        except Exception as e:
                            print(f"Error processing job: {str(e)}")
                            # If we're on a new tab, close it and switch back
                            if len(self.driver.window_handles) > 1:
                                self.driver.close()
                                self.driver.switch_to.window(main_window)
                            continue
                    
                    # Go to next page if not on last page
                    if page < 3:
                        try:
                            # Find and click the next page number
                            next_page = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, f"//div[@class='styles_pages__v1rAK']//a[text()='{page + 1}']"))
                            )
                            next_page.click()
                            print(f"Navigating to page {page + 1}")
                            time.sleep(5)  # Wait for new page to load
                        except Exception as e:
                            print(f"Error navigating to page {page + 1}: {str(e)}")
                            break
                
                except Exception as e:
                    print(f"Error on page {page}: {str(e)}")
                    continue
            
            # Print summary of processed jobs
            print("\n=== Job Application Summary ===")
            print(f"Total jobs processed: {total_jobs_processed}")
            print(f"\nEasy Apply Jobs ({len(easy_apply_jobs)}):")
            for job in easy_apply_jobs:
                print(f"- {job['title']}")
                print(f"  URL: {job['url']}")
            
            print(f"\nExternal Apply Jobs ({len(external_apply_jobs)}):")
            for job in external_apply_jobs:
                print(f"- {job['title']}")
                print(f"  URL: {job['url']}")
                print("  Note: This job requires application on company website")
            
            return {
                'total_processed': total_jobs_processed,
                'easy_apply_jobs': easy_apply_jobs,
                'external_apply_jobs': external_apply_jobs
            }
            
        except Exception as e:
            print(f"Search failed: {str(e)}")
            print("Current URL:", self.driver.current_url)
            return None

    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    print("Starting Naukri Auto Apply...")
    
    # Keep your hardcoded values
    email = "abx@gmail.com"
    password = "abx@abx"
    keywords = "python, software developer, healthcare"
    locations = "hyderabad, bangalore, pune"
    experience = 2
    
    print("\nSelect sort order:")
    print("1. Recommended")
    print("2. Relevance")
    print("3. Date")
    sort_choice = input("Enter your choice (1-3): ")
    
    sort_options = {
        "1": "p",  # Recommended
        "2": "r",  # Relevance
        "3": "f"   # Date
    }
    
    sort_by = sort_options.get(sort_choice, "p")
    
    # Initialize and run the auto apply system
    auto_apply = NaukriAutoApply()
    
    try:
        if auto_apply.login(email, password):
            print("Login successful!")
            auto_apply.search_jobs(keywords, locations, experience, sort_by)
            input("Press Enter to close the browser...")
        else:
            print("Login failed. Please check your credentials.")
    finally:
        auto_apply.close()

if __name__ == "__main__":
    main() 