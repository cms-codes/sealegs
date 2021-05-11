#!/usr/bin/python3

import sys
import os.path
from subprocess import Popen, PIPE

valid_commands = ["--name", "--namespace", "--from-file"]
file_list = []
namespace = ""
secret_name = ""

create_secrets_cmd_a = ["kubectl", "--namespace", "default", "create", 
						"secret", "generic", "sealegs-secrets"]
create_secrets_cmd_b = ["--dry-run=client", "-oyaml"]
create_ns_idx = 2
create_name_idx = 6

seal_secrets_cmd = ["kubeseal", "--format", "yaml", "--namespace", "default"]
seal_ns_idx = 4

def PrintHelpAndExit():
	print(sys.argv[0] + " --name [SECRET NAME] --namespace [NAMESPACE] --from-file [SECRET1] --from-file [SECRET2] --from-file [...]")
	sys.exit(-1)

def ErrorAndExit(error_name):
	print("Error! " + error_name)
	sys.exit(-1)

def GetArguments():
	arg_i = 1
	global secret_name
	global namespace
	global file_list

	while arg_i < len(sys.argv):
		if sys.argv[arg_i] not in valid_commands:
			PrintHelpAndExit()
		if sys.argv[arg_i] == "--from-file":
			try:
				file_list.append(sys.argv[arg_i+1])
			except:
				ErrorAndExit("Invalid secrets filename specified.")
		if sys.argv[arg_i] == "--name":
			try:
				secret_name = sys.argv[arg_i+1]
			except:
				ErrorAndExit("Invalid secrets name specified.")
		if sys.argv[arg_i] == "--namespace":
			try:
				namespace = sys.argv[arg_i+1]
			except:
				ErrorAndExit("Invalid namespace specified.")
		arg_i += 2

def main():
	if len(sys.argv) < 7:
		print("Invalid usage.")
		PrintHelpAndExit()

	GetArguments()

	if secret_name == "":
		ErrorAndExit("Could not determine secret name!")
	if namespace == "":
		ErrorAndExit("Could not determine namespace!")

	for file in file_list:
		if not os.path.exists(file):
			ErrorAndExit("File " + file + " not found!")
		create_secrets_cmd_a.append("--from-file")
		create_secrets_cmd_a.append(file)

	create_secrets_cmd_a[create_name_idx] = secret_name
	create_secrets_cmd_a[create_ns_idx] = namespace
	seal_secrets_cmd[seal_ns_idx] = namespace
	create_secrets_cmd_a.extend(create_secrets_cmd_b)

	proc_create = Popen(create_secrets_cmd_a, stdout=PIPE)
	proc_seal = Popen(seal_secrets_cmd, stdin=proc_create.stdout, stdout=PIPE)
	proc_create.stdout.close()
	output = proc_seal.communicate()[0]
	proc_seal.stdout.close()

	print("Secret name: " + secret_name)
	print("  Namespace: " + namespace)
	print("###########################")

	for line_encoded in output.splitlines():
		line = line_encoded.decode('ascii')
		for secret in file_list:
			secret_filename = secret.split('/')
			try:
				if line.find(secret_filename[-1]) != -1:
					print(line)
			except:
				pass

if __name__ == "__main__":
	main()