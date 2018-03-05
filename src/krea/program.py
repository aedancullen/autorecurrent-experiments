from llvmlite import ir as llvmir
from llvmlite import binding as llvmbinding
from ctypes import *
import signal

# llvm init
llvmbinding.initialize()
llvmbinding.initialize_native_target()
llvmbinding.initialize_native_asmprinter()


class ProgramUnresponsive(Exception):
    pass

class KreaProgram:

	program = None

	DATA_TYPE = c_char
	DATA_UBITS = 8

	LENGTH_TYPE = c_uint64
	LENGTH_UBITS = 64

	practice_functype = CFUNCTYPE(DATA_TYPE)
	krun_functype = CFUNCTYPE(None, POINTER(DATA_TYPE), LENGTH_TYPE, practice_functype)
	compiler = None
	krun = None

	def __init__(self, program):

		self.program = program

		self.bake()


	def irbuild(self):
		# self.program in, ir_module out

		cell_t = ir.IntType(DATA_UBITS)
		length_t = ir.IntType(LENGTH_UBITS)

		ir_module = llvmir.Module()

		callback_func_t = llvmir.FunctionType(length_t, ())

		krun_func_t = llvmir.FunctionType(llvmir.VoidType(), (cell_t.as_pointer(), length_t, callback_func_t.as_pointer()))
		krun_func = llvmir.Function(module, krun_func_t, "krun")
		krun_entry = krun_func.append_basic_block('entry')
		krun_builder = llvmir.IRBuilder(krun_entry)

		ptr, length, callback = krun_func.args

		zero = cell_t(0)
		one = cell_t(1)
		minus_one = cell_t(-1)


	def bake(self):

		ir_module = self.irbuild()

		llvm_module = llvmbinding.parse_assembly(str(ir_module))

		#optimizer = llvmbinding.create_pass_manager_builder()
    	#optimizer.opt_level = 3
    	#optimizer.size_level = 0
    	#passman = llvm.create_module_pass_manager()
    	#optimizer.populate(passman)
    	#passman.run(module)

		llvmtarget = llvmbinding.Target.from_default_triple().create_target_machine()
		
		self.compiler = llvmbinding.create_mcjit_compiler(llvm_module, llvmtarget)
		self.compiler.finalize_object()

		krun_pointer = self.compiler.get_function_address("krun")

		self.krun = self.krun_functype(krun_pointer)


	def run(self, data, practice_callback, buffersize=1024):

		def unresponsive_handler(signum, frame):
			raise ProgramUnresponsive()

		datalen = len(data)
		assert buffersize > datalen + 1

		membuffer = bytearray(buffersize)
		membuffer[0] = datalen
		membuffer[1:1+datalen] = data

		def callback_wrapper():
			result_length = membuffer[0]

			dataout = membuffer[1:1+result_length]
			score_float = practice_callback(dataout)
			score_data = score_float * (2 ** self.DATA_UBITS - 1)
			return int(score_data)

		membuffer_datatype = self.DATA_TYPE * buffersize
		membuffer_carray = membuffer_datatype.from_buffer(membuffer) # allows mutation of membuffer in-place
		membuffer_pointer = pointer(membuffer_carray)

		practice_function = self.practice_functype(callback_wrapper)

		signal.signal(signal.SIGALRM, unresponsive_handler) # only on unix
		signal.alarm(5)

		self.krun(membuffer_pointer, buffersize, practice_function)

		signal.alarm(0)

		result_length = membuffer[0]
		dataout = membuffer[1:1+result_length]

		return dataout



	def from_file(program_fn):

		with open(program_fn, "rb") as file:

			return KreaProgram(file.read())


	def to_file(self, program_fn):

		with open(program_fn, "wb") as file:

			file.write(self.program)


	def from_data(data):
		
		return KreaProgram(data)


	def from_nothing():
		pass


	def to_data(self):
		
		return self.program