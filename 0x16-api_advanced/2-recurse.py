#!/usr/bin/python3
"""ALX SE API Module."""
import requests


def recurse(subreddit, top_list=[]):
    """Return list of title of the top posts in a subreddit."""
    def recurse_post(lst, post_list, curr_idx):
        """Recursively add all title to top_list."""
        if curr_idx >= len(post_list):
            return
        title = post_list[curr_idx]['data']['title']
        lst.append(title)
        recurse_post(lst, post_list, curr_idx + 1)

    def get_post(limit, after, url, header, post_list):
        """Recursively make request to reddit api(Handled its pagination)."""
        if limit > len(post_list):
            return
        url = '{}&after={}'.format(url, after)
        response = requests.get(url, headers=header)
        post_list = response.json()['data']['children']
        after = 't3_{}'.format(post_list[-1]['data']['id'])
        recurse_post(top_list, post_list, 0)
        get_post(limit, after, url, header, post_list)

    header = {
            'User-Agent': 'MyBot/1.0'
            }
    limit = 100
    url = 'https://reddit.com/r/{}/top.json?limit={}'.format(subreddit, limit)
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        post_list = response.json()['data']['children']
        after = 't3_{}'.format(post_list[-1]['data']['id'])
        recurse_post(top_list, post_list, 0)
        get_post(limit, after, url, header, post_list)
        return top_list
    else:
        return None
