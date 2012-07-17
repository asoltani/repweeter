#!/usr/bin/python

import twitter
import re
import urllib2
import argparse
from collections import defaultdict
from operator import itemgetter

parser = argparse.ArgumentParser(description="Count repeated tweets URLs")
parser.add_argument("-u", "--user", type=str, help="Twitter username")
parser.add_argument("-c", "--count", type=str, help="How many tweets to pull (max 200)")
args = parser.parse_args()

api = twitter.Api();
dup = defaultdict(int)
buf = []

ss = api.GetUserTimeline(args.user, count=args.count, include_entities='expanded_url')
for s in reversed(ss):
 if (s.in_reply_to_user_id is None and not re.search(r'MT|RT', s.text)):
	for u in s.urls:
		url = ''
		try:
			url = urllib2.urlopen('http://therealurl.appspot.com?url=' + u.expanded_url).read()
#			url = re.match("(http[^\?]*)", lurl).group(0)
		except urllib2.URLError, e:
			pass
			
		url = url if url is not None else u
		if url: dup[url] += 1
		text = s.text.replace(u.url,url).encode('ascii', 'ignore')
		buf.append("(%s) %s | %s" % (dup[url], s.created_at[0:16], text))
		

print "###############################################################################"
print "### TOP REPWEETS:"
c = 0
for t in sorted(dup.items(), key=itemgetter(1), reverse=True):
	print "(%s) %s" % (t[1], t[0])
	c += 1
	if c >= 10:
		break

print "\n###############################################################################"
print "### ACTUAL TWEETS W/ REPWEET COUNT:"
for line in reversed(buf):
	print line

