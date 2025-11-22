#!/usr/bin/env python3
import sys, shutil, time, os
if len(sys.argv) < 3:
    print('usage: script input output', file=sys.stderr); sys.exit(2)
inp = sys.argv[1]; out = sys.argv[2]
time.sleep(1)
try:
    if os.path.exists(inp) and os.path.isfile(inp):
        shutil.copy(inp, out)
    else:
        with open(out, 'wb') as f:
            f.write(b'DEMO\n')
    print('OK')
    sys.exit(0)
except Exception as e:
    print('ERR:'+str(e), file=sys.stderr); sys.exit(1)
