#!/usr/bin/env bash
cd $1

echo "Updating module paths..."

# Modify the 'web-common' module path to match the container layout
sed -i 's/..\/common\/web/web-common/g' tsconfig.app.json vite.config.ts
