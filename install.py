from cct.module.jboss import JBossInstall

class Install(JBossInstall):

    def install(self):
        self._unpack_distribution()
        self._apply_patches(["jbeap4410.zip"])
        self._change_owner()

