'''
Created on Aug 2, 2013

@author: chadcumba

Parallel workflow execution with SLURM
'''
from __future__ import print_function, division, unicode_literals, absolute_import
from builtins import open

import os
import re
from time import sleep

from ...interfaces.base import CommandLine
from .base import (SGELikeBatchManagerBase, logger, iflogger, logging)



class SLURMPlugin(SGELikeBatchManagerBase):
    '''
    Execute using SLURM

    The plugin_args input to run can be used to control the SLURM execution.
    Currently supported options are:

    - template : template to use for batch job submission

    - sbatch_args: arguments to pass prepend to the sbatch call


    '''

    def __init__(self, **kwargs):

        template = "#!/bin/bash"

        self._retry_timeout = 2
        self._max_tries = 2
        self._template = template
        self._sbatch_args = None
        self._jobid_re = "Submitted batch job ([0-9]*)"

        if 'plugin_args' in kwargs and kwargs['plugin_args']:
            if 'retry_timeout' in kwargs['plugin_args']:
                self._retry_timeout = kwargs['plugin_args']['retry_timeout']
            if 'max_tries' in kwargs['plugin_args']:
                self._max_tries = kwargs['plugin_args']['max_tries']
            if 'jobid_re' in kwargs['plugin_args']:
                self._jobid_re = kwargs['plugin_args']['jobid_re']
            if 'template' in kwargs['plugin_args']:
                self._template = kwargs['plugin_args']['template']
                if os.path.isfile(self._template):
                    with open(self._template) as f:
                        self._template = f.read()
            if 'sbatch_args' in kwargs['plugin_args']:
                self._sbatch_args = kwargs['plugin_args']['sbatch_args']
        self._pending = {}
        super(SLURMPlugin, self).__init__(self._template, **kwargs)

    def _is_pending(self, taskid):
        #  subprocess.Popen requires taskid to be a string
        res = CommandLine('squeue',
                          args=' '.join(['-j', '%s' % taskid]),
                          terminal_output='allatonce').run()
        return res.runtime.stdout.find(str(taskid)) > -1

    def _submit_batchtask(self, scriptfile, node):
        """
        This is more or less the _submit_batchtask from sge.py with flipped
        variable names, different command line switches, and different output
        formatting/processing
        """
        cmd = CommandLine('sbatch', environ=dict(os.environ),
                          terminal_output='allatonce')
        path = os.path.dirname(scriptfile)

        sbatch_args = ''
        if self._sbatch_args:
            sbatch_args = self._sbatch_args
        if 'sbatch_args' in node.plugin_args:
            if 'overwrite' in node.plugin_args and\
               node.plugin_args['overwrite']:
                sbatch_args = node.plugin_args['sbatch_args']
            else:
                sbatch_args += (" " + node.plugin_args['sbatch_args'])
        if '-o' not in sbatch_args:
            sbatch_args = '%s -o %s' % (sbatch_args, os.path.join(path, 'slurm-%j.out'))
        if '-e' not in sbatch_args:
            sbatch_args = '%s -e %s' % (sbatch_args, os.path.join(path, 'slurm-%j.out'))
        if node._hierarchy:
            jobname = '.'.join((dict(os.environ)['LOGNAME'],
                                node._hierarchy,
                                node._id))
        else:
            jobname = '.'.join((dict(os.environ)['LOGNAME'],
                                node._id))
        jobnameitems = jobname.split('.')
        jobnameitems.reverse()
        jobname = '.'.join(jobnameitems)
        cmd.inputs.args = '%s -J %s %s' % (sbatch_args,
                                           jobname,
                                           scriptfile)
        oldlevel = iflogger.level
        iflogger.setLevel(logging.getLevelName('CRITICAL'))
        tries = 0
        while True:
            try:
                result = cmd.run()
            except Exception as e:
                if tries < self._max_tries:
                    tries += 1
                    sleep(self._retry_timeout)  # sleep 2 seconds and try again.
                else:
                    iflogger.setLevel(oldlevel)
                    raise RuntimeError('\n'.join((('Could not submit sbatch task'
                                                   ' for node %s') % node._id,
                                                  str(e))))
            else:
                break
        logger.debug('Ran command ({0})'.format(cmd.cmdline))
        iflogger.setLevel(oldlevel)
        # retrieve taskid
        lines = [line for line in result.runtime.stdout.split('\n') if line]
        taskid = int(re.match(self._jobid_re,
                              lines[-1]).groups()[0])
        self._pending[taskid] = node.output_dir()
        logger.debug('submitted sbatch task: %d for node %s' % (taskid, node._id))
        return taskid
