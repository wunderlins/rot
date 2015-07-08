#!/usr/bin/env bash

cd static
for f in *.zip; do unzip -o "$f"; done		
for f in *.tar.gz; do tar xzf "$f"; done
mv dist bootstrap
cd ../lib
for f in *.tar.gz *.tgz; do tar xzf "$f"; done
cd ..

