import sqlite3
import spacy
import re

class GoodsChatBot:
    def __init__(self, database_path='goods.db'):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.nlp = spacy.load('en_core_web_sm')

    def process_message(self, message):
        # Process the message using SpaCy
        doc = self.nlp(message.lower())

        # Recognize intent using regular expressions
        intent = self.get_intent(doc)

        # Get response based on intent
        response = self.get_response(intent, doc)

        return response

    def get_intent(self, doc):
        # Define regular expressions for intents
        info_patterns = re.compile(r'info|details|tell me about|what is')
        availability_patterns = re.compile(r'is\s+(\w+)\s+available\??|do\s+you\s+have\s+(\w+)\??|can\s+i\s+find\s+(\w+)\s+in\s+stock\??')

        # Match intents
        for token in doc:
            if token.text in ('info', 'details', 'tell me about', 'what is') or info_patterns.search(token.text):
                return 'info'
            elif availability_patterns.search(token.text):
                return 'availability'
        return 'unknown'

    def get_response(self, intent, doc):
        # Get response based on intent
        if intent == 'info':
            # Assuming the user is asking for information about goods
            return self.get_goods_info(doc)
        elif intent == 'availability':
            return self.check_goods_availability(doc)
        else:
            return "I'm not sure how to respond to that."

    def get_goods_info(self, doc):
        search_term = doc.text.split("about")[1].strip()
        print("Search term:", search_term)  # Debugging print
        try:
            self.cursor.execute("SELECT name, description FROM goods WHERE name LIKE ?", ('%' + search_term + '%',))
            result = self.cursor.fetchone()
            print("Result:", result)  # Debugging print
        except sqlite3.Error as e:
            print(f"Error executing SQL query: {e}")
            result = None

        if result:
            name, description = result
            return f"The good is {name}. Description: {description}"
        else:
            return "Sorry, I couldn't find any information about that good."

    def check_goods_availability(self, doc):
        search_terms = [token.lemma_ for token in doc if not token.is_stop and token.lemma_]
        search_term = ' '.join(search_terms)
        print("Search term:", search_term)  # Debugging print
        try:
            self.cursor.execute("SELECT name FROM goods WHERE name LIKE ?", ('%' + search_term + '%',))
            result = self.cursor.fetchone()
            print("Result:", result)  # Debugging print
        except sqlite3.Error as e:
            print(f"Error executing SQL query: {e}")
            result = None

        if result:
            return f"Yes, {search_term.capitalize()} is available."
        else:
            return f"Sorry, {search_term.capitalize()} is not available at the moment."

# Example usage
if __name__ == "__main__":
    chatbot = GoodsChatBot()

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = chatbot.process_message(user_input)
        print(f"Bot: {response}")

    # Close the database connection
    chatbot.conn.close()