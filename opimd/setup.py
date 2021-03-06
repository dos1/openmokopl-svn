import sys
import os

from ez_setup import use_setuptools
use_setuptools('0.6c3')

from setuptools import setup, find_packages, Extension
from distutils.sysconfig import get_python_inc
from glob import glob
import commands


dist = setup( name='opimd-utils',
    version='0.0.1',
    author='dos',
    author_email='seba.dos1@gmail.com',
    description='Test scripts for freesmartphone.org opimd interface',
    url='http://freesmartphone.org/',
    download_url='svn://openmoko.opendevice.org/trunk/opimd/',
    license='GNU GPL',
    packages=['opimd_utils'],
    scripts=['opimd-cli', 'opimd-notifier', 'opimd-messages', 'opimd-resolve', 'opimd-config'],
    data_files=[('applications', ['data/opimd-messages.desktop']),
    ('pixmaps/opimd-utils', glob("data/icons/*.png")),
    ('../../etc/X11/Xsession.d', ['data/89opimd-notifier'])
  ]
)

installCmd = dist.get_command_obj(command="install_data")
installdir = installCmd.install_dir
installroot = installCmd.root

if not installroot:
    installroot = ""

if installdir:
    installdir = os.path.join(os.path.sep,
        installdir.replace(installroot, ""))

