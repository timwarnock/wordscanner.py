#!/usr/bin/env python3
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
import wordscanner as ws


if __name__== "__main__":
    grid = ws.load_grid('jgrid1k.txt')
    jp = ws.load_words('日本.txt')
    matches = ws.find_words(ws._setscan_rtl(grid,jp), jp)
    print(len(matches))
