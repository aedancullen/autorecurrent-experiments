from multiprocessing import Pool
from krea import program
import math

class KreaPractice:

	problems = []
	pool = None
	log = None

	def __init__(self, practice_file, log):
		
		pool = multiprocessing.Pool()

		self.log = log

		with open(practice_file, "rb") as file:
			problems = pickle.load(file)


	def score(self, attempted_dataset, target_dataset):

		assert len(attempted_dataset) == len(target_dataset)

		error = 0
		for i in range(len(attempted_dataset)):

			len_attemptedset_i = len(attempted_dataset[i])
			len_targetset_i = len(target_dataset[i])

			maxlen = max(len_attemptedset_i, len_targetset_i)
			attempted_fullitem = bytearray(maxlen)
			target_fullitem = bytearray(maxlen)

			attempted_fullitem[:len_attemptedset_i] = attempted_dataset[i]
			target_fullitem[:len_targetset_i] = target_dataset[i]

			for i in range(maxlen):
				error += (attempted_fullitem[i] - target_fullitem[i]) ** 2

		return error / (maxlen * len(attempted_dataset))


	def run(self, program):

		tasklist = [(inset, outset, program) for inset, outset in problems]
		iterator = iter(tasklist)

		def pfunc(args):
			program, inset, outset = args

			best_score = 0

			def test_callback(programdata_out):
				program_out = program.KreaProgram.from_data(programdata_out)

				attempted_outset = []
				for item in inset:

					latest_result = item # simple init if no iters succeed w/o ProgramUnresponsive

					def score_individual(data_out):
						latest_result = data_out
						target_data = outset[inset.find(item)]
						return self.score([latest_result,], [target_data,])

					try:
						latest_result = program_out.run(item, score_individual)
					except program.ProgramUnresponsive:
						attempted_outset.append(b'')

					attempted_outset.append(latest_result)

				score = self.score(attempted_outset, outset)

				#self.log.log_practice(best_score, score)

				if score < best_score:
					best_score = score

				return score

			try:
				executable = program.run(program.KreaProgram.from_nothing().to_data(), test_callback)
				test_callback(executable)
			except program.ProgramUnresponsive:
				pass

			return best_score

		
		parallel_iterator = pool.imap_unordered(pfunc, iterator)

		results_list = list(parallel_iterator)
		return sum(results_list) / len(results_list)

		

