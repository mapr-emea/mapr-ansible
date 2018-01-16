#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mapr_entity

short_description: This module manages MapR accountable entities

version_added: "2.4"

description:
    - "This module manages MapR accountable entities"

options:
    name:
        description:
            - Entity name
        required: true
    type:
        description:
            - entity type: user or group
        required: true
    email:
        description:
            - Contact email for entity
        required: false
    soft_quota_in_mb:
        description:
            - Advisory quota in MB. Zero value means no quota. - default: 0
        required: false
    hard_quota_in_mb:
        description:
            - Hard quota in MB. Zero value means no quota. - default: 0
        required: false
author:
    - Carsten Hufe chufe@mapr.com
'''

EXAMPLES = '''
# Pass in a message
- name: Modify MapR entity
  mapr_entity:
    name: mapr
    type: user
    email: abc@email.com
    soft_quota_in_mb: 1024
    hard_quota_in_mb: 1024
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import json
import getpass
import tempfile

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        type=dict(type='str', required=True),
        name=dict(type='str', required=True),
        email=dict(type='str', required=False, default=''),
        soft_quota_in_mb=dict(type='int', required=False, default='0'),
        hard_quota_in_mb=dict(type='int', required=False, default='0')
    )

    result = dict(
        changed=False,
        original_message='No changes',
        message='No changes'
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    entity_info = get_entity_info(module.params['type'], module.params['name'])
    if entity_info == None:
        entity_exists = False
        old_values = dict()
        # module.fail_json(msg="Accountable entity " + module.params['name'] + " does not exist.", **result)
    else:
        entity_exists = True
        old_values = dict(
            name = entity_info['EntityName'].encode('ascii','ignore'),
            type = "user" if int(entity_info['EntityType']) == 0 else 'group',
            email = (entity_info['EntityEmail'].encode('ascii','ignore') if 'EntityEmail' in entity_info else ''),
            soft_quota_in_mb = int(entity_info['EntityAdvisoryquota']),
            hard_quota_in_mb = int(entity_info['EntityQuota'])
        )

    new_values = dict(
        name = module.params['name'],
        type = module.params['type'],
        email = module.params['email'],
        soft_quota_in_mb = module.params['soft_quota_in_mb'],
        hard_quota_in_mb = module.params['hard_quota_in_mb']
    )


    if entity_exists:
        for key in set(old_values.keys() + new_values.keys()):
            if old_values[key] != new_values[key]:
                result['changed'] = True
                result['original_message'] = "Entity " + module.params['name'] + " exists - values updated"
                result['message'] = result['original_message']
                break
    else:
        result['changed'] = True
        result['original_message'] = "New entity " + module.params['name'] + " created"
        result['message'] = result['original_message']

    result['diff'] = dict()
    result['diff']['before'] = build_compare_str(old_values)
    result['diff']['after'] = build_compare_str(new_values)


    if not module.check_mode and result['changed']:
        if not entity_exists:
            execute_entity_creation(new_values['type'], new_values['name'])
        # execute changes
        execute_entity_changes(new_values['type'], new_values['name'], new_values)

    module.exit_json(**result)

def build_compare_str(values):
    result = ""
    for key in values:
        result += (key + "=" + str(values[key]) + "\n")
    return result

def get_entity_info(type, name):
    converted_type = "0" if type == "user" else "1"
    process = subprocess.Popen("maprcli entity info -name " + name + " -type " + converted_type + " -json", shell=True, stdout=subprocess.PIPE)
    entity_info = process.communicate()
    maprclijson = json.loads(entity_info[0])
    if 'data' in maprclijson and len(maprclijson['data']) > 0:
        return maprclijson['data'][0]
    else:
        return None

def load_volume_names():
    volume_names = []

    maprcli_proc = subprocess.Popen('maprcli volume list -columns n -json', shell=True, stdout=subprocess.PIPE)
    proc_stdout = maprcli_proc.communicate()
    proc_json = json.loads(proc_stdout[0])
    for volume in proc_json['data']:
        volume_names.append(str(volume['volumename']))

    return volume_names

def suggest_temp_volume_name():
    volume_names = load_volume_names()
    while True:
        tmp_volume_name = 'taec.' + next(tempfile._get_candidate_names())
        volume_name_already_taken = False
        for volume_name in volume_names:
            if str(volume_name) == tmp_volume_name:
                volume_name_already_taken = True
                break
        if volume_name_already_taken == False:
            break

    return tmp_volume_name

def create_temp_volume(type, name):
    failed_counter = 0
    while failed_counter < 5:
        tmp_volume_name = suggest_temp_volume_name()
        maprcli_cmd =  'maprcli volume create'
        maprcli_cmd += ' -name ' + tmp_volume_name
        maprcli_cmd += ' -ae ' + name
        maprcli_cmd += ' -aetype ' + ('0' if type == 'user' else '1')
        maprcli_vol_create = subprocess.Popen(maprcli_cmd, shell=True)
        exitcode = maprcli_vol_create.wait()
        if exitcode != 0:
            failed_counter += 1
        else:
            return tmp_volume_name;

    raise RuntimeError('Could not create temporary volume!')

def remove_temp_volume(volume_name):
    failed_counter = 0
    while failed_counter < 5:
        maprcli_vol_remove = subprocess.Popen('maprcli volume remove -name ' + volume_name, shell=True)
        exitcode = maprcli_vol_remove.wait()
        if exitcode != 0:
            failed_counter += 1
        else:
            return

    raise RuntimeError('Could not remove temporary volume ' + volume_name + '!')

def execute_entity_creation(type, name):
    '''
        Create a temporary volume and assign the user/group defined by type, name as accountable entity
    '''
    temp_volume_name = create_temp_volume(type, name)
    remove_temp_volume(temp_volume_name)


def execute_entity_changes(type, name, new_values):
    update_cmd = "maprcli entity modify"
    update_cmd += " -type " + ("0" if type == "user" else "1")
    update_cmd += " -name " + name
    update_cmd += " -email '" + new_values['email'] + "'"
    update_cmd += " -advisoryquota " + str(new_values['soft_quota_in_mb'])
    update_cmd += " -quota " + str(new_values['hard_quota_in_mb'])
    subprocess.check_call(update_cmd, shell=True)

def main():
    run_module()

if __name__ == '__main__':
    main()
