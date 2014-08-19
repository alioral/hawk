from constants import strings, integers, lists
import twitter

import fdb
fdb.api_version(integers.API_VERSION)

api = twitter.Api(consumer_key= strings.CONSUMER_KEY,
                  consumer_secret= strings.CONSUMER_SECRET,
                  access_token_key= strings.ACCESS_TOKEN_KEY,
                  access_token_secret= strings.ACCESS_TOKEN_SECRET)

@fdb.transactional
def set_value(tr, username, word_dictionary):
  try:
    existing_word_dictionary = tr.get(username)
    print existing_word_dictionary
    if existing_word_dictionary:
      for w in word_dictionary:
        existing_word_dictionary[w] += 1
    else:
      tr.set(username, word_dictionary)
    tr.commit().wait()
    return
  except fdb.FDBError as error:
    tr.on_error(error).wait()

def get_word_dictionary(text):
  word_dictionary = dict()
  for word in text.split(' '):
    if word not in word_dictionary:
      word_dictionary[word] = 0
    word_dictionary[word] += 1
  return word_dictionary

def process_tweets(tr, terms = lists.DEFAULT_TERMS):
  tweets = api.GetSearch(term=terms, count= 100)
  users = []
  for t in tweets:
    user_screenname = str(t.user.screen_name)
    word_dictionary = str(get_word_dictionary(t.text))
    users.append(user_screenname)
    set_value(tr, user_screenname, word_dictionary)
  return users


if __name__ == '__main__':
  tr = fdb.open()
  # tr.clear_range('', '\xFF') - optional
  users = process_tweets(tr)
  for u in users:
    print 'User: ' + u
    words = eval(tr[u])
    for word in words.keys():
      print 'Term: ' + word + '\tFrequency: ' + str(words[word])
