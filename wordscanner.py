#!/usr/bin/env python3
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
import random
import datrie, string


def find_words(scanner, wordict):
    ''' find all words in scanner that exist within wordict, returns a set() of all matches

        scanner must be an iterable object that returns candidate words

        wordict is any dict-like object that will return True if key is in wordict
    '''
    matches = set([])
    for word in scanner:
        if word in wordict:
            matches.add(word)
    return matches


def _gen_grid_random(rows=1000, cols=1000, charset='abcdefghijklmnopqrstuvwxyz'):
    return ["".join([random.choice(charset) for _ in range(rows)]) for _ in range(cols)]

def save_grid(grid, filename):
    fh = open(filename, 'w')
    for row in grid:
        fh.write(row + '\n')
    fh.close()

def load_grid(filename):
    grid = []
    fh = open(filename)
    for line in fh:
        grid.append(line.strip())
    fh.close()
    return grid

def load_words(filename):
    wordict = set([])
    fh = open(filename)
    for line in fh:
        wordict.add(line.strip())
    fh.close()
    return wordict

def _linescan_rtl(grid, wordict):
    ''' generator yielding word candidates from grid by reading right-to-left
        BRUTE FORCE no pruning version
        
        worddict is a dict or set of match words
    '''
    maxlen = 0
    for word in wordict:
        if len(word) > maxlen:
            maxlen = len(word)
    for line in grid:
        for i in range(max(len(line),maxlen) - maxlen):
            candidate_word = ''
            for c in range(min(len(line),maxlen)):
                candidate_word += line[i+c]
                yield candidate_word

def _setscan_rtl(grid, wordict):
    ''' generator yielding word candidates from grid by reading right-to-left
        
        worddict is a dict or set of match words, creates a set of "almost words"
    '''
    almost_words = set([])
    maxlen = 0
    for word in wordict:
        if len(word) > maxlen:
            maxlen = len(word)
        for i in range(len(word)-1):
            almost_words.add( word[0:i+1] )
    for line in grid:
        for i in range(max(len(line),maxlen) - maxlen):
            candidate_word = ''
            for c in range(min(len(line),maxlen)):
                candidate_word += line[i+c]
                yield candidate_word
                if candidate_word not in almost_words:
                    break

def _datriescan_rtl(grid, wordict):
    ''' generator yielding word candidates from grid by reading right-to-left
        
        worddict is a dict or set of match words, creates a datrie (prefix tree) of words for optimization
        https://github.com/pytries/datrie
    '''
    trie = datrie.BaseTrie(string.ascii_letters+"'")
    maxlen = 0
    for word in wordict:
        if len(word) > maxlen:
            maxlen = len(word)
        trie[word] = True
    for line in grid:
        for i in range(max(len(line),maxlen) - maxlen):
            candidate_word = ''
            for c in range(min(len(line),maxlen)):
                candidate_word += line[i+c]
                yield candidate_word
                if not trie.has_keys_with_prefix(candidate_word):
                    break

def _triescan_rtl(grid, wordict):
    ''' generator yielding word candidates from grid by reading right-to-left
        
        worddict is a dict or set of match words, creates a simple Trie (prefix tree) of words for optimization
    '''
    trie = _make_trie(wordict)
    maxlen = 0
    for word in wordict:
        if len(word) > maxlen:
            maxlen = len(word)
    for line in grid:
        for i in range(max(len(line),maxlen) - maxlen):
            candidate_word = ''
            for c in range(min(len(line),maxlen)):
                candidate_word += line[i+c]
                yield candidate_word
                if not _in_trie(trie, candidate_word):
                    break

def _make_trie(wordict):
    trie = {}
    for word in wordict:
        current_trie = trie
        for letter in word:
            current_trie = current_trie.setdefault(letter, {})
        current_trie['$'] = '$'
    return trie

def _in_trie(trie, word):
    ''' prefix or word in trie
    '''
    current_trie = trie
    for letter in word:
        if letter in current_trie:
            current_trie = current_trie[letter]
        else:
            return False
    return True

