import json
import sys
import time
# import winsound
from datetime import datetime, timedelta
import urllib.request
import urllib.error


BRANCHES = {
    "Flamingo": "289537bba97afd8bf69f4a3a727f52ad31d0c95ccba0e6d8140c4f1dfc582fca",
    "Henderson": "12b6540fc956ac653afc530cb78d9211be3f32cda84b216b6198d18f72da5dc9",
    "Sahara": "b3a3c4a7d0eab805cbc9bb3ac1419daca1a901995be4fc96085411df29a15099",
}

SERVICES = {
    "RegistrationNew": "a8a535e55c3929b4e43679c32d8d3e60aba06b2768e61faa5af5bf364d28025d",
}

URL_TEMPLATE = "https://dmvapp.nv.gov/qmaticwebbooking/rest/schedule/branches/" \
               "{branch_id}/dates;servicePublicId={service_id};customSlotLength=15"


def beep():
    # winsound.Beep(440, 250)  # frequency, duration
    # time.sleep(0.25)  # in seconds (0.25 is 250ms)
    pass


def get_dates(branch_id, service_id):
    url = URL_TEMPLATE.format(branch_id=branch_id, service_id=service_id)
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print(e.reason)
        return None

    data = response.read()
    return json.loads(data)


def is_recent(date_string, days=7):
    dt = datetime.strptime(date_string, '%Y-%m-%d')
    return dt - datetime.now() < timedelta(days=days)


def main():
    days = int(sys.argv[1])

    while True:
        for branch, branch_id in BRANCHES.items():
            for service, service_id in SERVICES.items():
                print(f"getting service {service} from branch {branch}")
                date_list = get_dates(branch_id, service_id)
                if not date_list:
                    continue

                for date in date_list:
                    if is_recent(date["date"], days=days):
                        beep()
                        print(f"found appt for service {service} in branch {branch}: {date['date']}")

        time.sleep(10)


if __name__ == '__main__':
    main()
