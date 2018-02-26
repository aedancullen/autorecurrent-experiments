from krea import kreaprogram


class KreaLearn:

	practice = None
	program = None
	log = None

	highscore = -1

	latest_program = None
	latest_score = None

	def __init__(self, practice, program, log):
		self.practice = practice
		self.program = program
		self.log = log


	def run(self):

		def practice_callback(programdata_out):

			program_out = kreaprogram.KreaProgram.from_data(programdata_out)
			self.latest_program = program_out
			self.latest_score = self.practice.run(self.latest_program)

			self.log.log_main(self.highscore, self.latest_score, self.latest_program)

			if score > highscore:
				self.highscore = self.latest_score
				self.program = self.latest_program

				raise ScoreImproved()

			return score / highscore
		

		while True:
			programdata = self.program.to_data()
			try:
				programdata_out = self.program.run(programdata, practice_callback)
				practice_callback(programdata_out)
			except ScoreImproved:
				continue

			return
