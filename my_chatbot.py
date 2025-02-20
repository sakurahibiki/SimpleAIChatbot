from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import sqlite3

common_abbreviations = {
    "hru" : "how are you",
    "brb" : "be right back",
    "idk" : "i dont know",
    "idc" : "i dont care",
    "tbh" : "to be honest",
    "ngl" : "not going to lie",
}

#The chicken crossed the street
#["the", "chicken", "crossed", "the", "street"]
#["the", "chicken", "cross", "the", "street"]
#["chicken", "cross", "street"]

important_words = {"who", "what", "when", "where", "why", "how", "whom", "i", "you", "no", "not", "never"}

chatbot_data = ChatBot(
    name="Chatty Patty",
    storage_adapter = "chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///user_chat_database.sqlite3"
    )

trainer = ChatterBotCorpusTrainer(chatbot_data)
trainer.train("chatterbot.corpus.english")

def preprocessor(text):
    text = re.sub(r'[\.\!\,\:\;\"]', '', text)
    text = text.lower()

    words = text.split()
    words = [common_abbreviations[word] if word in common_abbreviations else word for word in words]
    text = " ".join(words)
    
    tokenized_words = word_tokenize(text)
    
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    lemmatized_words = [lemmatizer.lemmatize(token, pos='v') for token in tokenized_words if token not in stop_words or token in important_words]
    
    
    result = ""
    for i in range(len(lemmatized_words)):
        if lemmatized_words[i] == "?":
            result = result.rstrip() + "?"
        else:
            result += lemmatized_words[i] + " "

    return result.strip()

def clear_chat_history():
    connection = sqlite3.connect("user_chat_database.sqlite3")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM statement")
    connection.commit() 
    connection.close()
        


def chat(user_input):
    preprocessed_input = preprocessor(user_input)
    response = chatbot_data.get_response(preprocessed_input)

    return response