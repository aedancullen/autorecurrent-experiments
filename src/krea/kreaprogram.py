from llvmlite import ir as llvmir
from llvmlite import binding as llvmbinding
from ctypes import *

# llvm init
llvmbinding.initialize()
llvmbinding.initialize_native_target()
llvmbinding.initialize_native_asmprinter()




class KreaProgram:

	program = None

	DATA_TYPE = c_char
	DATA_UBITS = 8

	LENGTH_TYPE = c_uint64

	practice_functype = CFUNCTYPE(DATA_TYPE, LENGTH_TYPE)
	krun_functype = CFUNCTYPE(LENGTH_TYPE, POINTER(DATA_TYPE), LENGTH_TYPE, LENGTH_TYPE, practice_functype)
	compiler = None
	krun = None

	def __init__(self, program):

		self.program = program

		self.bake()


	def bake(self):

		module = llvmbinding.parse_assembly(blah)

		llvmtarget = llvmbinding.Target.from_default_triple().create_target_machine()
		
		self.compiler = llvmbinding.create_mcjit_compiler(module, llvmtarget)
		self.compiler.finalize_object()

		krun_pointer = self.compiler.get_pointer_to_function(module.get_function("krun"))

		self.krun = self.krun_functype(krun_pointer)


	def run2(self, data, practice_callback, memsize=1024):

		datalen = len(data)
		buffersize = datalen + memsize

		membuffer = bytearray(buffersize)
		data = bytes(data)
		membuffer[:datalen] = data

		def callback_wrapper(result_length):
			dataout = bytes(membuffer[:result_length])
			score_float = practice_callback(dataout)
			score_data = score_float * (2 ** self.DATA_UBITS - 1)
			return int(score_data)

		membuffer_datatype = self.DATA_TYPE * buffersize
		membuffer_carray = membuffer_datatype.from_buffer_copy(membuffer)
		membuffer_pointer = pointer(membuffer_carray)

		practice_function = self.practice_functype(callback_wrapper)
		result_length = self.krun(membuffer_pointer, buffersize, datalen, practice_function)

		dataout = bytes(membuffer[:result_length])
		return dataout



	def run(self, history, scores, practice_callback):

		nvals = len(history[0])

		while True:

			history_nrows = len(history)
			scores_nrows = len(scores)
			assert history_nrows == scores_nrows
			nrows = history_nrows

			history_unif = b''
			for row in history:
				history_unif += row

			history_datatype = c_char * len(history_unif)

			history_arr = history_datatype.from_buffer_copy(data_unif)
			history_pointer = pointer(history_arr)

			
			scores_unif = scores

			scores_datatype = c_double * len(scores_unif)

			scores_arr = scores_datatype(*scores_unif) # unpack list to pos. args
			scores_pointer = pointer(scores_arr)


			out_buffer = bytearray(nvals)
			out_datatype = c_char * nvals

			out_mutable = out_datatype.from_buffer(out_buffer)
			out_pointer = pointer(out_mutable)


			self.krun(out_pointer, history_pointer, scores_pointer, nvals, nrows)

			row_out = bytes(out_buffer) # krun has modified the buffer in memory

			running, score = practice_callback(row_out)
			if not running: break

			history.insert(0, row_out)
			scores.insert(0, score)


	def from_file(program_fn):

		with open(program_fn, "r") as file:

			return KreaProgram(file.read())


	def to_file(self, program_fn):

		with open(program_fn, "w") as file:

			file.write(self.program.encode())


	def from_data(data):
		pass


	def from_nothing():
		pass


	def to_data(self):
		pass