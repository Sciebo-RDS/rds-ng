#!/bin/sh

cd ../src/common/web || exit
ncu -ux vite,@vitejs/plugin-vue,eslint,@vue/eslint-config-typescript
npm i

cd ../../frontend || exit
ncu -ux vite,@vitejs/plugin-vue,eslint,@vue/eslint-config-typescript
npm i

