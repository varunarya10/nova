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

from nova.db.sqlalchemy import api as db_api
from nova.db.sqlalchemy import api_models
from nova import exception
from nova import objects
from nova.objects import base
from nova.objects import fields


@base.NovaObjectRegistry.register
class InstanceMapping(base.NovaTimestampObject, base.NovaObject):
    # Version 1.0: Initial version
    VERSION = '1.0'

    fields = {
        'id': fields.IntegerField(read_only=True),
        'instance_uuid': fields.UUIDField(),
        'cell_id': fields.IntegerField(),
        'project_id': fields.StringField(),
        }

    @staticmethod
    def _from_db_object(context, instance_mapping, db_instance_mapping):
        for key in instance_mapping.fields:
            setattr(instance_mapping, key, db_instance_mapping[key])
        instance_mapping.obj_reset_changes()
        instance_mapping._context = context
        return instance_mapping

    @staticmethod
    def _get_by_instance_uuid_from_db(context, instance_uuid):
        session = db_api.get_api_session()

        with session.begin():
            db_mapping = session.query(
                    api_models.InstanceMapping).filter_by(
                            instance_uuid=instance_uuid).first()
            if not db_mapping:
                raise exception.InstanceMappingNotFound(uuid=instance_uuid)

        return db_mapping

    @base.remotable_classmethod
    def get_by_instance_uuid(cls, context, instance_uuid):
        db_mapping = cls._get_by_instance_uuid_from_db(context, instance_uuid)
        return cls._from_db_object(context, cls(), db_mapping)

    @staticmethod
    def _create_in_db(context, updates):
        session = db_api.get_api_session()

        db_mapping = api_models.InstanceMapping()
        db_mapping.update(updates)
        db_mapping.save(session)
        return db_mapping

    @base.remotable
    def create(self):
        db_mapping = self._create_in_db(self._context, self.obj_get_changes())
        self._from_db_object(self._context, self, db_mapping)

    @staticmethod
    def _save_in_db(context, instance_uuid, updates):
        session = db_api.get_api_session()

        with session.begin():
            db_mapping = session.query(
                    api_models.InstanceMapping).filter_by(
                            instance_uuid=instance_uuid).first()
            if not db_mapping:
                raise exception.InstanceMappingNotFound(uuid=instance_uuid)

            db_mapping.update(updates)
            session.add(db_mapping)
        return db_mapping

    @base.remotable
    def save(self):
        changes = self.obj_get_changes()
        db_mapping = self._save_in_db(self._context, self.instance_uuid,
                changes)
        self._from_db_object(self._context, self, db_mapping)
        self.obj_reset_changes()

    @staticmethod
    def _destroy_in_db(context, instance_uuid):
        session = db_api.get_api_session()

        with session.begin():
            result = session.query(api_models.InstanceMapping).filter_by(
                    instance_uuid=instance_uuid).delete()
            if not result:
                raise exception.InstanceMappingNotFound(uuid=instance_uuid)

    @base.remotable
    def destroy(self):
        self._destroy_in_db(self._context, self.instance_uuid)


@base.NovaObjectRegistry.register
class InstanceMappingList(base.ObjectListBase, base.NovaObject):
    # Version 1.0: Initial version
    VERSION = '1.0'

    fields = {
        'objects': fields.ListOfObjectsField('InstanceMapping'),
        }
    obj_relationships = {
        'objects': [('1.0', '1.0')],
        }

    @staticmethod
    def _get_by_project_id_from_db(context, project_id):
        session = db_api.get_api_session()

        with session.begin():
            db_mappings = session.query(api_models.InstanceMapping).filter_by(
                    project_id=project_id).all()

        return db_mappings

    @base.remotable_classmethod
    def get_by_project_id(cls, context, project_id):
        db_mappings = cls._get_by_project_id_from_db(context, project_id)

        return base.obj_make_list(context, cls(), objects.InstanceMapping,
                db_mappings)
