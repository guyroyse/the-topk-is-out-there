from flask import Flask, jsonify

from redisbloom.client import Client

client = Client()

# the Flask app
app = Flask(__name__, instance_relative_config=True)

@app.route('/shapes')
def shapes():

  top_shapes = [{
    'shape': shape,
    'count': client.topkCount('ufo_shapes', shape)[0]
  } for shape in client.topkList('ufo_shapes')]

  return jsonify(top_shapes)

@app.route('/words')
def words():

  top_words = [{ 
    'word': word, 
    'count': client.topkCount('ufo_words', word)[0]
  } for word in client.topkList('ufo_words')]

  return jsonify(top_words)


# kick off the Flask application
if __name__ == '__main__':
  app.run()
