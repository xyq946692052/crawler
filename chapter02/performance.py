import csv
import time
import urllib2
import re
import timeit
from bs4 import BeautifulSoup
import lxml.html

FIELDS=('area','population','iso',country','capita)
