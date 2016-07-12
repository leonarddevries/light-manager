import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import lightmanager
print("Testing lightmanager version {}".format(lightmanager.version))

# In every test file: from context import lightmanager
