#!/bin/bash

python -m wikiextractor.WikiExtractor \
       ~/keywords-t5/knowledge_source_parsing/data/plwiki-20221120-pages-articles.xml \
       --output "/home/juanpablo/wikipedia_data" \
       --no-templates \
       --json \
       --anchors \
       --sections
