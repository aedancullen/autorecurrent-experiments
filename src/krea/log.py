import logging
logging.basicConfig(format='%(asctime)s\t\t%(message)s', level=logging.DEBUG)

class KreaLog:

	output_directory = None
	output_prefix = None

	def __init__(self, output_directory, output_prefix):

		self.output_directory = output_directory
		self.output_prefix = output_prefix

	def log_initinfo(self, practice_file, program_file, output_directory, output_prefix):

		logging.info("Krea Recurrent-Evolving AGI - github.com/aedancullen/krea\n")
		logging.info("Practice file (.koh):\t" + practice_file)
		logging.info("Program file (.kcl):\t" + program_file)
		logging.info("Output directory:\t" + output_directory + "\n")


	def log_learn(self, highscore, latest_score, latest_program):
		
		logging.info("lv:learn\ths:{}\tls:{}".format(highscore, latest_score))

		if latest_score == highscore:

			name = self.output_directory + "/" + self.output_prefix + '-' + str(highscore) + ".kcl"
			latest_program.to_file(name)

			logging.info("lv:log\tWrote {}".format(name))

	#def log_practice(self, )