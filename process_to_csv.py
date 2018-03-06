#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reddit submission velocity checking
"""


import glob
import argparse
import os
import pandas as pd
from copy import copy, deepcopy
import re
from datetime import datetime
import json


#
#
# program arguments
#
#
parser = argparse.ArgumentParser(description='user info dumper')
parser.add_argument('input_path', help='directory to scan')
parser.add_argument('output_filename', help='filename of csv to save')
args = parser.parse_args()

filename_re = re.compile(r"([a-zA-Z0-9]+)_(\d+-\d+-\d+_\d+)")

dirs = glob.glob(os.path.join(args.input_path, "*"))
scrapes = [os.path.basename(d) for d in dirs]


empty_row = {s: None for s in scrapes}
empty_row["created_utc"] = None
empty_row["scrape_time"] = None
empty_row["id"] = None
empty_row["score"] = None
empty_row["num_comments"] = None
empty_row["title"] = None
empty_row["author"] = None


rows = []

for s in scrapes:
    files = glob.glob(os.path.join(args.input_path, s, "*.json"))
    for filename in files:
        basename = os.path.basename(filename)
        matches = filename_re.match(basename)
        dt = datetime.strptime(matches.group(2), "%Y-%d-%m_%H%M%S")

        with open(filename) as f:
            for idx, line in enumerate(f):
                obj = json.loads(line)["data"]

                # duplicate empty row
                r = copy(empty_row)

                try:
                    r["created_utc"] = datetime.utcfromtimestamp(
                        obj["created_utc"])
                    r["scrape_time"] = dt
                    r["id"] = obj["id"]
                    r["score"] = obj["score"]
                    r["num_comments"] = obj["num_comments"]
                    r["title"] = obj["title"]
                    r["author"] = obj["author"]
                    r[s] = idx

                    rows.append(r)
                except KeyError, e:
                    print line
                    quit()

cols = ["created_utc", "scrape_time", "id", "score", "num_comments",
    "author", "title"]
cols.extend(scrapes)

print cols
df = pd.DataFrame(rows)
#df = df[cols]
df.to_csv(args.output_filename, encoding="utf-8", index=False, header=True,
    columns=cols)

