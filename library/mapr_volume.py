#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mapr_volumes

short_description: This module manages the state of MapR volumes

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
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
    path: /test
    read_ace: p
    write_ace: p
    min_replication: 2
    replication: 3
    soft_quota_in_mb: 1024
    hard_quota_in_mb: 1024
    read_only: False
    accountable_entity_type: user
    accountable_entity_name: mapr
    read_only: False
    
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
        path=dict(type='str', required=False, default=''),
        state=dict(type='str', required=False, default='present'),
        topology=dict(type='str', required=False, default='/data'),
        read_ace=dict(type='str', required=False, default='p'),
        write_ace=dict(type='str', required=False, default='p'),
        accountable_entity_type=dict(type='str', required=False, default='user'),
        accountable_entity_name=dict(type='str', required=False, default=getpass.getuser()),
        min_replication=dict(type='int', required=False, default=2),
        replication=dict(type='int', required=False, default=3),
        soft_quota_in_mb=dict(type='int', required=False, default='0'),
        hard_quota_in_mb=dict(type='int', required=False, default='0'),
        read_only=dict(type='bool', required=False, default=False)
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
        read_ace = module.params['read_ace'],
        write_ace = module.params['write_ace'],
        accountable_entity_type = module.params['accountable_entity_type'],
        accountable_entity_name = module.params['accountable_entity_name'],
        min_replication = module.params['min_replication'],
        replication = module.params['replication'],
        soft_quota_in_mb = module.params['soft_quota_in_mb'],
        hard_quota_in_mb = module.params['hard_quota_in_mb'],
        read_only = module.params['read_only']
    )

    old_values = dict()

    if volume_info == None:
        volume_exists = False
    else:
        volume_exists = True
        old_values = dict(
            name = volume_info['volumename'].encode('ascii','ignore'),
            path = volume_info['mountdir'].encode('ascii','ignore') if int(volume_info['mounted']) != 0 else '',
            topology = volume_info['rackpath'].encode('ascii','ignore'),
            read_ace = volume_info['volumeAces']['readAce'].encode('ascii','ignore'),
            write_ace = volume_info['volumeAces']['writeAce'].encode('ascii','ignore'),
            accountable_entity_type = "user" if int(volume_info['aetype']) == 0 else "group",
            accountable_entity_name = volume_info['aename'].encode('ascii','ignore'),
            min_replication = int(volume_info['minreplicas']),
            replication = int(volume_info['numreplicas']),
            soft_quota_in_mb = int(volume_info['advisoryquota']),
            hard_quota_in_mb = int(volume_info['quota']),
            read_only = (int(volume_info['readonly']) != 0)
        )
        # existing volume
    if module.params['state'] == "present":
        if volume_exists:
            for key in set(old_values.keys() + new_values.keys()):
                if old_values[key] != new_values[key]:
                    result['changed'] = True
                    result['original_message'] = "Volume exists - values updated"
                    break;
        else:
            result['changed'] = True
            result['original_message'] = "New volume created"


        result['diff'] = dict()
        result['diff']['before'] = str(old_values)
        result['diff']['after'] = str(new_values)
        result['message'] = result['original_message']
        if not module.check_mode:
            # execute changes
            execute_volume_changes(volume_exists, old_values, new_values)

    elif module.params['state'] == "absent":
        # TODO
        print("not yet implemented")
    else:
        module.fail_json(msg='State ' + module.params['state'] + ' is not supported.', **result)

    module.exit_json(**result)

def get_volume_info(volume_name):
    process = subprocess.Popen("maprcli volume info -name " + volume_name + " -json", shell=True, stdout=subprocess.PIPE)
    volume_info = process.communicate()
    maprclijson = json.loads(volume_info[0])
    if 'data' in maprclijson:
        return maprclijson['data'][0]
    else:
        return None

def execute_volume_changes(volume_exists, old_values, new_values):
    # TODO add -ae -aetype
    if not volume_exists:
        # create new volume
        volume_command = "maprcli volume create -name " + new_values['name']
        if new_values['path']:
            volume_command += " -mount true"
            volume_command += " -path " + new_values['path']
        volume_command += " -topology " + new_values['topology']
        volume_command += " -readAce " + new_values['read_ace']
        volume_command += " -writeAce " + new_values['write_ace']
        volume_command += " -minreplication " + str(new_values['min_replication'])
        volume_command += " -replication " + str(new_values['replication'])
        volume_command += " -advisoryquota " + str(new_values['soft_quota_in_mb'])
        volume_command += " -quota " + str(new_values['hard_quota_in_mb'])
        volume_command += " -readonly " + ("1" if new_values['read_only'] else "0")
        volume_command += " -aetype " + ("0" if new_values['accountable_entity_type'] == "user" else "1")
        volume_command += " -ae " + new_values['accountable_entity_name']
        subprocess.check_call(volume_command, shell=True)
    else:
        # update volume
        volume_command = "maprcli volume modify -name " + new_values['name']
        volume_command += " -readAce " + new_values['read_ace']
        volume_command += " -writeAce " + new_values['write_ace']
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
        if new_values['path'] != old_values['path']:
            if old_values['path']:
                subprocess.check_call("maprcli volume unmount -name " + new_values['name'] + " -force true", shell=True)
            if new_values['path']:
                subprocess.check_call("maprcli volume mount -name " + new_values['name'] + " -path " + new_values['path'], shell=True)

def main():
    run_module()

if __name__ == '__main__':
    main()

    # https://rogerwelin.github.io/ansible/2016/04/25/creating-custom-ansible-modules.html