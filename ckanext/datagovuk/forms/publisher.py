log = __import__('logging').getLogger(__name__)
import os
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class PublisherForm(plugins.SingletonPlugin, toolkit.DefaultOrganizationForm):
    plugins.implements(plugins.IGroupForm, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)

    # IConfigurer

    def update_config(self, config):
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))

    # IGroupForm

    def form_to_db_schema(self):
        from ckan.logic.schema import group_form_schema
        schema = group_form_schema()
        log.debug("c")
        for contact_key in ['contact-name', 'contact-email', 'contact-phone', 'foi-name', 'foi-email', 'foi-web', 'foi-phone']:
            schema.update({contact_key: [toolkit.get_validator('ignore_missing'),
                                         toolkit.get_converter('convert_to_extras'),
                                         unicode]})
        return schema

    def db_to_form_schema(self, package_type=None):
        from ckan.logic.schema import default_group_schema
        schema = default_group_schema()
        for contact_key in ['contact-name', 'contact-email', 'contact-phone', 'foi-name', 'foi-email', 'foi-web', 'foi-phone']:
            schema.update({contact_key: [toolkit.get_converter('convert_from_extras'),
                                         toolkit.get_validator('ignore_missing'),
                                         unicode]})
        schema['num_followers'] = []
        schema['created'] = []
        schema['display_name'] = []
        schema['package_count'] = [toolkit.get_validator('ignore_missing')]
        schema['packages'] = {'__extras': [toolkit.get_validator('keep_extras')]}
        schema['revision_id'] = []
        schema['state'] = []
        schema['users'] = {'__extras': [toolkit.get_validator('keep_extras')]}
        log.debug(schema)
        return schema

    def group_types(self):
       return ['organization']

    def group_controller(self):
        return 'organization'

    def is_fallback(self):
        return True
