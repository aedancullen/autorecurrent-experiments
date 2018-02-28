from multiprocessing import Pool
from krea import program

class KreaPractice:

	problems = []

	pool = None

	def __init__(self, problems_dir):
		
		pool = multiprocessing.Pool()

	def run(self, program):

		def pfunc(args):
			program, inset, outset = args

			highest_score = -1

			def test_callback(programdata_out):
				program_out = program.KreaProgram.from_data(programdata_out)

				attempted_outset = []
				for item in inset:
					res = program_out.run(item)
					attempted_outset.append(res)

				score = TODO scoring
				if score > highest_score:
					highest_score = score

				return score

			executable = program.run(program.KreaProgram.from_nothing(), test_callback)
			test_callback(executable)

		
		parallel_iterator = pool.imap_unordered(func, iterator)

		results_list = list(parallel_iterator)

		

