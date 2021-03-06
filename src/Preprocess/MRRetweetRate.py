from mrjob.job import MRJob
import json as simplejson
from datetime import datetime, timedelta

class MRRetweetRate(MRJob):
	
	def mapper_get_times(self, _, line):
		startTime = datetime.strptime('2014-03-01T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ') 
		tweet = simplejson.loads(line)
		language = 'es'
		if 'twitter_lang' in tweet : 
			language = tweet['twitter_lang']

		if language == 'en' :
			if 'id' in tweet and 'retweetCount' in tweet :
				tweetid = tweet['id'][len('tag:search.twitter.com,2005:') : ]
				tweeter = tweet['actor']['id'][len('id:twitter.com:') :]
				retweetTime = datetime.strptime(tweet['postedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
				creationTime = retweetTime
				if tweet['retweetCount'] > 0 :
					tweeter = tweet['object']['actor']['id'][len('id:twitter.com:') :]	
					tweetid = tweet['object']['id'][len('object:search.twitter.com,2005:') :]
					creationTime = datetime.strptime(tweet['object']['postedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
				if (creationTime - startTime).total_seconds() > 0 :
						timeDelta = (retweetTime - startTime).total_seconds() - (creationTime - startTime).total_seconds()
						if timeDelta < 300 :
							yield tweetid, (tweeter, int(timeDelta/30))
						elif timeDelta >= 600 :
							yield tweetid, ("ACTUAL", tweet['retweetCount'])	
										
				
	def reducer_compute_rate(self, tweetid, stats):
		rates = [0 for i in range(10)]
		actual = 0
		tweeter = "NONE"
		for u, t in stats :
			if u == "ACTUAL" :
				actual = t
			else :
				tweeter = u
				rates[t] = rates[t] + 1
		if actual == 0 :
			actual = sum(rates)

		if tweeter != "NONE":
			yield None, ('%s' % tweetid + ' ' + tweeter + ' ' + ' '.join(map(str, rates)) + ' ' + str(actual))
	
	def steps(self):
		return [
			self.mr(mapper=self.mapper_get_times,
				reducer=self.reducer_compute_rate)
		]

if __name__ == '__main__':
    MRRetweetRate.run()
