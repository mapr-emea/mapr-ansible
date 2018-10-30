#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mapr_volume

short_description: This module manages MapR volumes

version_added: "2.4"

description:
    - "This module manages MapR volumes"

options:
    name:
        description:
            - Volume name
        required: true
    state:
        description:
            - state can be present/absent - default: present
        required: false
    topology:
        description:
            - Volume topology - default: /data
        required: false
    type:
        description:
            - Volume type can be rw/mirror - default: rw
    path:
        description:
            - Mount path of volume, if not set the volume will be unmounted.
        required: false
    mirror_volume_source:
        description:
            - Source volume to mirror like sourcevolumename@sourceclustername - fill only if type is equal to mirror
    read_ace:
        description:
            - Read ACE of the volume - default: p
        required: false
    write_ace:
        description:
            - Write ACE of the volume - default: p
        required: false
    min_replication:
        description:
            - Minimum replication of the volume - default: 2
        required: false
    replication:
        description:
            - Replication of the volume - default: 3
        required: false
    soft_quota_in_mb:
        description:
            - Advisory quota in MB. Zero value means no quota. - default: 0
        required: false
    hard_quota_in_mb:
        description:
            - Hard quota in MB. Zero value means no quota. - default: 0
        required: false
    read_only:
        description:
            - If the volume is read only - default: False
        required: false
    accountable_entity_type:
        description:
            - Accountable entity type (user/group) - default: user
        required: false
    accountable_entity_name:
        description:
            - Name of accountable entity - default: User which executes the script
        required: false
    snapshot_schedule_name:
        description:
            - Name of snapshot schedule. - default: Empty string which is no schedule
        required: false
    mirror_schedule_name:
        description:
            - Name of mirror schedule. - default: Empty string which is no schedule
        required: false
author:
    - Carsten Hufe chufe@mapr.com
'''

EXAMPLES = '''
# Pass in a message
- name: Create MapR volume
  mapr_volume:
    name: my.new.volume
    state: present
    topology: /data
    type: rw
    path: /test
    read_ace: p
    write_ace: p
    min_replication: 2
    replication: 3
    soft_quota_in_mb: 1024
    hard_quota_in_mb: 1024
    accountable_entity_type: user
    accountable_entity_name: mapr
    read_only: False
    snapshot_schedule_name: Normal Data

# hard_quota and soft_quota = 0 means unlimited
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
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        name=dict(type='str', required=True),
        path=dict(type='str', required=False, default='none'),
        state=dict(type='str', required=False, default='present'),
        topology=dict(type='str', required=False, default='/data'),
        type=dict(type='str', required=False, default='rw'),
        mirror_volume_source=dict(type='str', required=False, default='none'),
        read_ace=dict(type='str', required=False, default='p'),
        write_ace=dict(type='str', required=False, default='p'),
        accountable_entity_type=dict(type='str', required=False, default='user'),
        accountable_entity_name=dict(type='str', required=False, default=getpass.getuser()),
        min_replication=dict(type='int', required=False, default=2),
        replication=dict(type='int', required=False, default=3),
        soft_quota_in_mb=dict(type='int', required=False, default='0'),
        hard_quota_in_mb=dict(type='int', required=False, default='0'),
        read_only=dict(type='bool', required=False, default=False),
        snapshot_schedule_name=dict(type='str', required=False, default='none'),
        mirror_schedule_name=dict(type='str', required=False, default='none'),
    )


    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='No changes',
        message='No changes'
    )



    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    volume_info = get_volume_info(module.params['name'])
    volume_exists = False
    new_values = dict(
        name = module.params['name'],
        path = module.params['path'],
        topology = module.params['topology'],
        type = module.params['type'],
        mirror_volume_source = module.params['mirror_volume_source'],
        read_ace = module.params['read_ace'],
        write_ace = module.params['write_ace'],
        accountable_entity_type = module.params['accountable_entity_type'],
        accountable_entity_name = module.params['accountable_entity_name'],
        min_replication = module.params['min_replication'],
        replication = module.params['replication'],
        soft_quota_in_mb = module.params['soft_quota_in_mb'],
        hard_quota_in_mb = module.params['hard_quota_in_mb'],
        snapshot_schedule_name = module.params['snapshot_schedule_name'],
        mirror_schedule_name = module.params['mirror_schedule_name'],
        read_only = module.params['read_only']
    )

    old_values = dict()

    if volume_info == None:
        volume_exists = False
    else:
        volume_exists = True
        old_values = dict(
            name = volume_info['volumename'].encode('ascii','ignore'),
            path = volume_info['mountdir'].encode('ascii','ignore') if int(volume_info['mounted']) != 0 else 'none',
            type = "rw" if int(volume_info['volumetype']) == 0 else "mirror",
            mirror_volume_source = volume_info['mirrorSrcVolume'].encode('ascii','ignore') + "@" + volume_info['mirrorSrcCluster'] if int(volume_info['volumetype']) == 1 else 'none',
            topology = volume_info['rackpath'].encode('ascii','ignore'),
            read_ace = volume_info['volumeAces']['readAce'].encode('ascii','ignore'),
            write_ace = volume_info['volumeAces']['writeAce'].encode('ascii','ignore'),
            accountable_entity_type = "user" if int(volume_info['aetype']) == 0 else "group",
            accountable_entity_name = volume_info['aename'].encode('ascii','ignore'),
            min_replication = int(volume_info['minreplicas']),
            replication = int(volume_info['numreplicas']),
            soft_quota_in_mb = int(volume_info['advisoryquota']),
            hard_quota_in_mb = int(volume_info['quota']),
            snapshot_schedule_name = get_schedule_name_by_id(volume_info['scheduleid']),
            mirror_schedule_name = get_schedule_name_by_id(volume_info['mirrorscheduleid']),
            read_only = (int(volume_info['readonly']) != 0)
        )
        # existing volume
    if module.params['state'] == "present":
        if volume_exists:
            for key in set(old_values.keys() + new_values.keys()):
                if old_values[key] != new_values[key]:
                    result['changed'] = True
                    result['original_message'] = "Volume " + module.params['name'] + " exists - values updated"
                    break;
        else:
            result['changed'] = True
            result['original_message'] = "New volume " + module.params['name'] + " created"

        result['diff'] = dict()
        result['diff']['before'] = build_compare_str(old_values)
        result['diff']['after'] = build_compare_str(new_values)
        result['message'] = result['original_message']
        schedule_id = get_schedule_id_by_name(new_values['snapshot_schedule_name'])
        if schedule_id == "undefined":
            module.fail_json(msg='Schedule ' + module.params['snapshot_schedule_name'] + ' does not exist.', **result)
        mirror_schedule_id = get_schedule_id_by_name(new_values['mirror_schedule_name'])
        if mirror_schedule_id == "undefined":
            module.fail_json(msg='Mirror schedule ' + module.params['mirror_schedule_name'] + ' does not exist.', **result)
        if not module.check_mode and result['changed']:
            # execute changes
            execute_volume_changes(volume_exists, old_values, new_values, schedule_id, mirror_schedule_id)

    elif module.params['state'] == "absent":
        if volume_exists:
            result['changed'] = True
            result['original_message'] = "Volume " + module.params['name'] + " exists - volume removed"
            result['message'] = result['original_message']
            if not module.check_mode:
                remove_volume(module.params['name'])
    else:
        module.fail_json(msg='State ' + module.params['state'] + ' is not supported.', **result)

    module.exit_json(**result)

def build_compare_str(values):
    result = ""
    for key in values:
        result += (key + "=" + str(values[key]) + "\n")
    return result


def get_volume_info(volume_name):
    process = subprocess.Popen("maprcli volume info -name " + volume_name + " -json", shell=True, stdout=subprocess.PIPE)
    volume_info = process.communicate()
    maprclijson = json.loads(volume_info[0])
    if 'data' in maprclijson:
        return maprclijson['data'][0]
    else:
        return None

def remove_volume(volume_name):
    subprocess.check_call("maprcli volume remove -name " + volume_name + " -force true", shell=True)

def execute_volume_changes(volume_exists, old_values, new_values, schedule_id, mirror_schedule_id):
    if not volume_exists:
        # create new volume
        volume_command = "maprcli volume create -name " + new_values['name']
        if new_values['path']:
            volume_command += " -mount true"
            volume_command += " -path " + new_values['path']
        volume_command += " -createparent true"
        volume_command += " -topology " + new_values['topology']
        volume_command += " -type " + new_values['type']
        if (new_values['mirror_volume_source'] != "none") & (new_values['type'] == "mirror"):
            volume_command += " -source " + new_values['mirror_volume_source']
        volume_command += " -readAce '" + new_values['read_ace'] + "'"
        volume_command += " -writeAce '" + new_values['write_ace'] + "'"
        volume_command += " -minreplication " + str(new_values['min_replication'])
        volume_command += " -replication " + str(new_values['replication'])
        volume_command += " -advisoryquota " + str(new_values['soft_quota_in_mb'])
        volume_command += " -quota " + str(new_values['hard_quota_in_mb'])
        volume_command += " -readonly " + ("1" if new_values['read_only'] else "0")
        volume_command += " -aetype " + ("0" if new_values['accountable_entity_type'] == "user" else "1")
        volume_command += " -ae " + new_values['accountable_entity_name']
        if schedule_id != "0":
            volume_command += " -schedule " + schedule_id
        if mirror_schedule_id != "0":
            volume_command += " -mirrorschedule " + mirror_schedule_id
        subprocess.check_call(volume_command, shell=True)
    else:
        # update volume
        volume_command = "maprcli volume modify -name " + new_values['name']
        if new_values['type'] != old_values['type']:
            volume_command += " -type " + new_values['type']
            if (new_values['mirror_volume_source'] != "none") & (new_values['type'] == "mirror"):
                volume_command += " -source " + new_values['mirror_volume_source']
        if (new_values['type'] == "mirror") & (new_values['mirror_schedule_name'] != old_values['mirror_schedule_name']):
            volume_command += " -mirrorschedule " + mirror_schedule_id
        if new_values['type'] != "mirror":
            volume_command += " -readAce '" + new_values['read_ace'] + "'"
            volume_command += " -writeAce '" + new_values['write_ace'] + "'"
        volume_command += " -minreplication " + str(new_values['min_replication'])
        volume_command += " -replication " + str(new_values['replication'])
        volume_command += " -advisoryquota " + str(new_values['soft_quota_in_mb'])
        volume_command += " -quota " + str(new_values['soft_quota_in_mb'])
        volume_command += " -readonly " + ("1" if new_values['read_only'] else "0")
        volume_command += " -aetype " + ("0" if new_values['accountable_entity_type'] == "user" else "1")
        volume_command += " -ae " + new_values['accountable_entity_name']
        subprocess.check_call(volume_command, shell=True)
        if new_values['topology'] != old_values['topology']:
            subprocess.check_call("maprcli volume move -name " + new_values['name'] + " -topology " + new_values['topology'], shell=True)
        # when no schedule is set and you set 0 again an error occurs
        print("aaa" + new_values['snapshot_schedule_name'])
        print("bbb" + old_values['snapshot_schedule_name'])
        if new_values['snapshot_schedule_name'] != old_values['snapshot_schedule_name']:
            subprocess.check_call("maprcli volume modify -name " + new_values['name'] + " -schedule " + schedule_id, shell=True)
        if new_values['path'] != old_values['path']:
            if old_values['path']:
                subprocess.check_call("maprcli volume unmount -name " + new_values['name'] + " -force true", shell=True)
            if new_values['path']:
                subprocess.check_call("maprcli volume mount -createparent true -name " + new_values['name'] + " -path " + new_values['path'], shell=True)

def get_schedule_name_by_id(schedule_id):
    if schedule_id == 0:
        return "none"
    process = subprocess.Popen("maprcli schedule list -json", shell=True, stdout=subprocess.PIPE)
    schedule_info = process.communicate()
    maprclijson = json.loads(schedule_info[0])
    for item in maprclijson['data']:
        if str(item['id']) == str(schedule_id):
            return item['name'].encode('ascii','ignore')
    return 'none'

def get_schedule_id_by_name(schedule_name):
    if schedule_name == "none":
        return "0"
    process = subprocess.Popen("maprcli schedule list -json", shell=True, stdout=subprocess.PIPE)
    schedule_info = process.communicate()
    maprclijson = json.loads(schedule_info[0])
    for item in maprclijson['data']:
        if item['name'] == schedule_name:
            return str(item['id'])
    return "none"

def main():
    run_module()

if __name__ == '__main__':
    main()
