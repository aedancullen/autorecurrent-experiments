from krea import kreaprogram


class KreaLearn:

	practice = None
	program = None
	log = None

	highscore = -1

	latest_program = None

	def __init__(self, practice, program, log):
		self.practice = practice
		self.program = program
		self.log = log


	def run(self):

		def practice_callback(programdata_out):

			program_out = kreaprogram.KreaProgram.from_data(programdata_out)
			self.latest_program = program_out
			score = self.practice.run(program_out)
			self.log.run(program_out, score)

			if score > highscore:
				self.highscore = score
				raise ScoreImproved()

			return score
		

		while True:
			programdata = self.program.to_data()
			try:
				programdata_out = self.program.run(programdata, practice_callback)
				practice_callback(programdata_out)
			except ScoreImproved:
				self.program = self.latest_program
				continue

			return
