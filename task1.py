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

    base_url = "http://mathprofi.ru/"
    queue.append(base_url)

    nested_link_class = "reference internal"

    page = 0
    max_pages = 100
    min_words = 500
    output_file_with_links = "index.txt"
    f = open(output_file_with_links, 'w')
    f.close()

    while queue and page < max_pages:
        url = queue.pop()
        # html = urllib.request.urlopen(url).read()
        if validators.url(url):
            try:
                html = urllib.request.urlopen(url).read()

                soup = BeautifulSoup(html, 'html.parser')
                for data in soup(['style', 'script', 'noscript', 'link']):
                    data.decompose()

                print('page #%d - address: %s' % (page, url))

                text = soup.get_text()
                if len(text.split()) >= min_words:
                    html_output = open(output + str(page) + ".txt", "wb")
                    html_output.write(html)
                    html_output.close()

                    with open(output_file_with_links, 'a') as file:
                        file.write(str(page) + " - " + url + "\n")

                    parsed_urls.add(url)
                    page += 1

                    internal_references = soup.find_all("a")
                    links = list(set([base_url + item['href'] for item in internal_references]))
                    #print(links)

                    nested_links = list()
                    for link in links:
                        if link not in parsed_urls:
                            nested_links.append(link)
                    queue.extend(nested_links)
                    # print(queue)
            except:
                continue
    print('done =)')
