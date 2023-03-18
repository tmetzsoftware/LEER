from dictionary_lookup import Dictionary, DictionaryErrorChecker

# Set paths for dictionary and thesaurus files
dictionary_path = 'dictionary.json'
thesaurus_path = 'thesaurus.json'

# Create an instance of DictionaryErrorChecker class to handle errors related to dictionary and thesaurus files
error_checker = DictionaryErrorChecker(dictionary_path, thesaurus_path)

# Create an instance of Dictionary class to look up words and add definitions and synonyms to local files
dictionary = Dictionary(dictionary_path, thesaurus_path)

# Get user input and call the define_word method of the Dictionary class to look up the word
while True:
    word = input("Enter a word (type 'q' to quit): ")
    if word.lower() == 'q':
        break
    dictionary.define_word(word)
