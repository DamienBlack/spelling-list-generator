from spelling import app
import csv, re, collections, random

class Word(object):
    def __init__(self, row):
        self.word, self.definition, self.origin, self.sentence, \
            rule1, rule2 = row
        rules = []
        if rule1: rules.append(rule1)
        if rule2: rules.append(rule2)
        self.rules = '; '.join(rules)

        self.origin = stripstring(self.origin, "Origin: ")
        self.sentence = stripstring(self.sentence, "Sentence: ")

def stripstring(s, prefix):
    if s.upper().startswith(prefix.upper()):
        return s[len(prefix):]
    else:
        return s

class Page(object):
    def __init__(self, subtitle, words):
        self.subtitle = subtitle
        self.words = words

def read_list(filename):
    words = []
    with app.open_resource(filename) as f:
        for row in csv.reader(f):
            row = [field.decode('utf-8') for field in row]
            words.append(Word(row))
    return words

word_database = {
        'list1': read_list('data/list1.txt'),
        'list2': read_list('data/list2.txt'),
        'list3': read_list('data/list3.txt'),
        }
    
def make_word_regex(omitted_words):
    omitted_regex = '|'.join(r'\b' + re.escape(word) + r'\b' for word in omitted_words)
    return re.compile(omitted_regex, re.I)

def filter_word_list(word_list, pattern):
    return [w for w in word_list if not pattern.search(w.word)]

def generate(
        contestants, tiebreakers, tiebreaker_list, words_per_round,
        omitted_words, word_lists, word_counts, shuffle):

    contestants = int(contestants)
    tiebreakers = int(tiebreakers) if tiebreakers else 0
    words_per_round = int(words_per_round) if words_per_round else 0
    
    omitted_words = omitted_words.split()
    distribution = [(l, int(c)) for (l,c) in zip(word_lists, word_counts) if l]
    words_per_contestant = sum(c for (l,c) in distribution)
    shuffle = (shuffle.lower() == 'yes')

    # compute eligible words
    if not omitted_words:
        eligible = word_database
    else:
        word_regex = make_word_regex(omitted_words)
        eligible = {}
        for list_name in word_database:
            eligible[list_name] = filter_word_list(word_database[list_name],
                    word_regex)

    # calculate number of total words from each list
    total_word_count = collections.defaultdict(int)
    for list_name, word_count in distribution:
        total_word_count[list_name] += word_count * contestants
    if tiebreakers:
        total_word_count[tiebreaker_list] += tiebreakers

    # randomly choose all words
    master_words = {}
    for list_name in total_word_count:
        master_words[list_name] = random.sample(eligible[list_name], 
                total_word_count[list_name])

    # divide words up by contestant
    contestant_lists = []
    for i in xrange(contestants):
        this_contestant = []
        for list_name, count in distribution:
            this_contestant += master_words[list_name][:count]
            del master_words[list_name][:count]
        if shuffle:
            random.shuffle(this_contestant)
        contestant_lists.append(this_contestant)

    if tiebreakers:
        tiebreaker_words = master_words[tiebreaker_list]
    else:
        tiebreaker_words = []

    # arrange words into pages
    pages = []
    for i in xrange(words_per_contestant):
        if words_per_round:
            subtitle = "Round %d / Word %d" % (
                    i / words_per_round + 1,
                    i % words_per_round + 1)
        else:
            subtitle = "Word %d" % (i + 1)

        this_list = []
        for l in contestant_lists:
            this_list.append(l[i])
        pages.append(Page(subtitle, this_list))
    if tiebreaker_words:
        pages.append(Page("Tiebreakers", tiebreaker_words))

    return pages


