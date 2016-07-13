from zipfile import ZipFile
from cct.module import Module
from cct.lib.file_utils import chown, chmod
import os

class Install(Module):

    def install(self):
        return
        eap_zip_path = os.path.join("/tmp/script/sources/",
                                    self.artifacts['eap.zip'].name)
        zip = ZipFile(eap_zip_path)
        zip.extractall(os.getenv("JBOSS_HOME"))

        chown(os.getenv("JBOSS_HOME"), user="jboss", group="jboss", rec=True)
        chmod(os.getenv("JBOSS_HOME"), 0o755)
