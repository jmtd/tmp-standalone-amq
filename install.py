"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See the LICENSE file for details.
"""

from cct.module.jboss import JBossInstall

class Install(JBossInstall):

    def install(self):
        self._unpack_distribution()
        self._apply_patches(["jbeap4410.zip"])
        self._change_owner()

