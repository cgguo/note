#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import shutil 
import time  
import pprint

from shotgun_connection import Connection

sys.path.append('U:/toolset/lib/production')


# copy file
def copyFiles(path="Z:\\projects\\tst\\asset\\chr", asset_name=None, version="v001"):
    """copyFiles("Z:\\projects\\tst\\asset\\chr", "man")
    """  
    mod_path = "%s\\%s\\mod\\publish\\%s.mod.model" % (path, asset_name, asset_name)
    lay_path = "%s\\%s\\rig\\publish\\%s.rig.rigging_layout.%s" % (path, asset_name, asset_name, version)

    # mod_path = "D:\\controls\\dog.mod.model"
    # lay_path = "D:\\controls\\dog.rig.rigging_layout"

    # set preview path
    if not os.path.exists(mod_path):
        return

    all_dir = os.listdir(mod_path)

    if not os.path.exists(lay_path):
        os.makedirs(lay_path)

    print "++++++++++++++++++++", asset_name
    for f in all_dir:

        if f.count(".ma"):
            f_path = "%s\\%s" % (mod_path, f)
            shutil.copy(f_path,  lay_path)
            print f

        # copy preview folder
        elif f.count("preview"): 
            mod_preview = os.path.join(mod_path, "preview")
            lay_preview = os.path.join(lay_path, "preview")

            # copy all file in the preview folder
            preview_file = os.listdir(mod_preview)
            if preview_file:
                for item in preview_file:
                    # make folder
                    if not os.path.exists(lay_preview):
                        os.makedirs(lay_preview)

                    # copy file
                    item_path = "%s\\%s" % (mod_preview, item)
                    item_preview = "%s\\%s" % (lay_preview, item)
                    if not os.path.exists(item_preview):
                        shutil.copy(item_path,  lay_preview)
                        print item

    print "-------------------", asset_name

"""
d_version = {'project': {'type': 'Project', 'name': 'TST', 'id': 102}, 
            'entity': {'type': 'Asset', 'name': 'cape_teen', 'id': 7387}}
            'sg_task': {'type': 'Task', 'name': 'rigging_body', 'id': 143558}, 
            'code': 'cape_teen.rig.rigging_body.v006', 
            'description': u'\u6253\u5370version info  \n { \u6a21\u578b\u7248\u672c\u4e3a\uff1av010 }', 
            'user': None, 
            'sg_version_folder': {'local_path': 'Z:\\projects\\tst\\asset\\chr\\cape_teen\\rig\\publish\\cape_teen.rig.rigging_body.v006\\', 
                                    'name': 'cape_teen.rig.rigging_body.v006', 
                                    'content_type': None, 
                                    'link_type': 'local'}, 
            'sg_version_type': 'Downstream', 
            'tag_list': [u'\u6a21\u5757'], 
            'created_by': None}
"""

def create_sg_version_batch(asset_name="cape_teen"):
    # get info
    project_name = "CAT"
    project_name_lower = "cat"

    task_name = "rigging_layout"
    version_name = '%s.rig.%s.v001' % (asset_name, task_name)

    # init functions
    sg = Connection('get_project_info').get_sg()

    # 1.get project info
    proj_info = sg.find_one('Project', [['name', 'is', project_name]])
    proj_info["name"] = project_name

    # 2.get asset info
    asset_entity = sg.find_one('Asset', [['project', 'is', proj_info], ['code', 'is', asset_name]])
    asset_entity["name"] = asset_name

    # 3.get task id
    task_info_rig = sg.find('Task', [['entity', 'is', asset_entity], ['content','is',task_name]], ["step"])

    # init vars
    task = {'type': 'Task', 'name': task_name, 'id': task_info_rig[0]["id"]}
    local_path = 'Z:\\projects\\%s\\asset\\chr\\%s\\rig\\publish\\%s\\' % (project_name_lower, asset_name, version_name)
    description = u"批量publish模型文件给layout"
    user = None

    d_version = {'project':proj_info, 
                'entity':asset_entity, 
                'sg_task':task,
                'code':version_name,
                'description':description,
                'user':user,
                'sg_version_folder':{ 'local_path': local_path, 
                                        'name':version_name,
                                        'content_type':None, 
                                        'link_type':'local'} , 

                'sg_version_type': "Downstream", 
                'tag_list':[u'\u6a21\u5757'], 
                'created_by':user}


    d_version_str = __dict_qstr2str(d_version)

    v_info = sg.create('Version', d_version_str)
    if not v_info:
        return  pprint.pformat(d_version_str)

    # Set related tasks
    task_info = sg.find_one('Task', [['id', 'is', task['id']]], ['step'])
    l_tasks = sg.find('Task', [['entity', 'is', entity]], ['step'])
    l_related_tasks = [task_info]

    # print 'local_path : '+local_path
    # print d_version
    # print d_version_str
    # print l_related_tasks
    #print v_info
    #print task_info
    #print l_tasks
    #print l_related_tasks

    for task in l_tasks:
        if entity['type'] == 'Asset' and task_info['step']['name'] == 'art':
            if task['step']['name'] == 'mod':
                l_related_tasks.append(task)
        elif entity['type'] == 'Asset' and task_info['step']['name'] == 'mod':
            if not task['step']['name'] in ['art', 'mod']:
                l_related_tasks.append(task)
        elif entity['type'] == 'Shot' and task_info['step']['name'] == 'lay':
            if task['step']['name'] != 'lay':
                l_related_tasks.append(task)

    sg.update('Version', v_info['id'], {'sg_related_tasks': l_related_tasks })
    print asset_name, "-------------------sg_final"

def __dict_qstr2str(dict_data):
    result={}
    for k,v in dict_data.items():
        if v.__class__.__name__ == 'QString':
            result[k]=unicode(v)
        elif v.__class__.__name__ == 'list':
            new_v=[]
            for vv in v:
                if vv.__class__.__name__ == 'QString':
                    new_v.append(unicode(vv))
                else:
                    new_v.append(vv)
            result[k]=new_v
        else:
            result[k]=v
    return result


# copy files
copy_chars=["pangolin_a",
            "rabbit_bar_a",
            "trachypithecus_francoisi_a",
            "macaque_monkey_a",
            "bar_animal_c",
            "bar_animal_d",
            "bar_animal_e",
            "bar_animal_g",
            "bar_animal_h",
            "bar_animal_i",
            "bar_animal_j",
            "bar_animal_k",
            "bar_animal_l",
            "bar_animal_o",
            "rabbit_a",
            "bamboo_rat_a",
            "bamboo_rat_b",
            "bar_animal_hb",
            "bar_animal_nb",
            "bar_animal_eb",
            "bar_animal_mb",
            "bar_animal_db",
            "bar_animal_gb",
            "bar_animal_fb",
            "macaque_monkey_b",
            "bar_animal_ib",
            "bar_animal_jb",
            "trachypithecus_francoisi_b",
            "prisoner_animal_l",   
            "prisoner_trachypithecus_francoisi_a", 
            "prisoner_animal_d",   
            "prisoner_bamboo_rat_a",   
            "prisoner_animal_e",   
            "prisoner_animal_h",   
            "prisoner_animal_f",   
            "prisoner_pangolin_a"]

for char in copy_chars:
    path = "Z:\\projects\\cat\\asset\\chr"
    copyFiles(path, char)

# # final
# for char in copy_chars:
#     create_sg_version_batch(char)