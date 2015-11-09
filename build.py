import os

from pybuilder.core import init, task, use_plugin
from pybuilder.vcs import VCSRevision


use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "gaius"
summary = 'AWS lambda function for deployment automation'
description = """
    AWS lambda function for deployment automation, which makes use of
    sns/sqs for trigger and backchannel."""
license = 'Apache License 2.0'
url = 'https://github.com/ImmobilienScout24/crassus'
version = VCSRevision().get_git_revision_count()
default_task = "publish"


@init
def set_properties(project):
    project.depends_on("boto3")
    project.depends_on("docopt")
    project.build_depends_on("unittest2")
    project.build_depends_on("mock")
    project.build_depends_on("moto")
    project.build_depends_on("mockito-without-hardcoded-distribute-version")
    project.set_property('coverage_break_build', False)

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration'
    ])
