import os
os.environ['NLTK_DATA'] = './nltk_data'

import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from redisbloom.client import Client

INPUT_FILE = 'nuforc_reports.csv'
STOP_WORDS = set(stopwords.words('english'))
SAMPLE_SIZE = 100

def main():

  # read in the CSV data
  df = pd.read_csv(INPUT_FILE, encoding='utf-8')
  print(f"Read {df.shape[0]} rows and {df.shape[1]} columns from '{INPUT_FILE}'.")

  # pick some random ufo sightings
  df = df.sample(n=SAMPLE_SIZE)
  print(f"Selected {SAMPLE_SIZE} random rows.")

  # drop all columns except 'summary', 'text', and 'shape'
  df = df.filter(items=['summary', 'text', 'shape'])
  print(f"Dropped all columns except {df.columns.to_list()}.")

  # make sure they're all strings
  df = df.astype(str)

  # setup the client
  rb = Client()

  # remove any old keys
  rb.delete('ufo_words', 'ufo_shapes')

  # setup some Top-K action!
  rb.topkReserve('ufo_words', 10, 10, 5, 0.9)
  rb.topkReserve('ufo_shapes', 5, 4, 5, 0.9)

  # add the words and shapes
  for index, row in df.iterrows():

    shape = row['shape']
    summary = parse_words(row['summary'])
    text = parse_words(row['text'])

    print(f"Row: {index + 1} Shape: {shape} Summary: {len(summary)} Text: {len(text)}")

    rb.topkAdd('ufo_shapes', shape)
    [rb.topkAdd('ufo_words', w) for w in summary]
    [rb.topkAdd('ufo_words', w) for w in text]

  # print the results
  top_words = [(word, rb.topkCount('ufo_words', word)) for word in rb.topkList('ufo_words')]
  top_shapes = [(shape, rb.topkCount('ufo_shapes', shape)) for shape in rb.topkList('ufo_shapes')]

  print()
  print("Top Words:", top_words)
  print("Top Shapes :", top_shapes)

def parse_words(text):
  words = word_tokenize(text.lower())
  return [w for w in words if w not in STOP_WORDS and w.isalpha()]

main()
