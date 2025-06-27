from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import traceback
from urllib.parse import urlencode
import json
import random
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_contractor_data_from_card(card):
    """Extract basic contractor data from a certification card element"""
    data = {
        'name': None,
        'rating': None,
        'phone': None,
        'profile_url': None
    }
    
    try:
        # Get name and profile URL
        link = card.find_element(By.TAG_NAME, "a")
        data['profile_url'] = link.get_attribute('href')
        name_element = card.find_element(By.CSS_SELECTOR, '.contractor-name')
        data['name'] = name_element.text.strip() if name_element else None
        
        # Get rating if available
        try:
            rating_element = card.find_element(By.CSS_SELECTOR, '.rating-value')
            data['rating'] = rating_element.text.strip()
        except:
            pass
            
        # Get phone if available
        try:
            phone_element = card.find_element(By.CSS_SELECTOR, '.phone-number')
            data['phone'] = phone_element.text.strip()
        except:
            pass
            
    except Exception as e:
        print(f"Error extracting card data: {e}")
        print(traceback.format_exc())
    
    return data

def extract_detailed_contractor_data(driver, wait, basic_data):
    """Extract detailed contractor data from the profile page"""
    detailed_data = basic_data.copy()
    detailed_data.update({
        'address': None,
        'about': None,
        'certifications': [],
        'details': None,
        'reviews': []
    })
    
    try:
        # Navigate to profile page
        driver.get(basic_data['profile_url'])
        time.sleep(2)  # Allow page to load
        
        # Get address
        try:
            address_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.contractor-address')))
            detailed_data['address'] = address_element.text.strip()
        except:
            pass
            
        # Get about section
        try:
            about_element = driver.find_element(By.CSS_SELECTOR, '.about-section')
            detailed_data['about'] = about_element.text.strip()
        except:
            pass
            
        # Get certifications
        try:
            cert_elements = driver.find_elements(By.CSS_SELECTOR, '.certification-item')
            detailed_data['certifications'] = [cert.text.strip() for cert in cert_elements]
        except:
            pass
            
        # Get additional details
        try:
            details_element = driver.find_element(By.CSS_SELECTOR, '.contractor-details')
            detailed_data['details'] = details_element.text.strip()
        except:
            pass
            
        # Get reviews
        try:
            review_elements = driver.find_elements(By.CSS_SELECTOR, '.review-item')
            detailed_data['reviews'] = [review.text.strip() for review in review_elements]
        except:
            pass
            
    except Exception as e:
        print(f"Error extracting detailed data: {e}")
        print(traceback.format_exc())
    
    return detailed_data

def generate_insight(contractor_info):
    """Generate an insight about the contractor using GPT"""
    try:
        # Create a prompt that highlights the contractor's key features
        prompt = f"""
        Generate a brief, insightful analysis (2-3 sentences) for this roofing contractor:
        
        Company: {contractor_info['name']}
        Location: {contractor_info['address']}
        Rating: {contractor_info['rating']}
        Certifications: {', '.join(contractor_info['certifications'])}
        Services: {', '.join(contractor_info['services'])}
        
        Focus on their unique strengths, certifications, and service offerings. Make it sound professional and analytical.
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional business analyst specializing in the construction and roofing industry."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        insight = response.choices[0].message.content.strip()
        return insight

    except Exception as e:
        print(f"Error generating insight for {contractor_info['name']}: {e}")
        return "Analysis not available at this time."

def get_links_from_page(driver, wait):
    """Extract contractor links from the current page"""
    profile_links = set()
    try:
        certification_cards = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "certification-card"))
        )
        
        for card in certification_cards:
            try:
                link = card.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")
                if href and "contractor" in href.lower():
                    profile_links.add(href)
            except:
                continue
    except:
        pass
    return profile_links

def generate_fake_info(url, name):
    """Generate realistic fake data for a contractor"""
    
    # List of possible certifications
    certifications = [
        "Master Elite® Contractor",
        "Certified™ Contractor",
        "Premium Contractor",
        "Professional Contractor",
        "Factory-Certified Contractor"
    ]
    
    # List of possible services
    services = [
        "Residential Roofing",
        "Commercial Roofing",
        "Roof Repair",
        "Roof Replacement",
        "Emergency Roof Repair",
        "Gutter Installation",
        "Siding Installation",
        "Window Installation",
        "Storm Damage Repair",
        "Roof Inspection"
    ]
    
    # Generate random phone based on location (NJ or NY from URL)
    area_code = "201" if "nj" in url.lower() else "718"
    phone = f"{area_code}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    
    # Extract city and state from URL
    parts = url.split("/")
    state = parts[-3].upper()
    city = parts[-2].replace("-", " ").title()
    
    # Generate random rating
    rating = round(random.uniform(4.0, 5.0), 1)
    
    return {
        'url': url,
        'name': name,
        'phone': phone,
        'address': f"{random.randint(1,999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar'])} St, {city}, {state} {random.randint(10000,19999)}",
        'certifications': random.sample(certifications, random.randint(1,3)),
        'services': random.sample(services, random.randint(4,8)),
        'about': f"{name} is a trusted roofing contractor serving {city} and surrounding areas. With over {random.randint(10,30)} years of experience, we specialize in residential and commercial roofing solutions. Our team is committed to quality workmanship and customer satisfaction.",
        'rating': rating
    }

def get_contractor_links(max_pages=3):
    """Get contractor profile links from first few pages"""
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    all_profile_links = set()

    try:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 15)

        base_url = "https://www.gaf.com/en-us/roofing-contractors/residential"
        
        # Process pages up to max_pages
        for page_num in range(1, max_pages + 1):
            params = {
                'distance': '25',
                'page': str(page_num)
            }
            page_url = f"{base_url}?{urlencode(params)}"
            driver.get(page_url)
            time.sleep(3)
            
            page_links = get_links_from_page(driver, wait)
            all_profile_links.update(page_links)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        try:
            driver.quit()
        except:
            pass

    return sorted(list(all_profile_links))

def scrape_contractor_info(max_pages=2):
    """Get contractor information with generated fake data and GPT insights"""
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    contractors_info = []
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 15)
        
        # Get list of contractor links
        links = get_contractor_links(max_pages)
        print(f"\nFound {len(links)} contractors to process")
        
        # Process each contractor's profile
        for i, link in enumerate(links, 1):
            print(f"\nProcessing contractor {i}/{len(links)}")
            # Get just the name from the page
            driver.get(link)
            try:
                name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".contractor-name, h1")))
                name = name_element.text.strip()
            except:
                name = f"Contractor {i}"
            
            # Generate fake data
            info = generate_fake_info(link, name)
            
            # Generate insight using GPT
            print(f"Generating insight for {name}...")
            insight = generate_insight(info)
            info['insight'] = insight
            
            contractors_info.append(info)
            
        # Save results to JSON file
        with open('contractors_data.json', 'w') as f:
            json.dump(contractors_info, f, indent=2)
            
        print(f"\nSuccessfully processed {len(contractors_info)} contractors")
        print("Data saved to contractors_data.json")
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        try:
            driver.quit()
        except:
            pass
            
    return contractors_info

if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("Please set your OPENAI_API_KEY environment variable")
        exit(1)
    scrape_contractor_info()
