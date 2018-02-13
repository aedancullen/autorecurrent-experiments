from llvmlite import ir as llvmir
from llvmlite import binding as llvmbinding
from ctypes import *

# llvm init
llvmbinding.initialize()
llvmbinding.initialize_native_target()
llvmbinding.initialize_native_asmprinter()




class KreaProgram:

	program = []

	compiler = None
	krun = None

	def __init__(self, program=[]):
		self.program = program

		llvmtarget = llvmbinding.Target.from_default_triple().create_target_machine()
		module = self.bake()

		self.compiler = llvmbinding.create_mcjit_compiler(module, llvmtarget)
		self.compiler.finalize_object()

		krun_pointer = self.compiler.get_pointer_to_function(module.get_function("krea_run"))

		krun_functype = CFUNCTYPE(None, POINTER(c_char), POINTER(c_char), POINTER(c_double), c_uint64, c_uint64)

		self.krun = krun_functype(krun_pointer)


	def bake(self):

		module = llvmbinding.parse_assembly(blah)
		return module

	def run(self, history, scores, practice_callback):

		nvals = len(history[0])

		while True:

			history_nrows = len(history)
			scores_nrows = len(scores)
			assert history_nrows == scores_nrows

			history_unif = b''
			for row in history:
				history_unif += row

			history_datatype = c_char * len(history_unif)

			history_arr = history_datatype.from_buffer_copy(data_unif)
			history_pointer = pointer(history_arr)

			
			scores_unif = scores

			scores_datatype = c_double * len(scores_unif)

			scores_arr = scores_datatype.from_buffer_copy(scores_unif)
			scores_pointer = pointer(scores_arr)


			out_buffer = bytearray(nvals)
			out_datatype = c_char * nvals

			out_mutable = out_datatype.from_buffer(out_buffer)
			out_pointer = pointer(out_mutable)


			self.krun(out_pointer, history_pointer, scores_pointer, nvals, nrows)

			row_out = bytes(out_pointer.contents[:nvals])

			running, score = practice_callback(row_out)
			if not running: break

			history.insert(0, row_out)
			scores.insert(0, score)


	def from_file(program_fn):
		pass


	def to_file(self, program_fn):
		pass


	def from_data(data):
		pass


	def to_data(self):
		pass