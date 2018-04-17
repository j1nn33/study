#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  python3 /home/ubuntu/workspace/python/Jinja/example_1/router_config_generator.py 

import yaml
from router_template import template_r1

routers = yaml.load(open('/home/ubuntu/workspace/python/conspect/Jinja/example_1/routers_info.yml'))
print (routers)
for router in routers:
    r1_conf = router['name']+'_r1.txt'
    with open(r1_conf,'w') as f:
        f.write(template_r1.render(router))
