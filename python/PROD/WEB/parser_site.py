# Обращаемся к странице и парсим ее
# результаты складываем в файлы 
#

import requests
import re
import json


def write_to_file(file, data, mode='w'):
    print('Writing to {}\n'.format(file))
    with open(file, mode) as newfile:
        newfile.write(data)


def read_file_data(file):
    print('Reading from {}\n'.format(file))
    try:
        opened_file = open(file)
        data = opened_file.read()
    finally:
        opened_file.close()

    return data

def get_service_data(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result
    else:
        raise RuntimeError("Request from url = '{}' ended with code {}".format(url, result.status_code))    

def get_web_data(links):
    r = requests.get(links)
    """ get data from WEB-page """
    print(r.status_code)
    print(r.headers)
    print(r.content)
    
def get_data_to_json(link):
    """get data from site and save to file (json format) """  
    response = get_service_data(link)
    dict_for_json = {}
    for hdr, value in response.headers.items():
        dict_for_json[hdr] = value
        print('{}:{}\n'.format(hdr, value))

    print('JSON response saved in file site_response.json')
    write_to_file('site_response.json', json.dumps(dict_for_json, sort_keys=True, indent=4))

def get_links(links):
    """ get all links from WEB-page """
    response = requests.get(links)
    if response.status_code == 200:
        link_pattern = r'<a[^><]*href=[\'"]([^><\'"]*)[\'"][^><]*>'
        print('Links from {} saved in file site_links.txt'.format(links))
        write_to_file('site_links.txt', '')
        for link_string in re.findall(link_pattern, response.text):
            write_to_file('site_links.txt', link_string + '\n', mode = 'a')
            print(link_string)
    return

if __name__ == "__main__":
    link_1 = 'http://habrahabr.ru/'
    link_2 = 'https://jsonplaceholder.typicode.com/'
    
    print ('get web data from ', link_1)
    #get_web_data(link_1)
    print ('get all links from web-site & save to file') 
    #get_links(link_1)
    print ('get data from web-site & save to file') 
    #get_data_to_json(link_2) 
    
   