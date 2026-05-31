import yaml
import pprint

# WRITE TO FILE
with open("containers.txt", "w") as file_to_write:
  file_to_write.writelines("Pod\n")
  file_to_write.writelines("Service\n")
  file_to_write.writelines("Volume\n")
  file_to_write.writelines("Namespace\n")

# cat containers.txt
# Pod
# Service
# Volume
# Namespace 

# READ FROM FILE
with open("containers.txt") as file_to_read:
  lines = file_to_read.readlines()
  print(lines)

# ['Pod\n', 'Service\n', 'Volume\n', 'Namespace\n']

# READ FROM FILE  
with open('containers.txt', 'r') as file:
    for line in file:
        print(line.strip())  # strip() удаляет символы переноса строки

# Pod
# Service
# Volume
# Namespace

# YAML

kubernetes_components = {
    "Pod": "Basic building block of Kubernetes.",
    "Service": "An abstraction for dealing with Pods.",
    "Volume": "A directory accessible to containers in a Pod.",
    "Namespaces": "A way to divide cluster resources between users."
}


with open("kubernetes_info.yaml", "w") as yaml_to_write:
  yaml.safe_dump(kubernetes_components, yaml_to_write, default_flow_style=False)


# cat kubernetes_info.yaml
# Namespaces: A way to divide cluster resources between users.
# Pod: Basic building block of Kubernetes.
# Service: An abstraction for dealing with Pods.
# Volume: A directory accessible to containers in a Pod.

with open("kubernetes_info.yaml", "rb") as yaml_to_read:
  result = yaml.safe_load(yaml_to_read)

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result)

#{   'Namespaces': 'A way to divide cluster resources between users.',
#    'Pod': 'Basic building block of Kubernetes.',
#    'Service': 'An abstraction for dealing with Pods.',
#    'Volume': 'A directory accessible to containers in a Pod.'}

