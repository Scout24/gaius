import os
import sys

from pybuilder.core import init, use_plugin
from pybuilder.vcs import VCSRevision


use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('python.cram')
use_plugin('copy_resources')


name = "gaius"
summary = 'The deployment client that triggers Crassus to deploy artefacts'
description = """
Deployment client which pushs an AWS SNS message with CloudFormation-Stack
parameters as Payload to trigger
Crassus <https://github.com/ImmobilienScout24/crassus> as deployment Lambda
function"""
license = 'Apache License 2.0'
url = 'https://github.com/ImmobilienScout24/gaius'
version = VCSRevision().get_git_revision_count()
default_task = "publish"


@init
def set_properties(project):
    project.depends_on("boto3")
    project.depends_on("docopt")
    if sys.version_info[0:2] < (2, 7):
        project.depends_on("ordereddict")
    project.build_depends_on("unittest2")
    project.build_depends_on("mock")
    project.build_depends_on("moto")
    project.build_depends_on("mockito-without-hardcoded-distribute-version")
    project.set_property("coverage_threshold_warn", 70)
    project.set_property("coverage_branch_threshold_warn", 80)
    project.set_property("coverage_branch_partial_threshold_warn", 80)
    project.set_property('coverage_break_build', True)

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').extend(['setup.cfg'])
    project.get_property('copy_resources_glob').append('post-install.sh')

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration'
    ])

    project.set_property(
        'distutils_console_scripts', ['gaius=gaius.cli:send_message'])
    project.version = '%s-%s' % (project.version,
                                 os.environ.get('BUILD_NUMBER', 0))
