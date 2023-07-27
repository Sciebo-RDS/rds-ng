#!/usr/bin/env bash
cd ./docs
rm -rf ./docs/reference
pydoc-markdown
