#!/usr/bin/env python3
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
import wordscanner as ws


if __name__== "__main__":
    grid = ws.load_grid('grid1k.txt')
    english = ws.load_words('english.txt')
    matches = ws.find_words(ws._datriescan_rtl(grid,english), english)
    print(len(matches))
