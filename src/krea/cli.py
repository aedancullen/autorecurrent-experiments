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
		self.parser.add_argument("practice_file", type=lambda x:isfile(self.parser,x))
		self.parser.add_argument("program_file", type=lambda x:isfile(self.parser,x))
		self.parser.add_argument("output_directory", type=lambda x:isdir(self.parser,x))


	def run(self):
		args = self.parser.parse_args()
		practice_file = args.practice_file
		program_file = args.program_file
		output_directory = args.output_directory
		practice_file_basename = os.path.basename(practice_file)
		output_prefix = practice_file_basename[:practice_file_basename.rfind('.')]
		self.run_krealearn(self, practice_file, program_file, output_directory, output_prefix)

	def run_krealearn(self, practice_file, program_file, output_directory, output_prefix):

		log = log.KreaLog(output_directory, output_prefix)
		log.log_initinfo(practice_file, program_file, output_directory, output_prefix)

		practice = practice.KreaPractice(practice_file, log)
		program = program.KreaProgram.from_file(program_file)
		learner = learn.KreaLearn(practice, program, log)
		learner.run()
