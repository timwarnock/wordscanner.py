# wordscanner.py
Scan through characters (grids, array, whatever) seeking words (English or otherwise).

This is simply a proof-of-concept to demonstrate the utility of using a Python set() as an alternative to Trie or DAWG structures for finding words in a given dictionary (English or otherwise).

## Overview
Given a character grid (or any character stream) where you can scan through individual characters, find all matching English words (according to an English dictionary, say, with roughly 100,000 entries). This is a standard exercise in natural language processing (with many examples and utils in [NLTK](https://www.nltk.org/)).

This is typically done with a [Trie](https://en.wikipedia.org/wiki/Trie), i.e., a prefix tree that can be implemented in Python using a nested dict:

    {'a': 
        {'p': 
            {'p': 
                {'l': 
                    {'e': 
                        {'$': '$'}
                    }
                }
            }, 
        'r': 
            {'e': 
                {'$': '$'}
            }
        }
    }

The advantage with a Trie is that it can store a large dictionary of words in a way that is useful for pruning through potential candidate matches (e.g., if I'm scanning letters and find an "a", then it matches the above Trie, but if the next character is not a "p" or "r", then I can stop searching on that path). Basically, a Trie (or [DAWG](https://en.wikipedia.org/wiki/Deterministic_acyclic_finite_state_automaton)) allows for efficient pruning and matching of words.

Additionally, there are numerous "Super-fast, efficient" Trie implementations. I used [datrie](https://github.com/pytries/datrie) for this example.

## Hypothesis

Rather than use a DAWG or Trie (even a "Super-fast, efficient" Trie), it is preferable to use a Python set() with the following algorithm:

    almost_words = set([])
    for word in dictionary:
        for i in range(len(word)-1)
            almost_words.add(word[0:i+1]

In other words, a flattened structure that contains all of the enumerated keys within a Trie or DAWG. The above example of ["apple", "are"] would look like this,

    {'a', 'ap', 'app', 'appl', 'ar'}

For Natural Language Processing tasks, this is nearly as memory efficient as a Trie or DAWG, and with equal to or better performance. I created test scripts to demonstrate this, using the included 1000x1000 character grid, as well as a generated 10,000 x 10,000 character grid.


## Trie vs set() for N=1,000,000
Scan through a 1000x1000 character grid. Interestingly, datrie performed the slowest, most likely due to the initial construction of the Trie itself. It was noticeably slower than the nested dict, but it was the most memory efficient. For larger grids, the slower construction of the Trie should not matter (as it's constant, based on the size of the dictionary).

    $ /usr/bin/time ./test_w_datrie.py
    3155
    3.50user 0.03system 0:03.54elapsed 99%CPU (0avgtext+0avgdata 38028maxresident)k
    0inputs+0outputs (0major+8880minor)pagefaults 0swaps

    $ /usr/bin/time ./test_w_trie.py
    3155
    2.00user 0.05system 0:02.05elapsed 99%CPU (0avgtext+0avgdata 81704maxresident)k
    0inputs+0outputs (0major+20976minor)pagefaults 0swaps

    $ /usr/bin/time ./test_w_set.py
    3155
    1.45user 0.01system 0:01.47elapsed 99%CPU (0avgtext+0avgdata 41860maxresident)k
    0inputs+0outputs (0major+9539minor)pagefaults 0swaps

## Trie vs set() for N=100,000,000
Scan through a 10,000 x 10,000 character grid. As expected, datrie outperformed the naive nested dict Trie, but failed to overtake the much simpler python set() implementation.

    $ /usr/bin/time ./test_w_datrie.py
    9787
    127.80user 0.16system 2:07.98elapsed 99%CPU (0avgtext+0avgdata 134288maxresident)k
    0inputs+0outputs (0major+58289minor)pagefaults 0swaps

    $ /usr/bin/time ./test_w_trie.py
    9787
    161.65user 0.12system 2:41.80elapsed 99%CPU (0avgtext+0avgdata 179600maxresident)k
    0inputs+0outputs (0major+54897minor)pagefaults 0swaps

    $ /usr/bin/time ./test_w_set.py
    9787
    120.05user 0.25system 2:00.42elapsed 99%CPU (0avgtext+0avgdata 139864maxresident)k
    0inputs+0outputs (0major+76902minor)pagefaults 0swaps
    
## Conclusion
For natural language processing, a naive set() of prefixes is faster than Trie, and is nearly as memory efficient as a DAWG or [libdatrie](https://linux.thai.net/~thep/datrie/datrie.html).

