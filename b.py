import os
import subprocess

outFile = 'output.md'

cmd = 'python setup.py build'

print(f'--------START:: ${cmd}')

buf = ''

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate()
print(f'■■■■ out : {out}')
result = out.split('\n')
for lin in result:
    if not lin.startswith('#'):
        print(lin)
        buf += lin + '\n'

os.system(f'code ${outFile}')

print("-------END")
print(buf)
