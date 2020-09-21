import urllib.request, urllib.error
import re
import time
from bs4 import BeautifulSoup
from collections import defaultdict
from string import punctuation
from gensim.summarization import summarize
from src.link_analysis import get_visited_links
from model.model_keyword import Links, KeywordsLink
from model.base_model import BaseModel
from settings import BASE_URL


def get_urls(soup, url_queue, visited):
    """ Retrieves all the hyperlinks from the page source soup and appends to the url_queue,
    if the link is not in visited list.

    Args:
        soup (BeautifulSoup): a html doc in BeautifulSoup format
        url_queue (list): a list of non-visited links
        visited (dict): a dict of visited links
    Returns:
        None
    """

    for item in soup.find_all('a'):
        link = item.get('href')
        # print(type(link))
        if link is None:
            pass
        elif link in visited.keys():
            pass
        elif re.match(r'http', link):
            url_queue.append(link)

    return


def get_keyword_counts(text):
    """ splits the text into tokens and counts the number of occurrences of each keyword

    Args:
        text (str): a string

    Returns:
        dict of keywords and its occurrence
    """
    text = text.translate(text.maketrans("", "", punctuation))
    keywords = text.lower().split()
    count_dict = defaultdict(int)
    for item in keywords:
        count_dict[item] += 1
    return count_dict


def main():
    # source URL
    source_url = BASE_URL

    # initialize the queue of URLs
    url_queue = [source_url]

    # get all the visited links from database
    # in visited, value = 1 the link nee dto be parsed for only get the hyperlinks
    # value = 0 the link need to be parsed for both links and keywords
    visited = get_visited_links()

    # # initialize list of visited URLs
    # visited = [source_url]

    # get the links from url_queue and parse them
    while len(url_queue):
        link = url_queue.pop()
        print(link)
        if link not in visited.keys():
            # update visited dict
            visited[link] = 0
            # update database table with the new link

            try:
                page = urllib.request.urlopen(link)
                # Parsing the html page through Beautiful Soup
                soup = BeautifulSoup(page, 'html.parser')

                # collecting all the hyperlinks of the page into url_queue
                get_urls(soup, url_queue, visited)

                # get all the keywords in the page and their occurrences into the count_dict
                text = soup.get_text()
                count_dict = get_keyword_counts(soup.get_text())
                print(count_dict)

                short_desc = soup.title.string
                short_desc = short_desc.replace("\r", "").replace("\n", "").replace("\t", "").replace("    ", " ").strip()
                print(short_desc)
                description = soup.p.get_text()
                description = description.replace("\r", "").replace("\n", "").replace("\t", "").replace("    ", " ").strip()
                print(len(description))
                if len(description) > 500:
                    description = summarize(description, word_count=50)

                print(description)
                # insert the into database table
                slot = BaseModel.db_create_record({"link": link, "short_desc": short_desc, "description": description}, Links)

                # insert records into KeywordsLink table
                for key, value in count_dict.items():
                    BaseModel.db_create_record({"keyword": key, "link_id": slot[0].id, "occurrence": value}, KeywordsLink)

            except urllib.error.HTTPError:
                pass
            except urllib.error.URLError:
                pass
            except Exception as er:
                print("error:",er)
        # print(len(url_queue))
        elif visited[link] == 1:
            visited[link] = 0
            try:
                page = urllib.request.urlopen(link)
                # Parsing the html page through Beautiful Soup
                soup = BeautifulSoup(page, 'html.parser')

                # collecting all the hyperlinks of the page into url_queue
                get_urls(soup, url_queue, visited)
            except urllib.error.HTTPError:
                pass
            except urllib.error.URLError:
                pass
        else:
            pass
    # for i in url_queue:
    #     print(i)

    # for key, value in count.items():
    #     print(key, value)

    # page = urllib.request.urlopen(url_queue[1])
    # soup = BeautifulSoup(page, 'html.parser')


if __name__ == '__main__':
    main()
