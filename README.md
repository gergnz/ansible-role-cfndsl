[![Build Status](https://travis-ci.org/gergnz/ansible-role-cfndsl.png?branch=master)](https://travis-ci.org/gergnz/ansible-role-cfndsl)

CFNDSL
=========

A module that compiles CFNDSL down to cloudformation.

Requirements
------------

A working install and some knowledge of [CFNDSL](https://github.com/stevenjack/cfndsl)

Example Playbook
----------------

```
---
  - hosts: localhost
    connection: local
    roles:
      - gergnz.cfndsl
    tasks:
      - name: testing
        cfndsl:
          dest: /tmp/sqs.json
          src: cfndsl/sqs.rb
          yaml:
            - external_parameters/sqs.yml
```

License
-------

MIT
