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

		krun_functype = CFUNCTYPE(POINTER(c_ubyte), POINTER(c_ubyte), c_uint64, c_uint64)

		self.krun = krun_functype(krun_pointer)


	def bake(self):

		module = llvmbinding.parse_assembly(blah)
		return module

	def run(self, data, practice_callback):

		running = True
		while running:

			data_unif = b''
			for row in data:
				data_unif += row

			ubyte_arr_datatype = c_ubyte * len(data_unif)

			ubyte_arr = ubyte_arr_datatype.from_buffer_copy(data_unif)
			ipointer = pointer(ubyte_arr)

			nvals = len(data[0])
			nrows = len(data)

			opointer = self.krun(ipointer, nvals, nrows)

			row_out = bytes(opointer.contents[:nvals])

			data.insert(0, row_out)

			running = practice_callback(data)


	def from_file(program_fn):
		pass


	def to_file(self, program_fn):
		pass


	def from_data(data):
		pass


	def to_data(self):
		pass