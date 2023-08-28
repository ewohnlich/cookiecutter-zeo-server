# post generation step 1: replace relative with absolute path
# theres no way to get this path while generating the files

import os
import re
from pathlib import Path

from cookiecutter.utils import work_in

target = """{{ cookiecutter.zeo_target }}"""
cwd = Path.cwd()
basedir = cwd.parent

with work_in(basedir):
    for dir, subdirs, files in os.walk(cwd / "etc"):
        for filename in files:
            infile = Path(dir) / filename
            lines = []
            try:
                with open(infile, "r") as fio:
                    for line in fio:
                        mo = re.match(r".*ABSPATH\((.*?)\).*", line)
                        if mo:
                            for path in mo.groups():
                                line = line.replace(
                                    f"ABSPATH({path})", os.path.abspath(path)
                                )
                        lines.append(line)

                with open(infile, "w") as fio:
                    fio.truncate()
                    for line in lines:
                        fio.writelines(line)
            except Exception:
                print(f"Can not replace ABSPATH() in file {infile}")

# post generation step 2: generate directories
Path("{{ cookiecutter.location_clienthome }}").mkdir(parents=True, exist_ok=True)
Path("{{ cookiecutter.location_log }}").mkdir(parents=True, exist_ok=True)
Path("{{ cookiecutter.db_filestorage_location }}").mkdir(parents=True, exist_ok=True)
for db in '{{ cookiecutter.mounted_dbs }}'.split(','):
    Path("{{ cookiecutter.db_filestorage_location }}/" + db).mkdir(parents=True, exist_ok=True)
Path("{{ cookiecutter.db_blobs_location }}").mkdir(parents=True, exist_ok=True)
for db in '{{ cookiecutter.mounted_dbs }}'.split(','):
    Path("{{ cookiecutter.db_blobs_location }}/" + db).mkdir(parents=True, exist_ok=True)
