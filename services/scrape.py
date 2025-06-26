from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def scrape_page():
    # Launch a new Chrome browser instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Navigate to the page
    driver.get('https://www.gaf.com/en-us/roofing-contractors/residential?distance=25')
    
    # Wait for page to load
    time.sleep(3)
    
    # Take screenshot for debugging
    driver.save_screenshot("after_page_load.png")
    
    wait = WebDriverWait(driver, 15)
    
    # Step 1: Enter address and select from dropdown
    # First scroll down to make sure the address field is visible
    driver.execute_script("window.scrollTo(0, 300);")  # Scroll down 300px
    time.sleep(2)
    
    # Wait for the address input to be both present and clickable
    address_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#unique-id-residential-us.field__input.pac-target-input')))
    
    # Try to click using JavaScript if regular click fails
    try:
        address_input.click()
    except:
        driver.execute_script("arguments[0].click();", address_input)
    
    time.sleep(1)
    
    # Clear the field using JavaScript
    driver.execute_script("arguments[0].value = '';", address_input)
    time.sleep(1)
    
    # Type the address using JavaScript
    driver.execute_script("arguments[0].value = '455 West Broadway, New York, NY, USA';", address_input)
    # Also trigger the input event
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", address_input)
    
    time.sleep(2)  # Wait for autocomplete dropdown to appear
    
    # Click the first element in the autocomplete dropdown
    try:
        dropdown_selectors = [
            '.pac-item:first-child',
            '.pac-container .pac-item:first-child',
            '[role="option"]:first-child',
            '.autocomplete-item:first-child',
            '.dropdown-item:first-child'
        ]
        
        dropdown_clicked = False
        for selector in dropdown_selectors:
            try:
                dropdown_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                dropdown_item.click()
                dropdown_clicked = True
                print(f"Clicked dropdown item with selector: {selector}")
                break
            except:
                continue
        
        if not dropdown_clicked:
            address_input.send_keys(Keys.ENTER)
            print("Pressed Enter to select address")
            
    except Exception as e:
        print(f"Error clicking dropdown: {e}")
        address_input.send_keys(Keys.ENTER)
    
    time.sleep(2)
    
    # Click "Get matched" button
    get_matched_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get matched')]")))
    get_matched_button.click()
    time.sleep(2)
    
    # Step 2: Select project timeline - choose "Immediately"
    try:
        immediately_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Immediately')]")))
        immediately_button.click()
        print("Selected 'Immediately' for project timeline")
    except:
        print("Could not find 'Immediately' button, trying alternative selectors")
        # Try alternative selectors
        timeline_selectors = [
            "//button[contains(text(), 'immediately')]",
            "//div[contains(text(), 'Immediately')]",
            "//label[contains(text(), 'Immediately')]"
        ]
        for selector in timeline_selectors:
            try:
                element = driver.find_element(By.XPATH, selector)
                element.click()
                print(f"Selected timeline with selector: {selector}")
                break
            except:
                continue
    
    time.sleep(1)
    
    # Click Next after timeline selection
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]")))
    next_button.click()
    time.sleep(2)
    
    # Step 3: Select insurance claim - choose "No"
    try:
        no_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label.radio-field__label[for*=":r2:-1"]')))
        no_button.click()
        print("Selected 'No' for insurance claim")
    except:
        print("Could not find 'No' button for insurance claim, trying alternative selectors")
        # Try alternative selectors
        no_selectors = [
            'label.radio-field__label:contains("No")',
            'label[for*=":r2:-1"]',
            'input[value="no"]',
            'input[id*="no"]'
        ]
        for selector in no_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                print(f"Selected 'No' with selector: {selector}")
                break
            except:
                continue
    
    time.sleep(1)
    
    # Click Next after insurance selection
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]")))
    next_button.click()
    time.sleep(2)
    
    # Step 4: Fill out contact information
    # First Name
    first_name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="firstName"], input[placeholder*="First"], input[id*="first"]')))
    first_name_input.send_keys("John")
    
    # Last Name
    last_name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="lastName"], input[placeholder*="Last"], input[id*="last"]')))
    last_name_input.send_keys("Doe")
    
    # Email
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"], input[name="email"], input[placeholder*="Email"]')))
    email_input.send_keys("john.doe@example.com")
    
    # Phone
    phone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="tel"], input[name="phone"], input[placeholder*="Phone"]')))
    phone_input.send_keys("555-123-4567")
    
    time.sleep(1)
    
    # Check the checkbox (usually for terms/consent)
    try:
        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="checkbox"], .checkbox input')))
        if not checkbox.is_selected():
            checkbox.click()
        print("Checked the consent checkbox")
    except:
        print("Could not find or click checkbox")
    
    time.sleep(1)
    
    # Scroll down to make sure the "Get results" button is visible
    driver.execute_script("window.scrollBy(0, 200);")  # Scroll down just 200px instead of to bottom
    time.sleep(2)
    
    # Take a screenshot to see what's on the page
    driver.save_screenshot("before_get_results.png")
    
    # Print all button text on the page to help debug
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print("Available buttons on the page:")
    for i, button in enumerate(buttons):
        try:
            text = button.text.strip()
            if text:
                print(f"  {i+1}. '{text}'")
        except:
            pass
    
    # Try different selectors for the "Get results" button
    get_results_selectors = [
        "//button[contains(@class, 'btn--primary') and contains(text(), 'Get Results')]",
        "//button[contains(@class, 'quiz-form__btn')]",
        "//button[contains(text(), 'Get Results')]",
        "//button[contains(text(), 'Get Results')]",
        "//button[contains(text(), 'Submit')]",
        "//button[contains(text(), 'Continue')]",
        "//button[contains(text(), 'Find')]",
        "//button[contains(text(), 'Search')]",
        "//button[contains(text(), 'Match')]",
        "//button[contains(text(), 'Submit Form')]",
        "//button[@type='submit']"
    ]
    
    get_results_button = None
    for selector in get_results_selectors:
        try:
            get_results_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            print(f"Found button with selector: {selector}")
            break
        except:
            continue
    
    if get_results_button:
        get_results_button.click()
        print("Clicked the results button")
        time.sleep(3)  # Wait for page to load
        
        # Navigate to the first contractor card
        try:
            # Wait for contractor cards to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.small-contractor-card')))
            
            # Find the first contractor card
            first_contractor = driver.find_element(By.CSS_SELECTOR, '.small-contractor-card')
            
            # Click on the contractor name link to navigate to their profile
            contractor_name_link = first_contractor.find_element(By.CSS_SELECTOR, '.small-contractor-card__name a')
            contractor_name = contractor_name_link.text.strip()
            print(f"Navigating to contractor: {contractor_name}")
            
            contractor_name_link.click()
            time.sleep(3)  # Wait for contractor profile page to load
            
            print(f"Now on contractor profile page for: {contractor_name}")
            
        except Exception as e:
            print(f"Could not navigate to first contractor: {e}")
            # Try alternative selectors
            try:
                first_contractor_link = driver.find_element(By.CSS_SELECTOR, '.small-contractor-card a[href*="contractors"]')
                first_contractor_link.click()
                print("Clicked first contractor link using alternative selector")
                time.sleep(3)
            except:
                print("Could not find any contractor links")
    else:
        print("Could not find any submit button")
        # Try to find any clickable button
        try:
            any_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button.btn, button.button")
            any_button.click()
            print("Clicked a generic submit button")
        except:
            print("No buttons found at all")
    
    time.sleep(3)
    
    # Take screenshot after completing the form
    driver.save_screenshot("after_form_completion.png")
    print(f"Current URL: {driver.current_url}")
    
    # Wait for results to load and scrape contractor data
    try:
        # Wait for contractor results to appear
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.contractor-card, .result-card, .listing-item')))
        
        # Find all contractor cards
        contractor_cards = driver.find_elements(By.CSS_SELECTOR, '.contractor-card, .result-card, .listing-item')
        
        print(f"\nFound {len(contractor_cards)} contractors:")
        for i, card in enumerate(contractor_cards, 1):
            try:
                # Try to extract name and contact info
                name = card.find_element(By.CSS_SELECTOR, '.name, .contractor-name, h3, h4').text
                print(f"{i}. {name}")
            except:
                print(f"{i}. Contractor (name not found)")
                
    except Exception as e:
        print(f"Could not scrape contractor results: {e}")
    
    # Keep browser open for manual inspection
    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    scrape_page()
    