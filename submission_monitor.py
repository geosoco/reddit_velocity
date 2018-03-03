#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reddit submission velocity checking
"""

import argparse
import codecs
import os
from reddit.connections import Reddit
from reddit.endpoints.subreddit import (
    SubredditListing)
import json
from ezconf import ConfigFile
import logging
from copy import deepcopy
from datetime import datetime
import time


#
#
# program arguments
#
#
parser = argparse.ArgumentParser(description='user info dumper')
parser.add_argument('subreddit', help='subreddit to scan')
parser.add_argument('output_path', help='path where files will be dumped')
args = parser.parse_args()


def dump_listing(filename, listing):
    with codecs.open(filename, "w", encoding="utf8") as outfile:
        for item in listing:
            outfile.write(json.dumps(item))
            outfile.write(u"\n")


def get_date_time_filename(base):
    return "{}_{}.json".format(
        base, datetime.now().strftime("%Y-%m-%d_%H%M%S"))

#
#
# main
#
#

logging.basicConfig(level=logging.DEBUG)

cfg = ConfigFile("config.json")
reddit = Reddit(
    cfg.getValue("auth.client_id"),
    cfg.getValue("auth.client_secret"),
    cfg.getValue("user-agent"))


# make directories
sub_dir = os.path.join(args.output_path, args.subreddit)
listing_dir = os.path.join(sub_dir, "listings")
top_month_listing_dir = os.path.join(listing_dir, "top_month")
top_day_listing_dir = os.path.join(listing_dir, "top_day")
top_week_listing_dir = os.path.join(listing_dir, "top_week")
hot_global_listing_dir = os.path.join(listing_dir, "hot_global")
new_listing_dir = os.path.join(listing_dir, "new")
rising_listing_dir = os.path.join(listing_dir, "rising")


listings = [
    {
        "name": "top day",
        "dir": top_day_listing_dir,
        "sort": "top",
        "args": {"t": "day"}
    },
    {
        "name": "top week",
        "dir": top_week_listing_dir,
        "sort": "top",
        "args": {"t": "week"}
    },
    {
        "name": "top month",
        "dir": top_month_listing_dir,
        "sort": "top",
        "args": {"t": "month"}
    },
    {
        "name": "hot global",
        "dir": hot_global_listing_dir,
        "sort": "hot",
        "args": {"g": "global"}
    },
    {
        "name": "new",
        "dir": new_listing_dir,
        "sort": "new",
        "args": {}
    },
    {
        "name": "rising",
        "dir": rising_listing_dir,
        "sort": "rising",
        "args": {}
    },
]

# make the subdirectories
for l in listings:
    if not os.path.exists(l["dir"]):
        os.makedirs(l["dir"])


# start our loop
while True:

    start_time = datetime.now()

    # run through listing types
    for l in listings:
        print l["name"]
        sub = SubredditListing(
            reddit,
            args.subreddit,
            l["sort"],
            **l["args"])

        filename = os.path.join(
            l["dir"], get_date_time_filename(args.subreddit))

        dump_listing(filename, sub)

    time_diff = 0

    while time_diff < 600:
        time_diff = (datetime.now() - start_time).total_seconds()
        time.sleep(5)



