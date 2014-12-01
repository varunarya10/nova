#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

import mock
from oslo.serialization import jsonutils

from nova import exception
from nova import objects
from nova.tests.unit.objects import test_objects

fake_instance_uuid = str(uuid.uuid4())

fake_obj_numa_topology = objects.InstanceNUMATopology(
    instance_uuid = fake_instance_uuid,
    cells=[
        objects.InstanceNUMACell(
            id=0, cpuset=set([1, 2]), memory=512, pagesize=2048),
        objects.InstanceNUMACell(
            id=1, cpuset=set([3, 4]), memory=512, pagesize=2048)
    ])

fake_numa_topology = fake_obj_numa_topology._to_dict()

fake_db_topology = {
    'created_at': None,
    'updated_at': None,
    'deleted_at': None,
    'deleted': 0,
    'id': 1,
    'instance_uuid': fake_instance_uuid,
    'numa_topology': fake_obj_numa_topology._to_json()
    }

fake_old_db_topology = dict(fake_db_topology)  # copy
fake_old_db_topology['numa_topology'] = jsonutils.dumps(fake_numa_topology)


class _TestInstanceNUMATopology(object):
    @mock.patch('nova.db.instance_extra_update_by_uuid')
    def test_create(self, mock_update):
        topo_obj = fake_obj_numa_topology
        topo_obj.instance_uuid = fake_db_topology['instance_uuid']
        topo_obj.create(self.context)
        self.assertEqual(1, len(mock_update.call_args_list))

    @mock.patch('nova.db.instance_extra_update_by_uuid')
    def test_save(self, mock_update):
        topo_obj = fake_obj_numa_topology
        topo_obj.instance_uuid = fake_db_topology['instance_uuid']
        topo_obj._save(self.context)
        self.assertEqual(1, len(mock_update.call_args_list))

    def _test_get_by_instance_uuid(self):
        numa_topology = objects.InstanceNUMATopology.get_by_instance_uuid(
            self.context, fake_db_topology['instance_uuid'])
        self.assertEqual(fake_db_topology['instance_uuid'],
                         numa_topology.instance_uuid)
        for obj_cell, topo_cell in zip(
                numa_topology.cells, fake_obj_numa_topology['cells']):
            self.assertIsInstance(obj_cell, objects.InstanceNUMACell)
            self.assertEqual(topo_cell.id, obj_cell.id)
            self.assertEqual(topo_cell.cpuset, obj_cell.cpuset)
            self.assertEqual(topo_cell.memory, obj_cell.memory)
            self.assertEqual(topo_cell.pagesize, obj_cell.pagesize)

    @mock.patch('nova.db.instance_extra_get_by_instance_uuid')
    def test_get_by_instance_uuid(self, mock_get):
        mock_get.return_value = fake_db_topology
        self._test_get_by_instance_uuid()

    @mock.patch('nova.db.instance_extra_get_by_instance_uuid')
    def test_get_by_instance_uuid_old(self, mock_get):
        mock_get.return_value = fake_old_db_topology
        self._test_get_by_instance_uuid()

    @mock.patch('nova.db.instance_extra_get_by_instance_uuid')
    def test_get_by_instance_uuid_missing(self, mock_get):
        mock_get.return_value = None
        self.assertRaises(
            exception.NumaTopologyNotFound,
            objects.InstanceNUMATopology.get_by_instance_uuid,
            self.context, 'fake_uuid')


class TestInstanceNUMATopology(test_objects._LocalTest,
                               _TestInstanceNUMATopology):
    pass


class TestInstanceNUMATopologyRemote(test_objects._RemoteTest,
                                     _TestInstanceNUMATopology):
    pass