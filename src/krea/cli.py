from krea import learn
from krea import practice
from krea import program
from krea import log
import argparse
import os

def start_cli():

	cli = KreaCLI()
	cli.run()


def isfile(parser, fn):
    if not os.path.isfile(fn):
        parser.error('{} is not a file'.format(fn))
    else:
        return fn


def isdir(parser, fn):
    if not os.path.isdir(fn):
        parser.error('{} is not a directory'.format(fn))
    else:
        return fn


class KreaCLI:

	parser = None

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			prog = "krea",
			description="Krea Recurrent-Evolving AGI - github.com/aedancullen/krea"
		)
		self.parser.add_argument("practice_file", type=lambda x:isfile(parser,x))
		self.parser.add_argument("program_file", type=lambda x:isfile(parser,x))
		self.parser.add_argument("output_directory", type=lambda x:isdir(parser,x))


	def run(self) :
		args = self.parser.parse_args()
		problems_dir = args.problems_directory + "/"
		programs_dir = args.programs_directory
		programs_prefix = os.path.basename(os.path.dirname(problems_dir))
		program_file = args.initial_program_file
		self.run_krealearn(self, problems_dir, programs_dir, programs_prefix, program_file)

	def run_krealearn(self, problems_dir, programs_dir, programs_prefix, program_fn):

		practice = practice.KreaPractice(problems_dir)
		program = program.KreaProgram.from_file(program_fn)
		log = log.KreaLog(programs_dir, programs_prefix)
		learner = learn.KreaLearn(practice, program, log)
		learner.run()
