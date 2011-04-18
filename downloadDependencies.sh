#!/bin/bash
## Webpy
#wget -nv http://webpy.org/static/web.py-0.34.tar.gz
#tar xf web.py-0.34.tar.gz
#mv web.py-0.34/web .
#rm -rf web.py-0.34
#rm -rf web.py-0.34.tar.gz
## Flup (library for server hosting thingies)
#wget -nv http://www.saddi.com/software/flup/dist/flup-1.0.2.tar.gz
#tar xf flup-1.0.2.tar.gz
#mv flup-1.0.2/flup .
#rm -rf flup-1.0.2
#rm -rf flup-1.0.2.tar.gz

# Google App Engine SDK
wget -nv http://googleappengine.googlecode.com/files/google_appengine_1.4.3.zip
unzip -q google_appengine_1.4.3.zip
mv google_appengine .
rm google_appengine_1.4.3.zip
