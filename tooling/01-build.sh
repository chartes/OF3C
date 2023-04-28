rm -r output-*
env/bin/protogenie build config-lemma-pos.xml --output output-lemma-pos -t .98 -d .02 -e 0 --verbose
env/bin/protogenie concat config-lemma-pos.xml output-lemma-pos
env/bin/protogenie build config-morph.xml --output output-morph -t .98 -d .02 -e 0 --verbose
env/bin/protogenie concat config-morph.xml output-morph