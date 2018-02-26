import logging
logging.basicConfig(format='%(asctime)s\t\t%(message)s', level=logging.DEBUG)

class KreaLog:

	def __init__(self):

		pass


	def log_main(self, highscore, latest_score, latest_program):
		
		logging.info("hs:{}\tls:{}".format(highscore, latest_score))

