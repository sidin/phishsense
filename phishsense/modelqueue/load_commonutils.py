import os
import sys

from django.conf import settings

sys.path.append(settings.BUSINESS_STEPS)
from invoke_steps import step1, step2, step3

sys.path.append(settings.COMMON_UTILS)
from get_timestamp import get_timestamp as get_timestamp_imported

def get_ts():
    return get_timestamp_imported

def get_ts_instance():
    return get_timestamp_imported()
