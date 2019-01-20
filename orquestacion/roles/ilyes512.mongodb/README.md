MongoDB (Ansidev)
=========
[![Build Status](https://travis-ci.org/Ilyes512/ansible-role-mongodb.svg)](https://travis-ci.org/Ilyes512/ansible-role-mongodb)

This role installs MongoDB for Ubuntu Trusty (14.04) and Xenial (16.04).

Requirements
------------

No requirements.

Role Variables
--------------

```
ansidev_package_state: present

mongodb_package_state: "{{ ansidev_package_state }}"
mongodb_version: "latest" # latest | version without v-prefix
mongodb_allow_downgrade: no # yes | no
mongodb_allow_remote: yes
```

Dependencies
------------

No dependencies.

Example Playbook
----------------
```
- hosts: servers
  roles:
    - { role: ilyes512.mongodb, tag: ansidev.mongodb }
```

Todo
----------------

- Add option to disable the [Transparent Huge Pages](https://docs.mongodb.com/master/tutorial/transparent-huge-pages/)

License
-------

MIT

Author Information
------------------

Ilyes Ahidar [@Ilyes512](https://twitter.com/ilyes512)
