import boto, sys, time
from subprocess import call
#hive -hiveconf TROPATH=$outdir -f ldapostprocess.q;

def check_connection(conn, jobid):
	status = conn.describe_jobflow(jobid)
	#terminal state
	if status in [u'COMPLETED', u'FAILED', u'TERMINATED']:
		return True
	return False

def wait_until(pred, timeout, period=30):
	mustend = time.time() + timeout
	while time.time() < mustend:
		if pred(): return True
		time.sleep(period)

if __name__ == "__main__":
	if sys.argv[1] == "emr":
		args1 = [u's3://us-east-1.elasticmapreduce/libs/hive/hive-script',
				 u'--base-path',
				 u's3://us-east-1.elasticmapreduce/libs/hive/',
				 u'--install-hive',
				 u'--hive-versions',
				 u'0.7']
		args2 = [u's3://us-east-1.elasticmapreduce/libs/hive/hive-script',
				 u'--base-path',
				 u's3://us-east-1.elasticmapreduce/libs/hive/',
				 u'--hive-versions',
				 u'0.7',
				 u'--run-hive-script',
				 u'--args',
				 u'-f',
				 s3_query_file_uri]
		steps = []
		for name, args in zip(('Setup Hive','Run Hive Script'),(args1,args2)):
			step = JarStep(name,
						   's3://us-east-1.elasticmapreduce/libs/script-runner/script-runner.jar',
						   step_args=args,
						   #action_on_failure="CANCEL_AND_WAIT"
						   )
			#should be inside loop
			steps.append(step)
# Kick off the job
		jobid = EmrConnection().run_jobflow(name, s3_log_uri,
										   steps=steps,
										   master_instance_type=master_instance_type,
										   slave_instance_type=slave_instance_type,
										   num_instances=num_instances,
										   hadoop_version="0.20")
		wait_until(lambda: check_connection(conn, jobid), 86400)
	else:
		"""
		Without elastic map reduce
		"""
		assert sys.argv[2]
		outdir_str = "TROPATH=%s" % sys.argv[2]
		call(["hive", "-hiveconf", outdir_str, "-f", "ldapostprocess.q"])