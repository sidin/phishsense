import os
import sys

from step_crawlurl import CrawlUrlHelper 
from step_extract_features import extract_features
from step_query_model import query_model

crawlHelper = CrawlUrlHelper()


def step1(dump_location, analysis_url):
    """
    Crawl the URL
    """
    saved_filename = crawlHelper.go(dump_location, analysis_url)
    return saved_filename

def step2():
    """
    Extract the features
    """
    extract_features()

def step3():
    """
    Query the model
    """
    query_model()


def run_all_steps():
    """
    Execute the steps in sequence
    """
    # Steps
    step1()
    step2()
    step3()

