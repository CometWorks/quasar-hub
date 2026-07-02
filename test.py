import os
import re
import sys
import xml.etree.ElementTree as ET


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(__file__)} input_directory")
        return

    plugin_dir = sys.argv[1]

    for root, dirs, files in os.walk(plugin_dir):
        for filename in files:
            fullpath = os.path.join(root, filename)
            if os.path.isfile(fullpath) and filename.lower().endswith(".xml"):
                try:
                    validate(fullpath)
                except BaseException as error:
                    print("Error occurred while reading file ", fullpath, ": ", error)
                    sys.exit(1)

    print("All files validated")


def validate(xml_file: str):
    clean_path = xml_file.replace(os.getcwd(), "").replace("\\", "/").lstrip("/")
    if not clean_path.startswith("Plugins/"):
        raise Exception(f"{xml_file} is not in the Plugins folder")

    tree = ET.parse(xml_file)
    if tree is None:
        raise Exception(f"{xml_file} is not valid xml")

    root = tree.getroot()
    plugin_type = root.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type")
    if plugin_type != "GitHubPlugin":
        raise Exception(f"{xml_file} has invalid type: {plugin_type}")

    require_text(root, xml_file, "Id")
    require_text(root, xml_file, "RepoId")
    require_text(root, xml_file, "FriendlyName")
    require_text(root, xml_file, "Author")
    require_text(root, xml_file, "Tooltip")
    require_text(root, xml_file, "PluginKind")
    require_text(root, xml_file, "ProjectPath")
    require_text(root, xml_file, "PackageManifest")

    plugin_kind = require_text(root, xml_file, "PluginKind")
    if plugin_kind != "QuasarUiPlugin":
        raise Exception(f"'{plugin_kind}' in {xml_file} is not a supported PluginKind")

    project_path = require_text(root, xml_file, "ProjectPath")
    if not project_path.endswith(".csproj"):
        raise Exception(f"'{project_path}' in {xml_file} must point to a .csproj")

    package_manifest = require_text(root, xml_file, "PackageManifest")
    if package_manifest != "quasar-plugin.json" and not package_manifest.endswith(".json"):
        raise Exception(f"'{package_manifest}' in {xml_file} must point to a JSON package manifest")

    commit = require_text(root, xml_file, "Commit")
    if not re.search(r"^[0-9a-fA-F]{7,40}$", commit):
        raise Exception(f"'{commit}' in {xml_file} is not a valid commit id")


def require_text(root, xml_file: str, name: str) -> str:
    element = root.find(name)
    if element is None or element.text is None or element.text.strip() == "":
        raise Exception(f"{xml_file} is missing a {name}")

    return element.text.strip()


if __name__ == "__main__":
    main()
