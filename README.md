# sealegs

A Python 3 script to automate the creation of sealed Kubernetes secrets using `kubeseal`.

## Instructions

1. Clone the project repository: `git clone https://github.com/cms-codes/sealegs.git`

2. Verify the shebang path matches your Python 3 interpreter.

3. Run the script with the following parameters: `sealegs.py --name [SECRET NAME] --namespace [NAMESPACE] --from-file [SECRETS1] --from-file [SECRETS2] --from-file [...]`.
Note that at minimum the secret name, namespace and one plaintext secrets file must be specified.

4. The sealed secrets for each file will be printed to stdout.
