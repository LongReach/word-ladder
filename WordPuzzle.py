# Solution to Amazon Word Puzzle

# List of all the words in the dictionary
word_list = []

file1 = open('FourLetterWords.txt', 'r')
file_lines = file1.readlines()

# Strips the newline character
for line in file_lines:
    words = line.strip().split(" ")
    # Remove any words of zero length, add remaining words to big list
    word_list = word_list + [w for w in filter(lambda x: len(x) > 0, words)]

class WordsFromLetter():

    def __init__(self):
        self.lists_by_letter = {} # dictionary indexed by letter

    def add_word(self, letter, word):
        the_list = self.lists_by_letter.get(letter)
        if the_list is None:
            the_list = []
            self.lists_by_letter[letter] = the_list
        the_list.append(word)

    def get_words(self, letter):
        the_list = self.lists_by_letter.get(letter)
        return [] if the_list is None else the_list

# For each letter index n of a four letter word, there is a lookup to find all the words that have a letter at
# position n in common.
lookups_by_pos = []
for i in range(4):
    lookups_by_pos.append(WordsFromLetter())

# fill out the lookup info
for word in word_list:
    for i in range(4):
        lookups_by_pos[i].add_word(word[i], word)

def get_words_by_pos_and_letter(pos, letter):
    return lookups_by_pos[pos].get_words(letter)

print("Words with first letter Y")
print(get_words_by_pos_and_letter(0, 'Y'))
print("Words with second letter E")
print(get_words_by_pos_and_letter(1, 'E'))
print("Words with third letter R")
print(get_words_by_pos_and_letter(2, 'R'))



