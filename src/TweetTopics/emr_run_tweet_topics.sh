#!/bin/sh

indir='s3n://tweettrack/Twitter_Firehose_Subset/';
outdir='s3n://tweettrack/Twitterrank_Full_Output/';
outdirnoslash='s3://tweettrack/Twitterrank_Full_Output';
temphdfsdir='hdfs:///tweettopictemp/';
temphdfsdir2='hdfs:///tweettopictemp2/';
temphdfsdir3='hdfs:///tweettopictemp3/';
rankdir='s3n://tweettrack/Twitterrank_Full_Output/';
numtopics=30;
nummappers=9;
numreducers=9;
mrldajar='s3n://mrldajarbucket/Mr.LDA-0.0.1.jar';
stopwords='s3n://mrldajarbucket/stopwords';
setnums='--jobconf mapreduce.job.maps=7 --jobconf mapreduce.job.maps=7 --num-ec2-instances 16 --ec2-master-instance-type m1.large --ec2-instance-type m3.xlarge'
s3distcpjar='/home/hadoop/lib/emr-s3distcp-1.0.jar' #cluster itself's home

#python GenerateTweetCorpus.py -c mrjob.conf  -r emr $indir --output-dir $outdirnoslash/tweetcorpus --no-output --jobconf mapred.skip.map.max.skip.records=100;
#python RunMrJobs.py emr $mrldajar $outdir $nummappers $numreducers $stopwords $temphdfsdir $temphdfsdir2 $s3distcpjar $rankdir
#python RunTweetTopicHive.py emr $outdir $temphdfsdir3 $s3distcpjar

priors='priors';
wc='wordcounts/wordcounts';
wp='wordprobs';
python TweetTopics.py $priors $wc $wp;
