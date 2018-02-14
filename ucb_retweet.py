from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import json, sys
import config as cfg

arm = ['856905595189776384']
matches = ['ucb']

auth_handler = OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth_handler.set_access_token(cfg.access_token, cfg.access_token_secret)
 
twitter_client = API(auth_handler)

class PyStreamListener(StreamListener):
	def on_data(self, data):
		tweet = json.loads(data)
		loc = tweet['text'].split(":")[0].lower()
		if any(match in loc for match in matches):
			clean_and_print(tweet['text'])
		# 	clean_and_print('[Y]', tweet['text'])
		# else:
		# 	clean_and_print('[N]', tweet['text'])
		return True

	def on_error(self, status):
		print(status)

def clean_and_print(*strs):
	clean_strs = []
	for s in strs:
		s = s.replace(u'\u2642', 'm').replace(u'\u2640', 'f')
		s = s.encode('ascii', 'ignore').decode('utf-8')
		clean_strs.append(s)
	print(*clean_strs)
	sys.stdout.flush()

if __name__ == '__main__':
	listener = PyStreamListener()
	stream = Stream(auth_handler, listener)
	stream.filter(follow=arm)