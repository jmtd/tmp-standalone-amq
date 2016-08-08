"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See the LICENSE file for details.
"""

from zipfile import ZipFile
import os
import subprocess
import tempfile
import shutil

from cct import Module
from cct.lib.file_utils import chown, chmod

class AMQInstall(Module):
    """
    This is a base module that can be extended to install AMQ

    Required env vars:
        - AMQ_HOME - location where the distribution should be installed
        - DISTRIBUTION_VERSION
        - ACTIVEMQ_VERSION

    Required source keys:
        - distribution.zip - this is the binary distribution
    """

    def setup(self):
        self.amq_home = os.getenv("AMQ_HOME")

        if not self.amq_home:
            raise Exception("AMQ_HOME environment variable is not set, I don't know where to install the application server")

        self.sources_path = "/tmp/scripts/sources/"

    def teardown(self):
        # Do not execute teardown method from base class
        # XXX: clean up old ZIP?
        pass

    def _unpack_distribution(self):
        """
        Extracts content of the distribution archive to AMQ_HOME

        We need to open distribution.zip and get a handle on
        "${DISTRIBUTION_VERSION}/extras/${ACTIVEMQ_VERSION}-bin.zip"

        Then open that and extract the result to AMQ_HOME
        """

        distribution_zip_path = os.path.join(self.sources_path, self.artifacts['distribution.zip'].name)

        self.logger.info("Unpacking AMQ distribution...")

        outerzip = zipfile.ZipFile(distribution_zip_path, "r")
        zipname = os.path.join(os.getenv("DISTRIBUTION_VERSION"), "extras", os.getenv("ACTIVEMQ_VERSION") + "-bin.zip")
        innerfd  = outerzip.open(zipname, "r")
        innerzip = zipfile.ZipFile(innerfd, "r")

        tmp_dir = tempfile.mkdtemp()
        innerzip.extractall(tmp_dir)

        # Move the distribution to the correct location
        shutil.move(os.path.join(tmp_dir, os.getenv("ACTIVEMQ_VERSION")), self.amq_home)

        self.logger.debug("Unpacked!")

    def _change_owner(self):
        """ Makes sure the content is owned by appropriate user """

        self.logger.info("Changing distribution owner to 'jboss'...")

        chown(self.amq_home, user="jboss", group="jboss", recursive=True)
        chmod(self.amq_home, 0o755)

        self.logger.info("Owner changed")

class Install(AMQInstall):

    def install(self):
        self._unpack_distribution()
        self._change_owner()

