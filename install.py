from zipfile import ZipFile

class Install(Module):

    def install(self):
        eap_zip_path = os.path.join("/tmp/script/sources/", self.artifacts['eap.zip'])
        zip = ZipFile(eap_zip_path)
        zip.extractall(os.getenv("JBOSS_HOME"))
        #FIXME permissions
