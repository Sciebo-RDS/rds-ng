#!/usr/bin/env bash

# generate python markdown files
cd ./docs
rm -rf ./docs/reference
#for gh-action to run properly
pip install pydoc-markdown
pydoc-markdown

# generate & install workspace package.json
cd ../src
echo "{ \"private\": true, \"workspaces\": [\"common\", \"frontend\"] }" > package.json
npm install
cd ../docs

# build docusaurus, incl. generating TS docs
npm install
npx docusaurus build
rm -rf ./docs/frontend/index.md ./docs/frontend/modules.md