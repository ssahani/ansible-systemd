#!/usr/bin/python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-2.1+
# (c) 2018, Susant Sahani <ssahani@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: systemd-journald
short_description: Automates systemd-journald conf files.
description:
    - Allows you to generate systemd-journald configuration files.
version_added: "2.8"
options:
    conf_path:
        description:
            - Specifies the path where to write the configuration files.
        default: "/etc/systemd/systemd-journald.conf"
        choices: [ "/etc/systemd/systemd-journald.conf", "/etc/systemd/systemd-journald.conf.d",
                   "/usr/lib/systemd/systemd-journald.conf.d", "/run/systemd/systemd-journald.conf.d" ]
    file_name:
        description:
            - This configuration file name where the configurations will be written. Note that file name will be
              automatically have the extension .conf. When path is /etc/systemd/systemd-journald.conf then the file_name
              will be ignored.
    storage:
        description:
            - Specifies where to store journal data.
        choices: [ "volatile", "persistent", "auto", "none" ]
    compress:
        description:
            - Whether to comppress the data.
        choices: [ "yes", "no" ]
    ratelimit_interval:
        description:
            - Configures the rate limiting that is applied to all messages generated on the system.
              May be specified in following units "s", "min", "h", "ms", "us".
    ratelimit_burst:
        description:
            - Configures how many messages allowed in ratelimit_interval.
    forward_to_syslog:
        description:
            - Configures whether log messages received by the journal daemon shall be forwarded to a syslog daemon.
        choices: [ "yes", "no" ]
    forward_to_kmsg:
        description:
            - Configures whether forwarded the kernel log buffer (kmsg).
        choices: [ "yes", "no" ]
    forward_to_console:
        description:
            - Configures whether forwarded console.
        choices: [ "yes", "no" ]
    forward_to_wall:
        description:
            - Configures whether forwarded as the wall messages to all logged-in users.
        choices: [ "yes", "no" ]
    action:
        description:
            - Create or removes the configration file.
        choices: [ create, remove ]
        default: create

author: "Susant Sahani (@ssahani) <susant@redhat.com>"
'''

EXAMPLES = '''
# Create config file
- systemd-journald:
     conf_path: /run/systemd/systemd-journald.conf.d
     file_name: test
     storage: auto
     forward_to_syslog: yes
     action: create

# Remove config file
- systemd-journald:
     conf_path: /run/systemd/systemd-journald.conf.d
     file_name: test
     action: remove
'''

RETURN = r'''
'''

import os
from ansible.module_utils.basic import get_platform, AnsibleModule

UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM_CONF = '/etc/systemd/systemd-journald.conf'
UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM = '/etc/systemd/systemd-journald.conf.d'
UNIT_PATH_SYSTEMD-JOURNALD = '/usr/lib/systemd/systemd-journald.conf.d'
UNIT_PATH_SYSTEMD-JOURNALD_RUN = '/run/systemd/systemd-journald.conf.d'


class systemd-journald(object):

    def __init__(self, module):
        self.module = module
        self.args = self.module.params
        self.conf_path = module.params['conf_path']
        self.file_name = module.params['file_name']
        self.storage = module.params['storage']
        self.compress = module.params['compress']
        self.ratelimit_interval = module.params['ratelimit_interval']
        self.ratelimit_burst = module.params['ratelimit_burst']
        self.forward_to_syslog = module.params['forward_to_syslog']
        self.forward_to_kmsg = module.params['forward_to_kmsg']
        self.forward_to_console = module.params['forward_to_console']
        self.forward_to_wall = module.params['forward_to_wall']
        self.action = module.params['action']
        self.changed = False

    def remove_files(self):
        paths = [UNIT_PATH_SYSTEMD-JOURNALD_RUN, UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM, UNIT_PATH_SYSTEMD-JOURNALD]
        rc = False

        list_conf_files = self.file_name.split(' ')
        for conf_file in list_conf_files:
            conf_file += '.conf'
            if os.path.exists(os.path.join(self.conf_path, conf_file)):
                os.remove(os.path.join(self.conf_path, conf_file))
                rc = True

        return rc

    def write_configs_to_file(self, conf):
        if not os.path.exists(self.conf_path):
            os.makedirs(self.conf_path, exist_ok=True)

        if self.conf_path != UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM_CONF:
            self.file_name += '.conf'
            path = os.path.join(self.conf_path, self.file_name)
        else:
            path = UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM_CONF

        with open(path, "w") as f:
                f.write(conf + '\n')
                f.close()
                return True

        return False

    def create_jounald_conf(self):
        conf = '[Journal]\n'

        if self.storage:
            conf += 'Storage={0}\n'.format(self.storage)
        if self.compress:
            conf += 'Compress={0}\n'.format(self.compress)
        if self.ratelimit_interval:
            conf += 'RateLimitIntervalSec={0}\n'.format(self.ratelimit_interval)
        if self.ratelimit_burst:
            conf += 'RateLimitBurst={0}\n'.format(self.ratelimit_burst)
        if self.forward_to_syslog:
            conf += 'ForwardToSyslog={0}\n'.format(self.forward_to_syslog)
        if self.forward_to_kmsg:
            conf += 'ForwardToKMsg={0}\n'.format(self.forward_to_kmsg)
        if self.forward_to_console:
            conf += 'ForwardToConsole={0}\n'.format(self.forward_to_console)
        if self.forward_to_wall:
            conf += 'ForwardToWall={0}\n'.format(self.forward_to_wall)

        return conf

    def configure_systemd-journald(self):
        rc = False

        if self.action == 'create':
            conf = self.create_jounald_conf()
            rc = self.write_configs_to_file(conf)
        elif self.action == 'remove':
            rc = self.remove_files()

        return rc


def main():
    module = AnsibleModule(
        argument_spec=dict(
            conf_path=dict(default=UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM_CONF, type='str',
                           choices=[UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM_CONF, UNIT_PATH_SYSTEMD-JOURNALD, UNIT_PATH_SYSTEMD-JOURNALD_RUN,
                                    UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM]),
            file_name=dict(default=None, type='str'),
            storage=dict(default=None, type='str', choices=['volatile', 'persistent', 'auto', 'none']),
            compress=dict(required=False, default=None, type='str', choices=['yes', 'no']),
            ratelimit_interval=dict(required=False, default=None, type='str'),
            ratelimit_burst=dict(required=False, default=None, type='str'),
            forward_to_syslog=dict(required=False, default=None, type='str', choices=['yes', 'no']),
            forward_to_kmsg=dict(required=False, default=None, type='str', choices=['yes', 'no']),
            forward_to_console=dict(required=False, default=None, type='str', choices=['yes', 'no']),
            forward_to_wall=dict(required=False, default=None, type='str', choices=['yes', 'no']),
            action=dict(choices=['create', 'remove'], default='create'),
        ),
        supports_check_mode=True
    )

    conf_path = module.params['conf_path']
    file_name = module.params['file_name']

    if conf_path != UNIT_PATH_SYSTEMD-JOURNALD_SYSTEM_CONF and file_name is None:
        module.fail_json(msg='file_name cannot be None')

    journal = systemd-journald(module)
    result = journal.configure_systemd-journald()

    module.exit_json(changed=result)


if __name__ == '__main__':
    main()
