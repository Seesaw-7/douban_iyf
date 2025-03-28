from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.parse

# Base search URL
base_url = "https://www.iyf.tv/search/"
local_chorme_driver_path = "/Users/mac/Downloads/chromedriver-mac-x64/chromedriver"

# Function to read movies from a file
def read_movie_list(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            movies = [line.strip() for line in f if line.strip()]
        return movies
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

# Function to check if a movie has valid search results using Selenium
def check_movie_results_selenium(movie_name):
    # Encode the movie name for the URL
    search_url = f"{base_url}{urllib.parse.quote(movie_name)}?cid=0,1,3&tag=&label=%E7%94%B5%E5%BD%B1"
    print(f"Checking: {search_url}")
    
    # Set up Selenium WebDriver
    options = Options()
    # options.headless = True  # Run in headless mode
    driver = webdriver.Chrome(service=Service(local_chorme_driver_path), options=options)
    
    try:
        driver.get(search_url)
        driver.implicitly_wait(2)  # Wait for JavaScript-rendered content to load
        
        no_results = driver.find_elements(By.CLASS_NAME, 'no-item-image')
        video_cards = driver.find_elements(By.CLASS_NAME, 'video-detail')
        
        if no_results:
            print(f"No results found for search term: {movie_name}")
            return False
        elif video_cards:
            first_movie_element = driver.find_element(By.CSS_SELECTOR, "h5.d-inline")
            first_movie_name = first_movie_element.text
            if first_movie_name == movie_name:
                print(f"Results found for search term: {movie_name}")
                return True
            else:
                print("No")
                return False
        else:
            print(f"No definitive results for: {movie_name}")
            return False
    except Exception as e:
        print(f"Error checking movie '{movie_name}': {e}")
        return False
    finally:
        driver.quit()

# Main function to process movies and save results
def main(input_file, output_file):
    movies = read_movie_list(input_file)
    if not movies:
        return

    with open(output_file, "w", encoding="utf-8") as f:
        for movie in movies:
            is_valid = check_movie_results_selenium(movie)
            result = f"{movie}: {'Found' if is_valid else 'Not Found'}"
            print(result)
            if is_valid:
                f.write(movie + "\n")

input_file = "movies_search_results.txt"
output_file = "available.txt"

main(input_file, output_file)
print(f"Results saved to {output_file}")
