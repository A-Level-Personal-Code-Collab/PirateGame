# --------------------------------------------------------------------- #
# File: docs/patch notes/compile.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame/
# Created Date: Wednesday, July 27th 2022, 12:31:12 pm
# Description: A script that can compile patch notes into JSON format from which they are rendered
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Wed Jul 27 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-07-27	WH	Added conversion from newer .md standard
# 2022-07-27	WH	Added converters from old .txt standard
# --------------------------------------------------------------------- #
import os
import json
from pathlib import Path

OUTPUT_LOCATION = Path("django/pirategame/patchnotes/patchnotes/")
INPUT_LOCATION = Path("docs/patch notes/")

def convertTxtToJSON(file):
    """Conversion from old standard"""
    title = file.readline().strip() #works
    body = file.readlines()

    jsonText = {
        "title": title,
        "blocks": []
    }

    block = None
    for line in body:
        # check if it starts with a ~ # or -
        if line[0] == "^": # checks if header
            if block and len(block["changes"]) > 0:
                jsonText["blocks"].append(block)
            block = {"title": line[1:].strip(), "changes": []}

        elif line[0] == "~": # description
            jsonText["overview"] = line[1:].strip()

        elif line[0] == "-": # Bullet point
            block["changes"].append(line[1:].strip())

    if block:
        jsonText["blocks"].append(block)

    return jsonText

def convertMDToJSON(file):
    """Conversion from markdown standard"""
    title = file.readline().strip()  # Title is still the first line
    body = file.readlines()

    jsonText = {
        "title": title[1:],
        "overview": "",
        "version": "",
        "blocks": []
    }

    # Generate list showing where all of the block headers are
    blockHeaders = []
    for number, line in enumerate(body):
        if line[:3] == "## ":
            blockHeaders.append(number)

    # Iterate through block breaks and handle them
    for line in range(len(blockHeaders)):
        title_line = blockHeaders[line]
        final_line = len(body) if line == len(blockHeaders)-1 else blockHeaders[line+1] - 1 # For the final block, the end line is the end of the file

        # Automatically send overview to overview section
        if "Overview" in body[title_line]:
            jsonText["overview"] = body[title_line+1].strip()

        else:
            block = {"title": body[title_line][2:], "changes": []}
            for l in body[title_line+1:final_line]:
                block["changes"].append(l[1:].strip()) # Append changes to the changes block (Remove '- ' from start)
            
            jsonText["blocks"].append(block) # Add completed block to main JSON

    return jsonText

# Handle all files in input folders
for file in os.listdir(INPUT_LOCATION):
    in_path = INPUT_LOCATION/file

    # Ignore files that are not patch notes
    if in_path.suffix in [".md",".txt"]:
        with open(in_path) as infile:
            if ".txt" == in_path.suffix:
                output_data = convertTxtToJSON(infile)
            elif ".md" == in_path.suffix:
                output_data = convertMDToJSON(infile)
            
            # Add version info to output
            output_data["version"] = in_path.stem

            # Write output
            output_file = OUTPUT_LOCATION / (in_path.stem + ".json")
            with open(output_file,"w") as outfile:
                json.dump(output_data,outfile,indent=4)