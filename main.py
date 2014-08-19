from constants import strings, integers, lists
import twitter, time

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
    if existing_word_dictionary:
      existing_word_dictionary = eval(existing_word_dictionary.value)
      for w in word_dictionary.keys():
        if w not in existing_word_dictionary:
          existing_word_dictionary[w] = 0
        existing_word_dictionary[w] += 1
      tr.set(username, str(existing_word_dictionary))
    else:
      tr.set(username, str(word_dictionary))
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
    word_dictionary = get_word_dictionary(t.text)
    users.append(user_screenname)
    set_value(tr, user_screenname, word_dictionary)
  return users

def sort_results_by_value(dictionary):
  return sorted(dictionary, key= dictionary.get, reverse=True)[:integers.TOP_WORD_COUNT]

def print_db(tr):
  for key, value in tr['':'\xFF']:
    result_dictionary = eval(value)
    result_dictionary = sort_results_by_value(result_dictionary)
    print 'User: ' + key
    print 'Top ' + str(integers.TOP_WORD_COUNT) + ' words '
    print map(lambda x:str(x), result_dictionary)

if __name__ == '__main__':
  tr = fdb.open()
  number_of_checks = integers.DEFAULT_CHECK_NUMBER
  tr.clear_range('', '\xFF') # Fresh DB everytime
  for i in xrange(number_of_checks):
    print 'Check #' + str(i + 1)
    users = process_tweets(tr)
    time.sleep(integers.DEFAULT_SLEEP_SECOND)
  print 'Results'
  print_db(tr)
