import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load API keys from .env file
dictionary_api_key = os.getenv('DICTIONARY_API_KEY')
thesaurus_api_key = os.getenv('THESAURUS_API_KEY')

class DictionaryErrorChecker:
    def __init__(self, dictionary_path, thesaurus_path):
        """
        Initializes the DictionaryErrorChecker object with the paths to the dictionary and thesaurus JSON files.

        Args:
        - dictionary_path (str): The path to the dictionary JSON file.
        - thesaurus_path (str): The path to the thesaurus JSON file.
        """
        self.dictionary_path = dictionary_path
        self.thesaurus_path = thesaurus_path

    def check_files(self):
        """
        Checks if the dictionary and thesaurus JSON files exist, and creates them if they don't.
        """
        # Check if dictionary file exists, create empty file if it doesn't
        if not os.path.exists(self.dictionary_path):
            with open(self.dictionary_path, 'w') as f:
                json.dump({}, f)

        # Check if thesaurus file exists, create empty file if it doesn't
        if not os.path.exists(self.thesaurus_path):
            with open(self.thesaurus_path, 'w') as f:
                json.dump({}, f)

    def add_dictionary_response(self, word, response):
        """
        Adds a dictionary API response for a given word to the dictionary JSON file.

        Args:
        - word (str): The word that was looked up in the dictionary.
        - response (dict): The dictionary API response for the word.
        """
        # Check if dictionary file exists, create empty file if it doesn't
        if not os.path.exists(self.dictionary_path):
            with open(self.dictionary_path, 'w') as f:
                json.dump({}, f)

        with open(self.dictionary_path, 'r+') as f:
            data = json.load(f)
            if word not in data:
                data[word] = {'data': []}

            data[word]['data'].append(response)

            f.seek(0)
            json.dump(data, f)
            f.truncate()

    def add_thesaurus_response(self, word, response):
        """
        Adds a thesaurus API response for a given word to the thesaurus JSON file.

        Args:
        - word (str): The word that was looked up in the thesaurus.
        - response (dict): The thesaurus API response for the word.
        """
        # Check if thesaurus file exists, create empty file if it doesn't
        if not os.path.exists(self.thesaurus_path):
            with open(self.thesaurus_path, 'w') as f:
                json.dump({}, f)

        with open(self.thesaurus_path, 'r+') as f:
            data = json.load(f)
            if word not in data:
                data[word] = {'data': []}

            data[word]['data'].append(response)

            f.seek(0)
            json.dump(data, f)
            f.truncate()



class Dictionary:
    def __init__(self, dictionary_path='dictionary.json', thesaurus_path='thesaurus.json'):
        """
        Initializes a new instance of the Dictionary class.

        Args:
            dictionary_path (str): The path to the dictionary file. Defaults to 'dictionary.json'.
            thesaurus_path (str): The path to the thesaurus file. Defaults to 'thesaurus.json'.
        """
        load_dotenv()  # Load environment variables from .env file
        self.dictionary_api_key = os.getenv('DICTIONARY_API_KEY')
        self.thesaurus_api_key = os.getenv('THESAURUS_API_KEY')
        print(f"Dictionary API key: {self.dictionary_api_key}")
        print(f"Thesaurus API key: {self.thesaurus_api_key}")
        self.error_checker = DictionaryErrorChecker(dictionary_path, thesaurus_path)

    def define_word(self, word):
        """
        Define a word by querying the Dictionary and Thesaurus APIs and saving the results to files.

        Parameters:
            word (str): The word to define

        Returns:
            None
        """

        # Check if dictionary and thesaurus files exist, create empty files if they don't
        self.error_checker.check_files()

        # Define URL for dictionary API request
        dictionary_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.dictionary_api_key}"

        # Define URL for thesaurus API request
        thesaurus_url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={self.thesaurus_api_key}"

        try:
            # Make dictionary API request
            dictionary_response = requests.get(dictionary_url)
            dictionary_response.raise_for_status()  # Check for errors
            dictionary_data = dictionary_response.json()

            # Add word and definitions to dictionary file
            self.error_checker.add_dictionary_response(word,
                                                       [d['shortdef'] for d in dictionary_data if 'shortdef' in d])

            # Make thesaurus API request
            thesaurus_response = requests.get(thesaurus_url)
            thesaurus_response.raise_for_status()  # Check for errors
            thesaurus_data = thesaurus_response.json()

            # Add word and synonyms to thesaurus file
            self.error_checker.add_thesaurus_response(word, [s for syn in thesaurus_data if
                                                             'meta' in syn and 'syns' in syn['meta'] for s in
                                                             syn['meta']['syns'][0]])
        except json.decoder.JSONDecodeError:
            # Handle JSON decoding errors
            print(f"Error: Could not decode JSON for '{word}'.\n{dictionary_response.text}\n{thesaurus_response.text}")
        except requests.exceptions.RequestException as e:
            # Handle API connection errors
            print(f"Error: Could not connect to API for '{word}'.\n{e}")



