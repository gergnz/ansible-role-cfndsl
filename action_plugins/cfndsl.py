# MIT License
# 
# Copyright (c) 2017 Greg Cockburn
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: cfndsl
short_description: Compiles CFNDSL to Cloudformation
description:
     - Compiles CFNDSL to CLoudformation
version_added: "2.2"
options:
  src:
    description:
      - The ruby template to be compiled.
    required: true
  dest:
    description:
      - The destination output of the compiled Cloudformation in JSON or YAML.
    required: true
  yaml:
    description:
      - A list of or single YAML file to use as external parameters.
    required: false
    default: null
  ruby:
    description:
      - A list of or single RUBY file to use as external parameters.
    required: false
    default: null
  json:
    description:
      - A list of or single JSON file to use as external parameters.
    required: false
    default: null
  pretty:
    description:
      - Output pretty JSON.
    required: false
    default: False
  outformat:
    description:
      - Change the output format to be YAML instead of JSON.
    required: false
    default: JSON
  defines:
    description:
      - A list of defines to pass to CFNDSL.
    required: false
    default: null
  disable_binding:
    description:
      - Enable or Disable bindings. (Safe not to)
    required: false
    default: True
author: "Greg Cockburn (@gergnz)"
'''
EXAMPLES = '''
# Create a SQS Queue Cloudformation
- name: build a sqs
  cfndsl:
    dest: /tmp/sqs.json
    src: cfndsl/sqs.rb
# Create a SQS Queue Cloudformation using external parameters in YAML format
- name: build sqs with external parameters
  cfndsl:
    dest: /tmp/sqs.json
    src: cfndsl/sqs.rb
    yaml:
      - external_parameters/sqs.yml
# Create a SQS Queue Cloudformation using defines
- name: build sqs with defines
  cfndsl:
    dest: /tmp/sqs.json
    src: cfndsl/sqs.rb
    defines:
      quename: myqueue
'''
from pprint import pprint
from subprocess import Popen, PIPE
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native, to_text
from ansible.utils.boolean import boolean
from ansible.utils.hashing import checksum_s
from ansible.parsing.yaml.objects import AnsibleUnicode

class ActionModule(ActionBase):
    ''' Process cfndsl files '''

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if self._play_context.check_mode:
            result['skipped'] = True
            result['msg'] = "skipped, this module does not support check_mode."
            return result

        src             = self._task.args.get('src', None)
        dest            = self._task.args.get('dest', None)
        yaml            = self._task.args.get('yaml', None)
        ruby            = self._task.args.get('ruby', None)
        json            = self._task.args.get('json', None)
        pretty          = self._task.args.get('pretty', False)
        outformat       = self._task.args.get('format', 'JSON')
        defines         = self._task.args.get('defines', None)
        disable_binding = self._task.args.get('disable_binding', True)

        if dest is None or src is None:
            result['failed'] = True
            result['msg'] = "src and dest are required"
            return result

        cmd = []
        cmd.append("cfndsl")

        if pretty is True:
            cmd.append(" -p")

        if disable_binding is True:
            cmd.append("-b")

        if outformat.upper() == 'JSON':
            cmd.append("-f")
            cmd.append("json")
        elif outformat.upper() == 'YAML':
            cmd.append("-f")
            cmd.append("yaml")
        else:
            result['failed'] = True
            result['msg'] = "unsupported output format"
            return result

        if dest is not None:
            cmd.append("-o")
            cmd.append(dest)
        else:
            result['failed'] = True
            result['msg'] = "dest must be supplied"
            return result

        if src is None:
            result['failed'] = True
            result['msg'] = "src must be supplied"
            return result

        if defines is not None:
            if type(defines) is dict:
                for key,value in defines.iteritems():
                    cmd.append("-D")
                    cmd.append(str(key)+"="+str(value))
            else:
                result['failed'] = True
                result['msg'] = "defines must be a dict"
                return result

        if yaml is not None:
            if type(yaml) is AnsibleUnicode:
                cmd.append("-y")
                cmd.append(str(yaml))
            elif type(yaml) is list:
                for y in yaml:
                    cmd.append("-y")
                    cmd.append(y)
            else:
                result['failed'] = True
                result['msg'] = "yaml variables can only be a list or string"
                return result

        if ruby is not None:
            if type(ruby) is str:
                cmd.append("-r")
                cmd.append(str(ruby))
            elif type(ruby) is list:
                for r in ruby:
                    cmd.append("-r")
                    cmd.append(r)
            else:
                result['failed'] = True
                result['msg'] = "ruby variables can only be a list or string"
                return result

        if json is not None:
            if type(json) is str:
                cmd.append("-j")
                cmd.append(str(json))
            elif type(json) is list:
                for j in json:
                    cmd.append("-j")
                    cmd.append(j)
            else:
                result['failed'] = True
                result['msg'] = "json variables can only be a list or string"
                return result

        cmd.append(src)
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        proc.wait()
        if proc.returncode is not 0:
            result['failed'] = True
            result['msg'] = proc.stdout.read()+"  "+proc.stderr.read()
            return result

        result['changed'] = True
        result['failed'] = False
        return result
