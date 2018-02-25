import yaml
import pprint

with open('swiches.yaml') as f:
    templates = yaml.load(f)
    
pprint.pprint(templates)