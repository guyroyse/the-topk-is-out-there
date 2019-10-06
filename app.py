import os
os.environ['NLTK_DATA'] = './nltk_data'

from flask import Flask, request

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))

from redisbloom.client import Client

rb = Client()
rb.topkReserve('ufo_words', 10, 10, 5, 0.9)

# the Flask app
app = Flask(__name__, instance_relative_config=True)

# hello world as a route
@app.route('/hello')
def hello():
  return "👋🏻🌎"

@app.route('/words', methods=['POST'])
def words():
  data = request.form['sighting']
  s = data.lower()
  words = word_tokenize(s)

  words_filtered = []
  for w in words:
    if w not in stopWords:
      if w.isalpha():
        rb.topkAdd('ufo_words', w)

  top = rb.topkList('ufo_words')
  print(top)
  return "Done"

# kick off the Flask application
if __name__ == '__main__':
  app.run()
