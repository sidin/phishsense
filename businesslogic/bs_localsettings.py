import os
import sys

BASE_DIR = os.path.dirname(__file__)
COMMON_UTILS_DIR = os.path.join(BASE_DIR, '../commonutils')
sys.path.append(COMMON_UTILS_DIR)

from get_timestamp import get_timestamp

def get_ts():
    return get_timestamp()

