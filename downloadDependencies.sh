#!/bin/bash
wget http://webpy.org/static/web.py-0.34.tar.gz
wget http://www.saddi.com/software/flup/dist/flup-1.0.2.tar.gz
tar xf web.py-0.34.tar.gz
mv web.py-0.34/web .
rm -rf web.py-0.34
rm -rf web.py-0.34.tar.gz
tar xf flup-1.0.2.tar.gz
mv flup-1.0.2/flup .
rm -rf flup-1.0.2
rm -rf flup-1.0.2.tar.gz
