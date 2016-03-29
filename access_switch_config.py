def change_vlan(parse,vlan_access,vlan_voice,hostname):
    for intf in parse.find_objects(r"^interface Gig|^interface Ten|^interface Fast"):
        is_in_vlan2 = intf.has_child_with(r'switchport access vlan 2$')
        is_switchport_trunk = intf.has_child_with(r'switchport trunk')
        is_printer = ((hostname == "Switch1" and intf.text == "interface GigabitEthernet0/48") or \
(hostname == "Switch2" and intf.text == "interface GigabitEthernet0/47") or \
(hostname == "Switch3" and intf.text == "interface GigabitEthernet0/35")
        if is_in_vlan2 and (not is_switchport_trunk) and (not is_printer):
            cfgdiffs.append_line(intf.text)
            cfgdiffs.append_line(" shut")
            cfgdiffs.append_line(" speed auto")
            cfgdiffs.append_line(" duplex auto")
            cfgdiffs.append_line(" no switchport access vlan 2")
            cfgdiffs.append_line(' switchport access vlan ' + str(vlan_access))
            cfgdiffs.append_line(' switchport voice vlan ' + str(vlan_voice))
            cfgdiffs.append_line(" switchport port-security maximum 1 vlan voice")
            cfgdiffs.append_line(" switchport port-security maximum 1 vlan access")
            cfgdiffs.append_line(" switchport port-security aging time 2")
            cfgdiffs.append_line(" switchport port-security aging type inactivity")
            cfgdiffs.append_line(" spanning-tree portfast")
            cfgdiffs.append_line(" spanning-tree bpduguard enable")
            cfgdiffs.append_line(" description Access port, Data " + str(vlan_access) + " Voice " + str(vlan_voice))
            cfgdiffs.append_line(" no shut")
        elif is_printer:
            cfgdiffs.append_line(intf.text)
            cfgdiffs.append_line(' description PRINTER')

import os
from ciscoconfparse import CiscoConfParse
os.chdir("C:\\Users\jmelvill\\Desktop\\Switch configs")


for filename in os.listdir(os.getcwd()):
    parse = CiscoConfParse(filename, factory=True, syntax='ios')
    obj_list = parse.find_objects_dna(r'Hostname')
    hostname = obj_list[0].hostname
    cfgdiffs = CiscoConfParse([])
    cfgdiffs.append_line("! " + hostname)
    cfgdiffs.append_line("! copy tftp://10.0.100.1/" + hostname + "_diffs.cfg " +  "flash:/"+ hostname + "_diffs.cfg")
    cfgdiffs.append_line("!")
    access_vlan=0
    voice_vlan=0
    if hostname == "Switch1":
        access_vlan=64
        voice_vlan=96
    elif hostname == "Switch2":
        access_vlan=65
        voice_vlan=97
    elif hostname == "Switch3":
        access_vlan=66
        voice_vlan=98
    else:
        print ("vlans for " + hostname + " not found")
    change_vlan(parse,access_vlan,voice_vlan,hostname)
    cfgdiffs.commit()
    cfgdiffs.save_as(hostname + '_diffs.cfg')
