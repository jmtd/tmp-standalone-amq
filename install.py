from zipfile import ZipFile
from cct.module import Module
from cct.lib.file_utils import chown, chmod
import os

class Install(Module):

    def install(self):
        eap_zip_path = os.path.join("/tmp/scripts/sources/",
                                    self.artifacts['eap.zip'].name)
        zip = ZipFile(eap_zip_path)
        zip.extractall(os.getenv("JBOSS_HOME"))

        chown(os.getenv("JBOSS_HOME"), user="jboss", group="jboss", recursive=True)
        chmod(os.getenv("JBOSS_HOME"), 0o755)
