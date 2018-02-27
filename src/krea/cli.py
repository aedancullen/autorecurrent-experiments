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
		self.parser.add_argument("problemsdir", type=lambda x:isdir(parser,x))
		self.parser.add_argument("programsdir", type=lambda x:isdir(parser,x))
		self.parser.add_argument("programfile", type=lambda x:isfile(parser,x))


	def run(self) :
		args = self.parser.parse_args()
		problems_dir = args.problemsdir + "/"
		programs_dir = args.programsdir
		programs_prefix = os.path.basename(os.path.dirname(problems_dir))
		program_file = args.programfile
		self.run_krealearn(self, problems_dir, programs_dir, programs_prefix, program_file)

	def run_krealearn(self, problems_dir, programs_dir, programs_prefix, program_fn):

		practice = practice.KreaPractice(problems_dir)
		program = program.KreaProgram.from_file(program_fn)
		log = log.KreaLog(programs_dir, programs_prefix)
		learner = learn.KreaLearn(practice, program, log)
		learner.run()
