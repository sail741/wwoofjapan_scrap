from urllib.request import urlopen
# from urllib.request import ProxyHandler, build_opener, install_opener
from urllib.error import HTTPError, URLError
import bs4

'''
proxy_http = "yourproxy"
proxy_https = "yourproxy"

proxy_support = ProxyHandler({"http": proxy_http, "https": proxy_https})
opener = build_opener(proxy_support)
install_opener(opener)
'''

list_div = {
    "qty_wwoofers": "cbfv_293",
    "relation_wwoofers": "cbfv_296",
    "date": "cbfv_290",
    "host_xp": "cbfv_542",
    "feeding_restriction": "cbfv_318",
    "city": "cbfv_423",
    "prefecture": "cbfv_152",
    "region": "cbfv_151",
    "tasks": "cbfv_303",
    "staying_time": "cbfv_292",
}


class Host:
    """
    Host represent an Host in the wwoofingjapan website.
    It contains every methods to get the soup, get the contents of div and to check criterias for research.
    """

    def __init__(self, item_id):
        self.id = item_id
        self.isValid = False
        self.url = Host._get_url_detail(item_id)

        soup = Host._get_soup_detail(item_id)
        if soup is None:
            return

        for key in list_div:
            setattr(self, key, Host._get_data_from_soup(soup, list_div[key]))
        self.island = Host._get_island(self.region)

        self.isValid = True

    @staticmethod
    def _get_soup(url):
        max_try = 3

        for i in range(max_try):
            try:
                html = urlopen(url).read().decode('utf-8', 'ignore')
                soup = bs4.BeautifulSoup(html, 'html.parser')
                return soup
            except HTTPError:
                pass
            except URLError:
                pass

        print("Fail trying to get soup from %s" % url)
        return None

    @staticmethod
    def get_soup_list():
        """
        Get the the soup from the page that display all the host list
        :return: the soup from bs4 that display all the host list
        """
        url_list = "https://www.wwoofjapan.com/main/index.php?option=com_comprofiler&task=usersList&listid=9&Itemid=476&lang=en"
        return Host._get_soup(url_list)

    @staticmethod
    def _get_url_detail(item_id):
        return "https://www.wwoofjapan.com/main/index.php?option=com_comprofiler&task=userProfile&user=%s&Itemid=514&lang=en" % item_id

    @staticmethod
    def _get_soup_detail(item_id):
        """
        Get the soup for a specific item in the hosts list
        :param item_id: The id of the specific item in the hosts list
        :return: the soup from bs4 that display a specific item in the hosts list
        """
        url = Host._get_url_detail(item_id)
        return Host._get_soup(url)

    @staticmethod
    def _get_data_from_soup(soup, div_id):
        """
        Get the content of a div from the soup by using the id
        :param soup: the soup where we look for the div
        :param div_id: the div id we look for
        :return: None is the div wasn't found, or his content if it was found. A string if leaf, or a Tag otherwise
        """
        data = soup.find(id=div_id)
        if data is None:
            return None

        return data.contents[0]

    def _should_add_string(self, criteria):
        """
        Check if the criteria is valid for the data with comparing as string.
        If the data is in the banned_values, we don't add it.
        Else, if the data is in the allowed_values, we add it.
        Otherwise, we don't add it.

        :param criteria: criteria from the params dictionary
        :return: True if the criteria is Ok, else otherwise
        """
        if not hasattr(self, criteria["name"]):
            return False
        data = getattr(self, criteria["name"])
        for banned_value in criteria["banned_values"]:
            if banned_value in data:
                return False

        for allowed_values in criteria["allowed_values"]:
            if allowed_values in data:
                return True

        return len(criteria["allowed_values"]) == 0

    def _should_add_int(self, criteria):
        """
        Check if the criteria is valid for the data with comparing as int.
        We cast data into int and we check if data > min_value and if data < max_value
        If min/max values are not set (i.e. equal None) we do not check

        :param criteria: criteria from the params dictionary
        :return: True if the criteria is Ok, else otherwise
        """
        if not hasattr(self, criteria["name"]):
            return False
        data = int(getattr(self, criteria["name"]))
        if criteria["min_value"] is not None and data < criteria["min_value"]:
            return False

        if criteria["max_value"] is not None and data > criteria["max_value"]:
            return False

        return True

    def _should_add_feeding(self, criteria):
        """
        Check if the criteria is valid for the data for specific feeding value
        N.B. : this remove hosts when they only display "It is not possible" in feeding information

        :param criteria: criteria from the params dictionary
        :return: True if the criteria is Ok, else otherwise
        """
        if not hasattr(self, criteria["name"]):
            return False
        data = getattr(self, criteria["name"])
        if criteria["remove"]:
            return not (len(data.contents) == 1 and data.contents[0].contents[0] == "It is not possible")
        return True

    @staticmethod
    def _get_island(region):
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

    def should_add(self, criterias):
        """
        Check if the current host should be added to the valided list according to the criterias
        :param criterias: the criterias from the params dictionary
        :return: True if we should add it, or False otherwise
        """
        for criteria in criterias:
            if not hasattr(self, criteria["name"]):
                return False
            if getattr(self, criteria["name"]) is None:
                if criteria["required"]:
                    return False
                else:
                    continue

            if criteria["type"] == "string" and not self._should_add_string(criteria):
                return False
            elif criteria["type"] == "int" and not self._should_add_int(criteria):
                return False
            elif criteria["type"] == "feeding" and not self._should_add_feeding(criteria):
                return False

        return True

    def to_string(self, list_columns):
        """
        Return the current host as string, by keeping the columns given in parameter
        It displays the host by separating the columns with tabulations (TSV)
        :param list_columns: the list of columns that we should keep
        :return: a string that represent an host as TSV
        """
        host_as_string = ""
        for column in list_columns:
            if hasattr(self, column):
                # We are carefull because there is error caused by encoding
                host_as_string += str(str(getattr(self, column)).encode('utf-8'))[2:-1] + "\t"
            else:
                host_as_string += "N/A\t"

        return host_as_string
