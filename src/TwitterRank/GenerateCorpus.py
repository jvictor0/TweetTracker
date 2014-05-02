from mrjob.job import MRJob
import json as simplejson

USERID_PREFIX = 'id:twitter.com:'

class GenerateCorpus(MRJob):

    def mapper(self, _, line):
        tweet = simplejson.loads(line)
        if 'twitter_lang' in tweet and tweet['twitter_lang'] == 'en' and 'actor' in tweet :
            user = tweet['actor']['id'][len(USERID_PREFIX) :]
            yield int(user), tweet['body']
            if 'retweetCount' in tweet and int(tweet['retweetCount']) > 0:
                tweeter = tweet['object']['actor']['id'][len(USERID_PREFIX) :]
                yield int(tweeter), tweet['body']

    def reducer(self, user, tweets):
        yield user, ' '.join(tweets)


if __name__ == '__main__':
    GenerateCorpus.run()
