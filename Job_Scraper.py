# Import necessary libraries for working with CSV files, parsing HTML, making HTTP requests, and logging
import csv
from bs4 import BeautifulSoup
import requests
import logging

# Function to save job data to a CSV file
def save_to_csv(jobs_data, filename):
  """
  Saves a list of job postings (represented as dictionaries) to a CSV file.

  Args:
      jobs_data: A list of dictionaries, where each dictionary represents a job posting.
      filename: The path to the CSV file where the data will be saved.
  """
  try:
    # Open the CSV file in write mode with newline='' to avoid extra blank lines
    with open(filename, 'w', newline='') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=['Company Name', 'Required Skills', 'Published on', 'More Info'])
      # Write the header row with field names
      writer.writeheader()
      # Write each job detail as a row in the CSV file
      writer.writerows(jobs_data)
  except Exception as e:
    # Catch any errors during CSV writing and log them
    logging.error(f"Error saving to CSV: {e}")

# Function to scrape job postings from a website
def scrape_jobs():
  """
  Scrapes job postings for "Machine Learning" from a website and returns extracted data.

  Returns:
      A list of dictionaries, where each dictionary represents a job posting with details.
  """
  url = 'https://www.timesjobs.com/candidate/job-search.html'  # Base URL for job search
  all_jobs_data = []

  # Configure logging to record events in a file named "scraping.log"
  logging.basicConfig(filename='scraping.log', level=logging.DEBUG)

  # Loop through multiple pages of search results (adjust range based on pagination)
  for page_num in range(1, 24):
    params = {
      'searchType': 'personalizedSearch',
      'from': 'submit',
      'searchTextSrc': 'as',
      'searchTextText': '"Machine Learning"',
      'txtKeywords': '"Machine Learning"',
      'txtLocation': '',
      'sequence': page_num
    }

    try:
      # Send a GET request to fetch the HTML content for the current page
      html_text = requests.get(url, params=params).text
      soup = BeautifulSoup(html_text, 'lxml')

      # Find all elements containing individual job postings using a CSS selector
      jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')  # Adjust selector if needed

      for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text
        company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
        skills = job.find('span', class_='srp-skills').text.replace(' ', '')
        more_info = job.header.h2.a['href']

        # Create a dictionary to store the extracted job details
        job_details = {
          'Company Name': company_name.strip(),
          'Required Skills': skills.strip(),
          'Published on': published_date,
          'More Info': more_info
        }
        all_jobs_data.append(job_details)
    except Exception as e:
      # Catch errors during scraping of a page and log them
      logging.error(f"Error scraping page {page_num}: {e}")

  return all_jobs_data

# Main execution block to run the scraping and saving process
if __name__ == '__main__':
  jobs_data = scrape_jobs()
  save_to_csv(jobs_data, 'Job_Postings.csv')  # Replace with your desired file path

  # Print the extracted job data to the console (optional)
  '''
  if jobs_data:
    for job in jobs_data:
      print(f"Company Name: {job['Company Name']}")
      print(f"Required Skills: {job['Required Skills']}")
      print(f'Published on: {job['Published on']}')
      print(f'More Info: {job['More Info']}')
      print('')
  '''    