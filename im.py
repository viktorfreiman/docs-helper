import importlib.util
from pprint import pprint
import sys

# from: https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

file_path = "/workspaces/docs-helper/docs/conf.py"
module_name = "conf"

# read the ref api
spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)

# spec is of type :py:class:`importlib.machinery.ModuleSpec`

# sys.mod is good to set
sys.modules[module_name] = module

# Execte the imported file
spec.loader.exec_module(module)

pprint(vars(module))
