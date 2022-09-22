import django
import os
import sys
import time
import json
import requests

sys.path.append("")
# Add this line
django.setup()


def poll():
    while True:
        print('Service poller polling for data')
        try:
            pass
        except Exception as e:
            print(e, file=sys.stderr)
        time.sleep(30)


if __name__ == "__main__":
    poll()
