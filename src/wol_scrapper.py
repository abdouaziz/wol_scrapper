import requests
from bs4 import BeautifulSoup
import itertools
import re
from typing import List
import csv
from tqdm import tqdm
import argparse


def _is_valid_url_sw(href: str) -> bool:

    if str(href).startswith("https://www.wolof-online.com"):
        href = href.replace("https://www.wolof-online.com", "")
        if href != " " and href.startswith("/?"):
            return True

    return False


def get_page_soup(url: str) -> BeautifulSoup:
    """
    Makes a request to a url and creates a beautiful soup oject from the response html

    input:
        :param url: input page url
    returns:
        - page_soup: beautiful soup oject from the response html
    """

    if _is_valid_url_sw(url) == False:
        raise ValueError("Invalid url")

    response = requests.get(url)
    page_html = response.text
    page_soup = BeautifulSoup(page_html, "html.parser")

    return page_soup


def get_valid_href(soup: BeautifulSoup):

    valid_href = []
    pages = soup.findAll("div", {"class": "posts-column"})
    for i in pages:
        for a in i.find_all("a"):
            if (
                a["href"]
                .split("#")[0]
                .replace("https://www.wolof-online.com/", "")
                .startswith("?p=")
            ):
                valid_href.append(a["href"].split("#")[0])

    return list(set(valid_href))


def get_all_text(valid_hrefs, category):

    all_text = []
    for url in valid_hrefs:
        header = get_page_soup(url)
        head_div = header.findAll("strong", {"class": "post"})[0]
        head = re.sub(r"<[^>]*>", "", str(head_div))

        page_soup = get_page_soup(url)
        story_div = page_soup.findAll("div", {"class": "entry"})

        all_paragraphs = [div.findAll("p", recursive=False) for div in story_div]
        all_paragraphs = list(itertools.chain(*all_paragraphs))

        for para in all_paragraphs:
            texts = re.sub(r"<[^>]*>", "", str(para))
            for i in texts.replace(".", "\\n").split("\\n"):
                if i not in [
                    "Tamsir Anne © wolof-online",
                    "anne@wolof-online",
                    "com",
                    "tamsir",
                    "",
                ]:
                    all_text.append([head, i, category, url])

    return all_text


def save_csv(all_text, filename):

    with open(filename + ".csv", "w", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";")
        spamwriter.writerow(["head", "text", "category", "url"])
        for line in tqdm(all_text):
            spamwriter.writerow(line)


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", type=str, default="https://www.wolof-online.com/?cat=4"
    )
    parser.add_argument("--category", type=str, default="politig")
    args = parser.parse_args()

    if args.category is None:
        raise ValueError("Category is required")

    return args


def main():

    args = get_args()
    page_soup = get_page_soup(args.url)
    valid_hrefs = get_valid_href(page_soup)
    all_text = get_all_text(valid_hrefs, args.category)
    save_csv(all_text, args.category)

    print("Done for category: ", args.category)


if __name__ == "__main__":
    main()


# to run the script
# python wol_scrapper.py --url https://www.wolof-online.com/?cat=12 --category nekkin