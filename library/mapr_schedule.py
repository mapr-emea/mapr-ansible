#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mapr_schedule

short_description: This module manages MapR schedules

version_added: "2.4"

description:
    - "This module manages MapR schedules"

options:
    name:
        description:
            - Schedule name
        required: true
    state:
        description:
            - state can be present/absent - default: present
        required: false
    rules:
        description:
            - MapR format from command line. See example below.
        required: false
author:
    - Carsten Hufe chufe@mapr.com
'''

EXAMPLES = '''
# Pass in a message
- name: Modify MapR schedule
  mapr_schedule:
    name: testrule
    state: present
    rules:
      - frequency: daily
        time: 0
        retain: 7d
      - frequency: weekly
        date: sun
        time: 0
        retain: 4w
      - frequency: monthly
        date: "1"
        time: 0
        retain: 2m
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

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=True),
        rules=dict(type='list', required=True),
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

    schedule_info = get_schedule_info(module.params['name'])
    schedule_exists = False

    new_values = dict(
        name = module.params['name'],
        rules = module.params['rules']
    )
    if schedule_info != None:
        schedule_exists = True
        old_values = dict(
            name = schedule_info['name'],
            rules = schedule_info['rules']
        )

    if module.params['state'] == "present":
        if schedule_exists:
            for key in set(old_values.keys() + new_values.keys()):
                if key == "rules":
                    rule_pairs = zip(new_values['rules'], old_values['rules'])
                    if any(x != y for x, y in rule_pairs):
                        result['changed'] = True
                        result['original_message'] = "Schedule " + module.params['name'] + " exists - values updated"
                        result['message'] = result['original_message']
                        break
                elif old_values[key] != new_values[key]:
                    result['changed'] = True
                    result['original_message'] = "Schedule " + module.params['name'] + " exists - values updated"
                    result['message'] = result['original_message']
                    break
            result['diff'] = dict()
            result['diff']['before'] = build_compare_str(old_values)
            result['diff']['after'] = build_compare_str(new_values)
        else:
            result['changed'] = True
            result['original_message'] = "New schedule " + module.params['name'] + " created"
        if not module.check_mode and result['changed']:
            # execute changes
            execute_schedule_changes(schedule_exists, schedule_info['id'] if schedule_info != None else 0, new_values)
    elif module.params['state'] == "absent":
        if schedule_exists:
            result['changed'] = True
            result['original_message'] = "Schedule " + module.params['name'] + " exists - volume removed"
            result['message'] = result['original_message']
            if not module.check_mode:
                remove_schedule(schedule_info['id'])
    else:
        module.fail_json(msg='State ' + module.params['state'] + ' is not supported.', **result)

    module.exit_json(**result)

def build_compare_str(values):
    result = ""
    for key in values:
        result += (key + "=" + str(values[key]) + "\n")
    return result

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x
    return dict(map(ascii_encode, pair) for pair in data.items())

def get_schedule_info(name):
    process = subprocess.Popen("maprcli schedule list -json", shell=True, stdout=subprocess.PIPE)
    entity_info = process.communicate()
    maprclijson = json.loads(entity_info[0], object_hook=ascii_encode_dict)
    if 'data' in maprclijson:
        schedules = maprclijson['data']
        for schedule in schedules:
            if schedule['name'] == name:
                return schedule

    return None
def remove_schedule(id):
    subprocess.check_call("maprcli schedule remove -id " + str(id), shell=True)

def execute_schedule_changes(schedule_exists, schedule_id, new_values):
    if schedule_exists:
        update_cmd = "maprcli schedule modify"
        update_cmd += " -id " + str(schedule_id)
        update_cmd += " -rules \"" + str(new_values['rules']) + "\""
        subprocess.check_call(update_cmd, shell=True)
    else:
        update_cmd = "maprcli schedule create"
        update_cmd += " -schedule \"" + str(new_values) + "\""
        subprocess.check_call(update_cmd, shell=True)

def main():
    run_module()

if __name__ == '__main__':
    main()
