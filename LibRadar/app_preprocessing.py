# -*- coding: utf-8 -*-
"""
    APK file Pretreatment
    ~~~~~~~~~~

    A simple pre-processing tool for APK.

    :copyright: (c) 2016 by Zachary Ma
    :for App Analysis Platform & LibRadar
"""

import os
import platform
import hashlib
import logging
import zipfile


class AppTreat:
    """
    App Pre-processing
    """
    def __init__(self, source_app, target_dir):
        """
        Init App Treat
        :param source_app: apk file path
        :param target_dir: unzip the apk into the folder
        """
        self.source_app = source_app
        self.target_dir = target_dir
        self.valid = self._validate()
        if self.valid < 0:
            return
        self.md5 = ""
        self.meta_inf = ""
        self.decoded_manifest = ""
        self.processing()

    def _validate(self):
        """
        Validate the source path and the target path.
        :return: status
        """
        if not os.path.exists(self.source_app):
            logging.error("%s do not exist." % self.source_app)
            return -1
        if not os.path.isfile(self.source_app):
            logging.error("%s is not a file" % self.source_app)
            return -2
        if len(self.source_app) < 5 or self.source_app[-4:] != ".apk":
            logging.warning("Something wrong with the filename %s." % self.source_app)
            return -3
        if not os.path.exists(self.target_dir):
            logging.debug("Create dir %s" % self.target_dir)
            os.mkdir(self.target_dir)
        return 0

    def get_md5(self):
        if not os.path.isfile(self.source_app):
            logging.critical("file path %s is not a file" % self.source_app)
            raise AssertionError
        file_md5 = hashlib.md5()
        f = file(self.source_app, 'rb')
        while True:
            block = f.read(4096)
            if not block:
                break
            file_md5.update(block)
        f.close()
        file_md5_value = file_md5.hexdigest()
        logging.debug("APK %s's MD5 is %s" % (self.source_app, file_md5_value))
        self.md5 = file_md5_value
        return file_md5_value

    def unzip(self):
        with zipfile.ZipFile(self.source_app, mode='r') as zf:
            for member in zf.infolist():
                words = member.filename.split('/')
                path = self.target_dir
                for word in words[:-1]:
                    while True:
                        drive, word = os.path.splitdrive(word)
                        head, word = os.path.split(word)
                        if not drive:
                            break
                    if word in (os.curdir, os.pardir, ''):
                        continue
                    path = os.path.join(path, word)
                zf.extract(member, path)

    def get_meta_inf(self):
        target_cert_file = "%s/META-INF/META-INF/CERT.RSA" % self.target_dir
        if not os.path.isfile(target_cert_file):
            target_cert_file = "%s/META-INF/META-INF/CERT.DSA" % self.target_dir
            if not os.path.isfile(target_cert_file):
                logging.warning("Something wrong with meta-inf.")
        # Use keytool
        if platform.system() == "Windows":
            cmd_keytool = r"tool\keytool.exe -printcert -file %s" % target_cert_file
        else:
            cmd_keytool = "keytool -printcert -file %s" % target_cert_file
        cmd_output = os.popen(cmd_keytool)
        for line in cmd_output.readlines():
            self.meta_inf += line

    def decode_manifest(self):
        target_manifest_file = "%s/AndroidManifest.xml" % self.target_dir
        if not os.path.isfile(target_manifest_file):
            logging.warning("Something wrong with AndroidManifest.xml")
        # Use AXMLPrinter2.jar
        if platform.system() == "Windows":
            cmd_axmlprinter2 = r"java -jar tool\AXMLPrinter2.jar %s" % target_manifest_file
        else:
            cmd_axmlprinter2 = "java -jar tool/AXMLPrinter2.jar %s" % target_manifest_file
        cmd_output = os.popen(cmd_axmlprinter2)
        for line in cmd_output.readlines():
            self.decoded_manifest += line

    def processing(self):
        # Check the source app and the target path.
        if self.valid < 0:
            logging.error("Not a valid situation.")
            raise AssertionError
        # get md5
        self.get_md5()
        # Unzip source into target directory
        self.unzip()
        # Get META-INF
        self.get_meta_inf()
        # Decode AndroidManifest.xml
        self.decode_manifest()

if __name__ == "__main__":
    # Usage
    app_treat = AppTreat("/Users/marchon/Downloads/aappkk/air.br.com.bitlabs.SWFPlayer.apk", "Data/IntermediateData/air")
    if app_treat.valid == 0:
        print("---------------------------------\nMD5:")
        print(app_treat.md5)
        print("---------------------------------\nMETA-INF:")
        print(app_treat.meta_inf)
        print("---------------------------------\nMANIFEST:")
        print(app_treat.decoded_manifest)
    elif app_treat.valid < 0:
        print("Not Valid")
    else:
        print("Not possible")
        raise AssertionError
