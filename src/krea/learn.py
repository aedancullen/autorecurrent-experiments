from krea import program

class ScoreImproved(Exception):
    pass

class KreaLearn:

	practice = None
	program = None
	log = None

	highscore = 0

	latest_program = None
	latest_score = None

	def __init__(self, practice, program, log):
		self.practice = practice
		self.program = program
		self.log = log


	def run(self):

		self.highscore = self.practice.run(self.program)
		self.log.log_main(self.highscore, self.highscore, self.program)

		def practice_callback(programdata_out):

			program_out = program.KreaProgram.from_data(programdata_out)
			self.latest_program = program_out
			self.latest_score = self.practice.run(self.latest_program)

			self.log.log_learn(self.highscore, self.latest_score, self.latest_program)

			if score < highscore:
				self.highscore = self.latest_score

				raise ScoreImproved()

			return score
		

		while True:
			programdata = self.program.to_data()
			try:
				programdata_out = self.program.run(programdata, practice_callback)
				practice_callback(programdata_out)
			except ScoreImproved:
				pass
			except program.ProgramUnresponsive:
				pass
			
			# and proceed with newest program
			self.program = self.latest_program
