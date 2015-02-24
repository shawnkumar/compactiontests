# compactiontests

requires:
- cstar perf setup on 1-node cluster

to run:
- move scripts to user directory (one level up from fab folder)
- run test_script.py

outputs:
- performance stats - stats.lcs/stcs.json
- all lines concering compaction in system log
- pending tasks from compactions stats
