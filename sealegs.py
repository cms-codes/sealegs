#!/usr/bin/python

import sys
import os.path
from subprocess import Popen, PIPE

arg_i = 3
file_list = []
namespace = ""

create_secrets_cmd_a = ["kubectl", "--namespace", "default", "create", 
						"secret", "generic", "sealegs-secrets"]
create_secrets_cmd_b = ["--dry-run=client", "-oyaml"]
create_ns_idx = 2

seal_secrets_cmd = ["kubeseal", "--format", "yaml", "--namespace", "default"]
seal_ns_idx = 4

if len(sys.argv) < 5:
	print("Invalid usage.")
	print(sys.argv[0] + " --namespace [namespace] --from-file [secrets 1] --from-file \
		  [secrets 2] --from-file [...]")
	sys.exit(-1)

if sys.argv[1] == "--namespace":
	try:
		namespace = sys.argv[2]
	except:
		pass

if namespace == "":
	print("Could not determine namespace!")
	sys.exit(-1)

while arg_i < len(sys.argv):
	if sys.argv[arg_i] == "--from-file":
		try:
			file_list.append(sys.argv[arg_i+1])
		except:
			pass
	else:
		break
	arg_i += 2

for file in file_list:
	if not os.path.exists(file):
		print("File " + file + " not found!")
		sys.exit(-1)
	create_secrets_cmd_a.append("--from-file")
	create_secrets_cmd_a.append(file)

create_secrets_cmd_a[create_ns_idx] = namespace
seal_secrets_cmd[seal_ns_idx] = namespace
create_secrets_cmd_a.extend(create_secrets_cmd_b)

proc_create = Popen(create_secrets_cmd_a, stdout=PIPE)
proc_seal = Popen(seal_secrets_cmd, stdin=proc_create.stdout, stdout=PIPE)
proc_create.stdout.close()
output = proc_seal.communicate()[0]
proc_seal.stdout.close()

for line in output.splitlines():
	for secret in file_list:
		secret_name = secret.split("/")
		if line.find(secret_name[-1]) > -1:
			print(line)
