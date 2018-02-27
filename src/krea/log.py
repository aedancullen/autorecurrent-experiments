import logging
logging.basicConfig(format='%(asctime)s\t\t%(message)s', level=logging.DEBUG)

class KreaLog:

	programs_dir = None
	programs_prefix = None

	def __init__(self, programs_dir, programs_prefix):

		pass


	def log_main(self, highscore, latest_score, latest_program):
		
		logging.info("hs:{}\tls:{}".format(highscore, latest_score))

		if latest_score == highscore:

			latest_program.to_file(programs_dir + '/' + programs_prefix + '-' + str(highscore) + ".kcl")
