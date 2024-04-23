import sqlite3
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class GoodsChatBot:
    def __init__(self, database_path='goods.db'):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def process_message(self, message):
        # Tokenize the message
        words = word_tokenize(message.lower())

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalnum() and word not in stop_words]

        # Stem the words
        ps = PorterStemmer()
        words = [ps.stem(word) for word in words]

        # Recognize intent using regular expressions
        intent = self.get_intent(words)

        # Get response based on intent
        response = self.get_response(intent, words)

        return response

    def get_intent(self, words):
        # Define regular expressions for intents
        info_patterns = re.compile(r'info|details|tell me about|what is')

        # Match intents
        if info_patterns.search(' '.join(words)):
            return 'info'
        else:
            return 'unknown'

    def get_response(self, intent, words):
        # Get response based on intent
        if intent == 'info':
            # Assuming the user is asking for information about goods
            return self.get_goods_info(words)
        else:
            return "I'm not sure how to respond to that."

    def get_goods_info(self, words):
        search_term = ' '.join(words)
        try:
            self.cursor.execute("SELECT name, description FROM goods WHERE name = ? OR description = ?", (search_term, search_term))
            result = self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error executing SQL query: {e}")
            result = None

        if result:
            name, description = result
            return f"The good is {name}. Description: {description}"
        else:
            return "Sorry, I couldn't find any information about that good."
# Example usage
if __name__ == "__main__":
    chatbot = GoodsChatBot()

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = chatbot.process_message(user_input)
        print(f"Bot: {response}")