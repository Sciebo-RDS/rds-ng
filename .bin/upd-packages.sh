#!/bin/sh

cd ../src/common/web || exit
ncu -utminor
npm i

cd ../../frontend || exit
ncu -utminor
npm i

