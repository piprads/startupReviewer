import time, random
from xgoogle.search import GoogleSearch, SearchError
import csv
ofile  = open('companies/bdna.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

max_pages = 58; # 58 times
for page in range (0, max_pages):
  wt = random.uniform(2, 5)
  try:
    #gs = GoogleSearch("quick and dirty")
    #gs = GoogleSearch("site:linkedin.com/pub/ Experience healthtap")
    gs = GoogleSearch("site:linkedin.com/pub/ OR site:linkedin.com/in/ \"at healthtap\"")
    gs.results_per_page = 10
    gs.page = page
    results = gs.get_results()
    #Try not to annnoy Google, with a random short wait
    time.sleep(wt)
    for res in results:
      print res.title.encode("utf8")
      print res.desc.encode("utf8")
      print res.url.encode("utf8")
      print
      writer.writerow([res.title.encode("utf8"), res.desc.encode("utf8"), res.url.encode("utf8")])
  except SearchError, e:
    print "Search failed: %s" % e

print "Done"
ofile.close()



from xgoogle.search import GoogleSearch, SearchError
import csv
ofile  = open('companies/healthtap2.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

try:
  #gs = GoogleSearch("quick and dirty")
  #gs = GoogleSearch("site:linkedin.com/pub/ Experience healthtap")
  gs = GoogleSearch("site:linkedin.com/pub/ \"at healthtap\"")
  gs.results_per_page = 10
  gs.page = 0
  results = gs.get_results()
  for res in results:
    print res.title.encode("utf8")
    print res.desc.encode("utf8")
    print res.url.encode("utf8")
    print
    writer.writerow([res.title.encode("utf8"), res.desc.encode("utf8"), res.url.encode("utf8")])
  ofile.close()
except SearchError, e:
  print "Search failed: %s" % e




import re
from urlparse import urlparse
from xgoogle.search import GoogleSearch, SearchError

target_domain = "healthtap.com"
target_keyword = "healthtap"

def mk_nice_domain(domain):
    """
    convert domain into a nicer one (eg. www3.google.com into google.com)
    """
    domain = re.sub("^www(\d+)?\.", "", domain)
    # add more here
    return domain

gs = GoogleSearch(target_keyword)
gs.results_per_page = 100
results = gs.get_results()
for idx, res in enumerate(results):
  parsed = urlparse(res.url)
  domain = mk_nice_domain(parsed.netloc)
  if domain == target_domain:
    print "Ranking position %d for keyword '%s' on domain %s" % (idx+1, target_keyword, target_domain)
