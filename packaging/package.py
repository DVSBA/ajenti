#!/usr/bin/env python

import os
import sys
import subprocess

def deps(x, p):
    for y in x:
        if 'any' in y[0] or p in y[0]:
            return y[1]
    return []
    
def shell(c):
    subprocess.Popen('LC_ALL=C '+c, shell=True).wait()
    
def name(name):
    return name.replace('_', '-')    
    
def version(ver):
    return ver.split(':')[-1]
    
    
def package_deb(id):
    ddeps = ['ajenti']
    shell('mkdir tmp/DEBIAN')
    
    control = 'Section: admin\nPriority: optional\nMaintainer: Eugeny Pankov <e@ajenti.org>\nVersion: %s\nPackage: ajenti-plugin-%s\nArchitecture: all\nHomepage: http://ajenti.org/\nDepends: %s\nDescription: %s plugin for Ajenti\n'%(version(VERSION),name(id),','.join(ddeps),NAME)
    open('tmp/DEBIAN/control', 'w').write(control)

    
    shell('mkdir -p tmp/var/lib/ajenti/plugins')
    shell('cp -r ../plugins/%s tmp/var/lib/ajenti/plugins/'%id)
    
    shell('dpkg-deb -b tmp .')
    shell('mv *.deb out')    
    
    
    
    
    
formats = {
    'debian': 'deb'
}

    
platform = sys.argv[1]    
shell('mkdir out')    
    
print ':: Packaging plugins for ' + platform
    
for s in sorted(os.listdir('../plugins')):
    print '  - '+s
    shell('mkdir tmp')
    meta = open('../plugins/%s/__init__.py'%s).read()
    exec(meta)
    DEPS = deps(DEPS, platform)
    eval('package_%s'%formats[platform])(s)
    shell('rm -r tmp')
    break
    #shell('cp ../plugins/%s/files/icon.png meta/plugins/%s'%(s,s))
#    shell('cd ../plugins; tar -cz %s > plugin.tar.gz'%s)
#    shell('mv ../plugins/plugin.tar.gz meta/plugins/%s'%s)    
