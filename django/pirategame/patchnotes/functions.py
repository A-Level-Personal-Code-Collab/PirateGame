#---------------------------------------------------------------------#
# File: /functions.py
# Project: https://github.com/Lime-Parallelogram/patchnotes
# Created Date: Wednesday, July 27th 2022, 10:54:38 am
# Description: This file contains a number of functions for handling the markdown files
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Wed Jul 27 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------#

def parseMarkdown(markdown):
    print(markdown)
    return {
        "title": markdown[0]
    }