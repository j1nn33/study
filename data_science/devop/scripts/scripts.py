#!/usr/bin/env python
import subprocess
subprocess.run(["ls", "-l"])

python_df = subprocess.run(["df", "-h"])
