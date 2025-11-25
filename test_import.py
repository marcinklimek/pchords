import sys
import traceback

try:
    from backend.api import scales
    print("SUCCESS: scales imported")
except Exception as e:
    print("ERROR importing scales:")
    traceback.print_exc()
    sys.exit(1)
