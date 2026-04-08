import os
import sysconfig
import site

# Python will check both possible installation folders
paths = [
    os.path.join(sysconfig.get_path("scripts"), "openenv.exe"),
    os.path.join(site.getuserbase(), "Scripts", "openenv.exe")
]

for exe_path in paths:
    if os.path.exists(exe_path):
        print(f"🚀 Found openenv at: {exe_path}")
        print("📦 Packaging and pushing to Hugging Face...")
        os.system(f'"{exe_path}" push')
        break
else:
    print("❌ Could not find openenv.exe. We might need to reinstall it!")