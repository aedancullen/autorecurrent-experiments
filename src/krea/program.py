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

	DATA_TYPE = c_int
	DATA_UBITS = 32

	LENGTH_TYPE = c_int
	LENGTH_UBITS = 32

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
		krun_func = llvmir.Function(ir_module, krun_func_t, "krun")
		krun_entry = krun_func.append_basic_block("entry")
		krun_builder = llvmir.IRBuilder(krun_entry)

		ptr, length, callback = krun_func.args

		zero = cell_t(0)
		one = cell_t(1)
		minus_one = cell_t(-1)

		rand_t = ir.FunctionType(cell_t, [])
		rand = ir.Function(ir_module, rand_t, "rand")

		stack = []
		class Loop:
    		pass

        for instr in program:

            if instr == b'\x01':
                ptr = krun_builder.gep(ptr, [one])
            elif instr == b'\x02':
                ptr = krun_builder.gep(ptr, [minus_one])
            elif instr == b'\x03':
                value = krun_builder.load(ptr)
                value = krun_builder.add(value, one)
                krun_builder.store(value, ptr)
            elif instr == b'\x04':
                value = krun_builder.load(ptr)
                value = krun_builder.sub(value, one)
                krun_builder.store(value, ptr)

            elif instr == b'\x05':
                loop = Loop()
                loop.entry = krun_builder.block
                loop.body = krun_builder.append_basic_block()
                loop.exit = krun_builder.append_basic_block()

                value = krun_builder.load(ptr)
                cond = krun_builder.icmp_unsigned("!=",value,zero)
                krun_builder.cbranch(cond, loop.body, loop.exit)

                with krun_builder.goto_block(loop.exit):
                    loop.ptr_exit = krun_builder.phi(pcell_t)
                    loop.ptr_exit.add_incoming(ptr, loop.entry)

                with krun_builder.goto_block(loop.body):
                    loop.ptr_body = krun_builder.phi(pcell_t)
                    loop.ptr_body.add_incoming(ptr, loop.entry)

                krun_builder.position_at_end(loop.body)
                ptr = loop.ptr_body
                stack.append(loop)

            elif instr == b'\x06':
                if len(stack) == 0:
                    continue

                loop = stack.pop()

                loop.ptr_body.add_incoming(ptr, krun_builder.block)
                loop.ptr_exit.add_incoming(ptr, krun_builder.block)

                value = krun_builder.load(ptr)
                cond = krun_builder.icmp_unsigned("!=",value, zero)
                krun_builder.cbranch(cond, loop.body, loop.exit)

                ptr = loop.ptr_exit
                krun_builder.position_at_end(loop.exit)

            elif instr == b'\x07':
                value = krun_builder.call(callback, ())
                value = krun_builder.trunc(value, cell_t)
                krun_builder.store(value, ptr)

            elif instr == b'\x08':
                value = krun_builder.call(rand, ())
                value = krun_builder.trunc(value, cell_t)
                krun_builder.store(value, ptr)


        return ir_module



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
			result_length = max(membuffer[0], len(membuffer) - 1)
			dataout = membuffer[1:1+result_length]

			score = practice_callback(dataout)
			return int(score)

		membuffer_datatype = self.DATA_TYPE * buffersize
		membuffer_carray = membuffer_datatype.from_buffer(membuffer) # allows mutation of membuffer in-place
		membuffer_pointer = pointer(membuffer_carray)

		practice_function = self.practice_functype(callback_wrapper)

		signal.signal(signal.SIGALRM, unresponsive_handler) # only on unix
		signal.alarm(5)

		self.krun(membuffer_pointer, buffersize, practice_function)

		signal.alarm(0)

		result_length = max(membuffer[0], len(membuffer) - 1)
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
		return KreaProgram(b'')


	def to_data(self):
		
		return self.program