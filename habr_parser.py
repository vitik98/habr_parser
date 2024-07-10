import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_habr(keyword):
    base_url = "https://habr.com"
    search_url = f"{base_url}/ru/search/?q={keyword}&target_type=posts&order_by=relevance"
    current_page = 1

    results = []

    while True:
        print(f"Parsing page {current_page}...")
        url = f"{base_url}/ru/search/page{current_page}/?q={keyword}&target_type=posts&order_by=relevance"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data from Habr. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all("article", class_="tm-articles-list__item")

        if not articles:
            print("No more articles found.")
            break

        for article in articles:
            title_tag = article.find("a", class_="tm-title__link")
            author_tag = article.find("a", class_="tm-user-info__username")
            date_tag = article.find("time")

            if title_tag and author_tag and date_tag:
                title = title_tag.text.strip()
                author = author_tag.text.strip()
                date = date_tag.get("datetime").split("T")[0]

                results.append({
                    "Заголовок": title,
                    "Автор": author,
                    "Дата публикации": date
                })
            else:
                print("One of the required tags (title, author, date) was not found in the article.")

        next_page_tag = soup.find("a", {"data-test-id": "pagination-next-page"})
        if next_page_tag and 'href' in next_page_tag.attrs:
            current_page += 1
        else:
            break

    return results

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    keyword = input("Введите ключевое слово для поиска на Habr: ")
    results = parse_habr(keyword)
    if results:
        save_to_excel(results, "habr_results.xlsx")
