import os
import json
import requests
from multiprocessing.pool import ThreadPool


def build_index():
    page = 1
    URLs = []

    while True:
        res = requests.get("https://undraw.co/api/illustrations?page={}".format(page))
        json_body = res.json()

        for item in json_body['illos']:
            title = item['title']
            url = item['image']

            print("Title: %s => URL: %s" % (title, url))
            URLs.append([title, url])

        page = json_body['nextPage']
        print("Proceeding to Page %d" % page)

        if not json_body['hasMore']:
            print("Finished Gathering JSON.")
            return URLs


def download_from_entry(entry):
    title, url = entry
    file_name = "%s.svg" % title.lower().replace(' ', '_')

    print("Downloading %s" % file_name)

    if not os.path.exists(file_name):
        res = requests.get(url, stream=True)

        if res.status_code == 200:
            path = "./images/%s" % file_name

            with open(path, 'wb') as f:
                for chunk in res:
                    f.write(chunk)

            return file_name


urls = build_index()

print("Downloading %d files." % len(urls))

results = ThreadPool(20).imap_unordered(download_from_entry, urls)

for path in results:
    print("Downloaded %s" % path)

print("Downloaded %d files." % len(urls))