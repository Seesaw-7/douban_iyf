import requests
from bs4 import BeautifulSoup
import time

# configure the request header, simulating visits from browsers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

base_url = "https://movie.douban.com/people/236635934/wish"

def get_movie_names(url):
    movie_titles = []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # check response code

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all("div", class_="item")
        for item in items:
            title_tag = item.find("em")
            if title_tag:
                movie_titles.append(title_tag.text.strip())

        # keeps going for the next page
        next_link = soup.find("span", class_="next").find("link")
        if next_link:
            next_url = 'https://movie.douban.com' + next_link["href"]
            time.sleep(1)  # 延迟以避免触发反爬虫机制
            movie_titles.extend(get_movie_names(next_url))

    except Exception as e:
        print(f"Exception: {e}")

    return movie_titles

movies = get_movie_names(base_url)
movies_stripped = [m.split(' ')[0] for m in movies]

output_file = "movies_list.txt"
with open(output_file, "w", encoding="utf-8") as f:
    if movies:
        f.write("电影清单:\n")
        for i, movie in enumerate(movies, 1):
            f.write(f"{i}. {movie}\n")
        print(f"Film list saved to: {output_file}")
    else:
        f.write("Failed\n")
        print(f"Failed")

output_file2 = 'movies_list_stripped.txt'
with open(output_file2, "w", encoding="utf-8") as f:
    if movies_stripped:
        for movie in movies_stripped:
            f.write(f"{movie}\n")
        print(f"Film list saved to: {output_file2}")
    else:
        f.write("Failed\n")
        print(f"Failed")
