from multiprocessing import Pool
from krea import program

class KreaPractice:

	problems = []

	pool = None

	log = None

	def __init__(self, practice_file, log):
		
		pool = multiprocessing.Pool()

		self.log = log

		with open(practice_file, "rb") as file:
			problems = pickle.load(file)

	def run(self, program):

		tasklist = [(inset, outset, program) for inset, outset in problems]
		iterator = iter(tasklist)

		def pfunc(args):
			program, inset, outset = args

			highest_score = 0

			def test_callback(programdata_out):
				program_out = program.KreaProgram.from_data(programdata_out)

				attempted_outset = []
				for item in inset:

					latest_result = item # simple init if no iters succeed w/o ProgramUnresponsive

					def score_individual(data_out):
						latest_result = data_out
						target_data = outset[inset.find(item)]
						return TODO scoring

					try:
						latest_result = program_out.run(item, score_individual)
					except program.ProgramUnresponsive:
						pass

					attempted_outset.append(latest_result)

				score = TODO scoring
				if score > highest_score:
					highest_score = score

				return score

			try:
				executable = program.run(program.KreaProgram.from_nothing(), test_callback)
				test_callback(executable)
			except program.ProgramUnresponsive:
				pass

			return highest_score

		
		parallel_iterator = pool.imap_unordered(pfunc, iterator)

		results_list = list(parallel_iterator)

		

