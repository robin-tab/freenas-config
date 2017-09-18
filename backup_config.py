#!/usr/local/bin/python
#
import os
import shutil
import datetime
import sys
import logging

#path=usr/local/bin/python
d = datetime.datetime.now()
date_format = "%a-%d-%b-%Y"
log_file = "/tmp/freenas-backup.log"
db_file = "/data/freenas-v1.db"
bk_path = "/mnt/backups/"
backup_name = "freenas_config"
archive_name = "freenas_archive"
ext = ".db"

matched = None
fname = None
backup_len = len(backup_name)

console = logging.StreamHandler()
console.setLevel(logging.INFO)


logging.basicConfig(filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs).03d     %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')
logging.getLogger('').addHandler(console)

if  os.stat(log_file)[6]==0:
        logging.debug('Version 1.0 build 16')
        logging.debug('---------------------------')

os.chdir(bk_path)
logging.debug('Searching for previous backup in ' + bk_path )
for files in os.listdir("."):
        if files.startswith(backup_name):
                fname = files
                bk_file = bk_path + files
                matched = True
                logging.debug('Found file ' + bk_file)
                break
if matched is True:
        read1 = file(db_file).read().split('\n')
        read2 = file(bk_file).read().split('\n')
        if read1 == read2:
                logging.info('Configuration has not changed. Aborting backup')
                sys.exit()
        else:
                logging.debug('Configuration changed. Archiving previous backup')
                logging.debug(bk_file + ' >> ' + bk_path + archive_name + fname[backup_len:])
                shutil.move(bk_file,  bk_path + archive_name + fname[backup_len:])
                logging.info('Creating backup ' + bk_path + backup_name + '_' + d.strftime(date_format) + ext)
                shutil.copy2(db_file, bk_path + backup_name + '_' + d.strftime(date_format) + ext)

else:
        bk_file = bk_path + backup_name + '_' + d.strftime(date_format) + ext
        logging.info('No previous backup found. Create new backup: ' + bk_file)
        shutil.copy2(db_file, bk_file)
sys.exit()
