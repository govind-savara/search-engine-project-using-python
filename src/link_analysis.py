import json
import operator
from peewee import fn
from collections import defaultdict
from model.model_keyword import Links, KeywordsLink


def get_links(keyword):
    """ Retrieves all the links for the tokens of keyword

    Args:
        keyword (str): A string of tokens

    Returns:
        list of all link details
    """
    tokens = keyword.lower().split()

    related_links = defaultdict(dict)
    i = 0
    for token in tokens:
        for record in Links.select(Links.link, fn.SUM(KeywordsLink.occurrence).alias("key_count"))\
                .join(KeywordsLink, on=(Links.id == KeywordsLink.link_id))\
                .dicts()\
                .where(KeywordsLink.keyword.contains(token))\
                .group_by(Links.link):
            related_links[str(i)]['link'] = record['link']
            related_links[str(i)]['count'] = record['key_count']
            i += 1

    if related_links:
        links = ranking_links(related_links)
        return links
    else:
        return related_links


def get_visited_links():
    """ Get all the stored links from database

    Returns:
        {}
    """
    # initialize dict of visited links
    visited_links = {}

    for record in Links.select().dicts():
        # print(record["link"])
        visited_links[record["link"]] = 1

    return visited_links


def ranking_links(links):
    """ sorts the links by the number of tokens and occurrence of tokens

    Args:
        links (dict): a dictionary of links

    Returns:
         list of sorted links according to no_of_tokens and occurrence of tokens
    """
    rank_links = defaultdict(dict)
    link_desc = defaultdict(dict)
    ranked_links = defaultdict(dict)
    rank_links_list = []
    for key, value in links.items():
        if value['link'] not in rank_links.keys():
            rank_links[value['link']]['no_of_tokens'] = 1
            rank_links[value['link']]['count'] = value['count']
        else:
            rank_links[value['link']]['no_of_tokens'] += 1
            rank_links[value['link']]['count'] += value['count']

    # for key, value in rank_links.items():
    #     print(key, value['no_of_tokens'], value['count'])
    # print("rank_links", len(rank_links))
    for record in Links.select():
        # print('record:', record.link)
        link_desc[record.link] = record

    i = 0
    for key, value in rank_links.items():
        # print(value)
        rank_links_list.append({})
        rank_links_list[i]["link"] = key
        rank_links_list[i]["no_of_tokens"] = value['no_of_tokens']
        rank_links_list[i]["occurrence"] = int(value['count'])
        rank_links_list[i]["short_desc"] = link_desc[key].short_desc
        rank_links_list[i]["description"] = link_desc[key].description
        i += 1

    # for item in rank_links_list:
    #     print(item[2])
    rank_links_list = sorted(rank_links_list, key=lambda k: (-k["no_of_tokens"], -k["occurrence"]))
    print(rank_links_list)
    # i = 1
    # for item in rank_links_list:
    #     ranked_links[str(i)]['link'] = item[0]
    #     ranked_links[str(i)]['no_of_tokens'] = item[1]
    #     ranked_links[str(i)]['keyword_count'] = int(item[2])
    #     ranked_links[str(i)]['short_desc'] = item[3]
    #     ranked_links[str(i)]['description'] = item[4]
    #     i += 1
    # print("no of links found:", len(ranked_links))
    # return ranked_links
    print("no of links found:", len(rank_links_list))
    return rank_links_list


def main():
    web_links = get_links("month power the more you like is powerful")
    for item in web_links:
        print(item)
    print(len(web_links))
if __name__ == '__main__':
    main()