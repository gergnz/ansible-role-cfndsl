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
