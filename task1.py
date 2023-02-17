from bs4 import BeautifulSoup
import os
import shutil
import urllib.request
import validators


if __name__ == '__main__':

    output = "output/"
    shutil.rmtree(output)
    os.mkdir(output)

    queue = []
    parsed_urls = set()

    base_url = "https://cloud.yandex.ru/docs"
    queue.append(base_url)

    page = 0
    max_pages = 100
    min_words = 10
    output_file_with_links = "index.txt"

    while queue and page < max_pages:
        url = queue.pop()
        if validators.url(url):
            try:
                html = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(html, 'html.parser')

                print('page #%d - address: %s' % (page, url))

                if len(soup.text.split()) >= min_words:

                    html_output = open(output + str(page) + ".txt", "wb")
                    html_output.write(html)
                    html_output.close()

                    with open(output_file_with_links, 'a') as file:
                        file.write(str(page) + " - " + url + "\n")

                    parsed_urls.add(url)
                    page += 1

                    internal_references = soup.find_all("a")
                    links = list(set([item['href'] for item in internal_references]))

                    nested_links = list()
                    for link in links:
                        if link not in parsed_urls:
                            nested_links.append(link)
                    queue.extend(nested_links)
            except:
                continue
    print('done =)')


