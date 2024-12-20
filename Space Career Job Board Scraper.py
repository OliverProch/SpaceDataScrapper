import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Specify the URL
url = 'https://spacecareers.uk/jobs?search=&include_expired=false&part_time_only=false&early_careers=true&ordering=-posted_date'

# Specify the directory where you want to save the CSV files
directory_path = 'E:\\Job Board Scrapes\\SpaceCareers\\'

# Create a timestamp to make the filename unique
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Generate a unique filename using the timestamp
filename = f'UK_Space_Jobs_{timestamp}.csv'

# Combine the directory path and filename to create the full file path
file_path = directory_path + filename

# Configure ChromeOptions with the executable path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("executable_path=C:\\Users\\Oliver Cooper\\Desktop\\Job Board Scraper\\chromedriver.exe")  # Replace with the actual path

# Create a WebDriver instance (e.g., Chrome)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
driver.get(url)

# Wait for the page to load (adjust the sleep duration as needed)
time.sleep(5)  # You can adjust the sleep duration as needed

# Function to check if new jobs have loaded
def new_jobs_loaded(prev_page_source, curr_page_source):
    return prev_page_source != curr_page_source

# Scroll down to load more jobs continuously
prev_page_source = ""
while True:
    # Get the current page source
    curr_page_source = driver.page_source
    
    # If new jobs have loaded, update the previous page source and continue scrolling
    if new_jobs_loaded(prev_page_source, curr_page_source):
        prev_page_source = curr_page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to load more jobs
    else:
        break  # No new jobs loaded, exit the loop

# Get the page source
page_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Initialize lists to store data
companies = []
roles = []
entry_professional = []

# Find elements containing job details
job_elements = soup.find_all('div', class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-1au9qiw")

# Extract data and populate the respective lists
for job_element in job_elements:
    # Extract company name
    company_element = job_element.find('a', class_='MuiTypography-root MuiTypography-subtitle1 MuiLink-root MuiLink-underlineHover css-buw4oj', href=True)
    company_name = company_element.text.strip() if company_element else ""

    # Extract role
    role_element = job_element.find('a', class_="MuiTypography-root MuiTypography-h6 MuiLink-root MuiLink-underlineHover css-1t4ustm")
    role = role_element.text.strip() if role_element else ""

    # Extract entry or professional information
    entry_professional_element = job_element.find('p', class_="MuiTypography-root MuiTypography-body1 css-of073w")
    entry_professional_info = entry_professional_element.text.strip() if entry_professional_element else ""

    # Append data to lists
    companies.append(company_name)
    roles.append(role)
    entry_professional.append(entry_professional_info)

# Create a DataFrame
df = pd.DataFrame({"Company": companies, "Role": roles, "Entry or Professional": entry_professional})

# Export data into the new CSV file
df.to_csv(file_path, index=False)

# Print the filename and full file path for reference
print(f"Data saved to {file_path}")

# Close the web driver
driver.quit()
