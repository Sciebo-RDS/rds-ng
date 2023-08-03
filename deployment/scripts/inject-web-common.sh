#!/usr/bin/env bash
cd $1

echo "Injecting 'web-common' into the web container..."

# Add the 'web-common' dependency
sed -i 's/"dependencies": {/"dependencies": {\n\        "web-common": "latest",/g' package.json

# Modify the 'common' module path to match the container layout
sed -i 's/..\/common\/web/web-common/g' tsconfig.app.json vite.config.ts
