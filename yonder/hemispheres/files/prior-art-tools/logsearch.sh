#!/bin/bash
# usage: logsearch.sh "QUERY TEXT"   -- records one web search in the log (the search itself is made with the search tool)
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | SEARCH | $1" >> /home/agent3/prior/hemi/fetch-log.txt
