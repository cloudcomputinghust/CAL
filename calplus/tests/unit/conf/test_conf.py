# Copyright 2016 HPCC-ICSE Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import collections
import mock
from oslo_config import cfg
import six

import calplus.conf
from calplus.conf import opts
from calplus.tests import base


CONF = calplus.conf.CONF


class ConfTestCase(base.TestCase):

    def test_list_opts(self):
        for group, opt_list in opts.list_opts():
            if isinstance(group, six.string_types):
                self.assertEqual(group, 'DEFAULT')
            else:
                self.assertIsInstance(group, cfg.OptGroup)
            for opt in opt_list:
                self.assertIsInstance(opt, cfg.Opt)

    def test_list_module_name_invalid_mods(self):
        with mock.patch('pkgutil.iter_modules') as mock_mods:
            mock_mods.return_value = [(None, 'foo', True),
                                      (None, 'opts', False)]
            self.assertEqual([], opts._list_module_names())

    def test_list_module_name_valid_mods(self):
        with mock.patch('pkgutil.iter_modules') as mock_mods:
            mock_mods.return_value = [(None, 'foo', False)]
            self.assertEqual(['foo'], opts._list_module_names())

    def test_import_mods_no_func(self):
        modules = ['foo', 'bar']
        with mock.patch('importlib.import_module') as mock_import:
            mock_import.return_value = mock.sentinel.mods
            self.assertRaises(AttributeError, opts._import_modules, modules)
            mock_import.assert_called_once_with('calplus.conf.foo')

    def test_import_mods_valid_func(self):
        modules = ['foo', 'bar']
        with mock.patch('importlib.import_module') as mock_import:
            mock_mod = mock.MagicMock()
            mock_import.return_value = mock_mod
            self.assertEqual([mock_mod, mock_mod],
                             opts._import_modules(modules))
            mock_import.assert_has_calls([mock.call('calplus.conf.foo'),
                                          mock.call('calplus.conf.bar')])

    def test_append_config(self):
        opt = collections.defaultdict(list)
        mock_module = mock.MagicMock()
        mock_conf = mock.MagicMock()
        mock_module.list_opts.return_value = mock_conf
        mock_conf.items.return_value = [('foo', 'bar')]
        opts._append_config_options([mock_module], opt)
        self.assertEqual({'foo': ['b', 'a', 'r']}, opt)

    def test_load_config_file_to_realize_all_driver(self):
        CONF(['--config-file',
              'calplus/tests/fake_config_file.conf'])
        # TODO: Maybe we need remove example group,
        # such as: openstack and amazon

        # ensure all driver groups have been registered
        sections = CONF.list_all_sections()
        for section in sections:
            CONF.register_group(cfg.OptGroup(section))

        # ensure all of enable drivers configured exact opts
        enable_drivers = CONF.providers.enable_drivers
        for driver in enable_drivers.keys():
            if enable_drivers.get(driver) == 'openstack':
                CONF.register_opts(
                    calplus.conf.providers.openstack_opts, driver)
            elif enable_drivers.get(driver) == 'amazon':
                CONF.register_opts(
                    calplus.conf.providers.amazon_opts, driver)
            else:
                continue

        self.assertEqual(CONF.openstack1['driver_name'], 'HUST')
        self.assertEqual(CONF.openstack2['driver_name'], 'SOICT')
        self.assertEqual(CONF.amazon['driver_name'], 'Amazon')
