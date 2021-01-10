#!/usr/bin/python


DOCUMENTATION = '''
---
module: my_module
author:  Atila Aloise de Almeida
short_description: Apenas um mock 
description:
    - Mockando para aprender
options:
    name:
        description:
            - O nome do item
        required: true
    description:
        description:
            - Descrição do item
        required: true
    sizeMb:
        description:
            - tamanho do item em megabytes. Default = 100
        required: false
    path:
        description:
            - Path do item. default= /tmp/
        required: false
    state:
        description:
            - Se o item deve existir ou nao
        default: present
        choices: ['present', 'absent']
'''

EXAMPLES = '''
- name: Creates a single item
  my_module:
      name: test_item
      description: simple item
      state: present

- name: Creates a custom configured item
  my_module:
      name: test_item
      description: Simple item
      SizeMB: 800
      homePath: /opt/items/test_item
      state: present

- name: Ensure item is absent
  my_module:
      name: test_item
      state: present

'''

RETURN = '''
original_state:
    description: The original state of the param that was passed in
    type: str
changed_state:
    description: The output state that the module generates
    type: str
'''

def get_item(name):
    return True

def create_item(name, **kwargs):
    return True


def update_item(name, **kwargs):
    if get_item(name):
        pass
    else:
        create_item(name, **kwargs)
    return True


def delete_item(name):
    return True

from ansible.module_utils.basic import AnsibleModule


def main():

    # Manage the parameters
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            description=dict(type="str"),
            sizeMB=dict(type="int", default=100),
            path=dict(type="str", default="/tmp/" ),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=([("state", "present", ["description"])]),
        supports_check_mode=True,
    )

    # Manage the result, assume no changes
    result = dict(
        changed=False,
        original_state='',
        changed_state=''
    )

    # Set the requested state
    requested_state = module.params["state"]

    # assign parameters to local variables
    name = module.params["name"]
    
    description = None
    if module.params["description"] is not None:
        description = module.params["description"]
    
    sizeMB = None
    if module.params["sizeMB"] is not None:
        sizeMB = module.params["sizeMB"]
    
    path = None
    if module.params["path"] is not None:
        path = module.params["path"]

    # Change for testing
    item_sizeMB = 200 
    item_description = "Simple description"
    item_path = "/tmp/test/"
    newconfs = {}


    # if the object exists and the 'requested_state' is 'present'
    # check for changes, if there is a change set 'changed' to true

    # if the object exists and the 'requested_state' is not 'present'
    # set 'changed' to true

    # if the object does not exist and the 'requested_state' is 'present'
    # set 'changed' to true
    if get_item(name):
        if requested_state == "present":
            if sizeMB:
                if sizeMB != item_sizeMB:
                    newconfs['sizeMB'] = sizeMB
                    result['changed'] = True
            if description:
                if description != item_description:
                    newconfs['description'] = description
                    result['changed'] = True
            if path:
                if path != item_path:
                    newconfs['path'] = path
                    result['changed'] = True
        else:
            result['changed'] = True
    else:
        if requested_state == "present":
            result['changed'] = True

    # if 'changed' is True and the 'requested_state' is 'present'
    # create or update the object, if not 'module.check_mode'

    # if 'changed' is True and the 'requested_state' is 'absent'
    # delete the object, if not 'module.check_mode'
    if result['changed'] and not module.check_mode:
        if requested_state == "present":
            update_item(name, **newconfs)
        else:
            delete_item(name)

    # exit with change state indicated
    module.exit_json(**result)


if __name__ == "__main__":
    main()
