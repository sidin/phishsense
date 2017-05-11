import os
import random
import requests

from bs_localsettings import get_ts

USER_AGENTS = ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.7.01001)', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0', 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8', 'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0', 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)', 'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1', 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)', 'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)', 'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1', 'Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.02', 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1', 'Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.0) Opera 7.02 Bork-edition [en]']


class PageVisitor(object):

    def __init__(self, url):
        self.url = url
        self.body = None

    def fetchHtml(self):
        headers = { 'User-Agent': random.choice(USER_AGENTS)}
        if not self.url.startswith('http'):
            self.url = 'http://' + self.url
        phishing_url_response = requests.get(self.url, headers=headers, timeout=3)
        self.body = phishing_url_response.text
        return self.body


class CrawlUrlHelper(object):
    """
    Class to have a single focus to crawl the html content and save for further use
    """

    def verify_dump_location_exists(self, dump_location):
        if not os.path.exists(dump_location):
            os.makedirs(dump_location)

    def fetchHtmlBody(self, url):
        pv = PageVisitor(url)
        html_body = pv.fetchHtml()
        return html_body

    def download_webpage(self, url):
        s = requests.session()
        req = s.get(url)
        reqcontent = req.content
        return reqcontent

    def savecontent(self, html_content, filename_to_save):
        if os.path.exists(filename_to_save):
            # Log error here. Should not happen. Find out why/if it reached here.
            pass
        else:
            fp = open(filename_to_save, "w")
            fp.write(html_content)
            fp.close()

    def crawl_method1(self, analysis_url):
        html_content = self.fetchHtmlBody(analysis_url)
        return html_content

    def crawl_method2(self, analysis_url):
        html_content = self.download_webpage(analysis_url)
        return html_content

    def go(self, dump_location, analysis_url):
        self.verify_dump_location_exists(dump_location)
        html_content = self.crawl_method2(analysis_url)
        filename_to_save = "%s%s%s.html" % (dump_location, os.sep, get_ts())
        self.savecontent(html_content, filename_to_save)
        return filename_to_save




