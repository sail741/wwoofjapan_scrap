import time
from Host import Host


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


def scrap(params):
    """
    Make the scrap for the params in script.py
    :param params: the param dictionnary
    :return: None
    """

    print("Starting to scrap data...")

    f = open(params["output_file"], 'w')

    # We display the header
    for column in params["list_columns"]:
        f.write('%s\t' % column)
    f.write('\n')

    soup_list = Host.get_soup_list()
    if soup_list is None:
        print("Can't get the list of all host.")
        exit(1)
    rows = soup_list.find_all('tr', "sectiontableentry1") + soup_list.find_all('tr', "sectiontableentry2")

    cpt = 0
    size = len(rows)
    qty_matched = 0
    failed = []
    start = time.time()

    for row in rows:
        if cpt > 10:
            break
        # We use the cpt to know at wich percent we are
        percent = (cpt / size) * 100
        if params["display_eta"] and cpt % 5 == 0:
            eta = get_eta(start, percent)
            print("%.2f%% ETA : %s" % (percent, eta))
        cpt += 1

        # We get the soup for the current item
        item_id = row.contents[1].contents[1].contents[0].contents[0]

        host = Host(item_id)
        if not host.isValid:
            failed.append(item_id)
            continue

        should_add = host.should_add(params["criterias"])

        if should_add:
            host_as_string = host.to_string(params["list_columns"])

            # We output the result
            f.write('%s\n' % host_as_string)
            qty_matched += 1

    print("From the %s hosts, there is %s that match the criterias" % (size, qty_matched))
    if len(failed) > 0:
        print("The following hosts page didn't answered in time. They can't be listed : \n%s" % failed)
        f.write('%s\n' % failed)

    f.close()
