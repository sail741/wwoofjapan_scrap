
from urllib.request import urlopen
# from urllib.request import ProxyHandler, build_opener, install_opener
import bs4
import time

'''
proxy_http = "yourproxy"
proxy_https = "yourproxy"

proxy_support = ProxyHandler({"http": proxy_http, "https": proxy_https})
opener = build_opener(proxy_support)
install_opener(opener)
'''

more_data = [
    {
        "name": "city",
        "div_id": "cbfv_423"
    },
    {
        "name": "prefecture",
        "div_id": "cbfv_152"
    },
    {
        "name": "region",
        "div_id": "cbfv_151"
    },
    {
        "name": "tasks",
        "div_id": "cbfv_303"
    }

]


def get_soup_list():
    """
    Get the the soup from the page that display all the host list
    :return: the soup from bs4 that display all the host list
    """
    url_list = "https://www.wwoofjapan.com/main/index.php?option=com_comprofiler&task=usersList&listid=9&Itemid=476&lang=en"
    html = urlopen(url_list).read().decode('utf-8', 'ignore')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup


def get_url_detail(item_id):
    return "https://www.wwoofjapan.com/main/index.php?option=com_comprofiler&task=userProfile&user=%s&Itemid=514&lang=en" % item_id


def get_soup_detail(item_id):
    """
    Get the soup for a specific item in the hosts list
    :param item_id: The id of the specific item in the hosts list
    :return: the soup from bs4 that display a specific item in the hosts list
    """
    url = get_url_detail(item_id)
    html = urlopen(url).read().decode('utf-8', 'ignore')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup


def get_eta(start_time, current_percent):
    """
    Get the estimated time average (from the starting time and the current percent
    :param start_time: the time.time() that we saved at the beginning of the loop
    :param current_percent: the current percent of the loop
    :return: a string that represent the ETA
    "+inf" if current_percent=0 because we can't calculate anything without time
    "Ts" if current_percent>0
    """
    if current_percent == 0:
        return "+inf"

    now = time.time()
    difference = now - start_time

    return str(int((100 / current_percent) * difference - difference)) + "s"


def should_add_string(criteria, data):
    """
    Check if the criteria is valid for the data with comparing as string.
    If the data is in the banned_values, we don't add it.
    Else, if the data is in the allowed_values, we add it.
    Otherwise, we don't add it.

    :param criteria: criteria from the params dictionary
    :param data: the current value of the div
    :return: True if the criteria is Ok, else otherwise
    """
    for banned_value in criteria["banned_values"]:
        if banned_value in data:
            return False

    for allowed_values in criteria["allowed_values"]:
        if allowed_values in data:
            return True

    return len(criteria["allowed_values"]) == 0


def should_add_int(criteria, data):
    """
    Check if the criteria is valid for the data with comparing as int.
    We cast data into int and we check if data > min_value and if data < max_value
    If min/max values are not set (i.e. equal None) we do not check

    :param criteria: criteria from the params dictionary
    :param data: the current value of the div
    :return: True if the criteria is Ok, else otherwise
    """
    data = int(data)
    if criteria["min_value"] is not None and data < criteria["min_value"]:
        return False

    if criteria["max_value"] is not None and data > criteria["max_value"]:
        return False

    return True


def should_add_feeding(criteria, data):
    """
    Check if the criteria is valid for the data for specific feeding value
    N.B. : this remove hosts when they only display "It is not possible" in feeding information

    :param criteria: criteria from the params dictionary
    :param data: the current value of the div
    :return: True if the criteria is Ok, else otherwise
    """
    if criteria["remove"]:
        return not(len(data.contents) == 1 and data.contents[0].contents[0] == "It is not possible")
    return True


def get_island(region):
    """
    Get the island from the region
    :param region: The region as it is displayed on the website
    :return: Hokkaido, Shikoku, Kyushu or Honshuu
    """
    if region in ["Hokkaido"]:
        return "Hokkaido"
    elif region in ["Shikoku area"]:
        return "Shikoku"
    elif region in ["Kyushu area"]:
        return "Kyushu"
    elif region in ["Chubu area", "Chugoku area", "Kansai area", "Kanto area", "Tohoku area"]:
        return "Honshuu"

    return "N/A"


def scrap(params):
    """
    Make the scrap for the params in script.py
    :param params: the param dictionnary
    :return: None
    """

    print("Starting to scrap data...")

    f = open(params["output_file"], 'w')

    soup_list = get_soup_list()
    rows = soup_list.find_all('tr', "sectiontableentry1") + soup_list.find_all('tr', "sectiontableentry2")

    cpt = 0
    size = len(rows)
    qty_matched = 0
    start = time.time()
    for row in rows:
        # We use the cpt to know at wich percent we are
        percent = (cpt / size) * 100
        cpt += 1
        if params["display_eta"] and cpt % 5 == 0:
            eta = get_eta(start, percent)
            print("%.2f%% ETA : %s" % (percent, eta))

        # We get the soup for the current item
        item_id = row.contents[1].contents[1].contents[0].contents[0]
        soup_detail = get_soup_detail(item_id)

        should_add = True
        list_data = [get_url_detail(item_id)]
        for criteria in params["criterias"]:

            data = soup_detail.find(id=criteria["div_id"])
            if data is None and criteria["required"]:
                should_add = False
                break
            elif data is None:
                continue
            data = data.contents[0]

            if criteria["type"] == "string":
                should_add = should_add_string(criteria, data)
            elif criteria["type"] == "int":
                should_add = should_add_int(criteria, data)
            elif criteria["type"] == "feeding":
                should_add = should_add_feeding(criteria, data)

            if not should_add:
                break
            list_data.append(str(data))

        if should_add:
            for md in more_data:
                data = soup_detail.find(id=md["div_id"])
                if data is not None:
                    data = str(data.contents[0].encode('utf-8'))[2:-1]
                    list_data.append(data)
            # We append the island in japan
            list_data.append(get_island(list_data[8]))
            # We output the result
            f.write('%s\t%s\n' % (item_id, "\t".join(list_data)))
            qty_matched += 1

    f.close()

    print("From the %s hosts, there is %s that match the criterias" % (size, qty_matched))
