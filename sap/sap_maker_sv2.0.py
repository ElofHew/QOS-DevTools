"""
@ PY OS Improved & Quarter OS
@ Shizuku Software Manager
@ Shizuku Application Package Maker
@ Author: ElofHew
@ Version: 2.0
@ Date: 2025.07.28
"""

import os
import sys
import time
import json
import zipfile
from colorama import init, Fore, Style
from subprocess import call, run

init(autoreset=True)

def pack_apps(app_name, app_version):
    print("=" * 30)
    print(f"{Fore.CYAN}Packing Application Package...{Style.RESET_ALL}")
    source_directory = "app_files"
    output_archive = f"{app_name}_v{app_version}.zip"
    sap_archive = f"{app_name}_v{app_version}.sap"

    try:
        with zipfile.ZipFile(output_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, source_directory))
        print(f"{Fore.GREEN}Application Compressed Successfully.{Style.RESET_ALL}")

        try:
            os.rename(output_archive, sap_archive)
            print(f"{Fore.GREEN}SAP File Renamed Successfully.{Style.RESET_ALL}")
            sap_path = os.path.abspath(sap_archive)
            print(f"{Fore.GREEN}Path: {sap_path}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}Error: SAP File not found.{Style.RESET_ALL}")
        except FileExistsError:
            os.remove(sap_archive)
            os.rename(output_archive, sap_archive)
            print(f"{Fore.GREEN}SAP File Renamed Successfully.{Style.RESET_ALL}")
            sap_path = os.path.abspath(sap_archive)
            print(f"{Fore.GREEN}Path: {sap_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input(f"{Fore.RED}(Press Enter to Exit.){Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.CYAN}Return to Main Menu in 3s...{Style.RESET_ALL}")
    time.sleep(3)
    run(["cls" if os.name == "nt" else "clear"])
    call([sys.executable, __file__])
    sys.exit()

def load_app_info():
    try:
        with open("app_files/info.json", "r", encoding="utf-8") as f:
            app_info = json.load(f)
            return {
                "name": str(app_info.get("name", "None")),
                "version": str(app_info.get("version", "None")),
                "vcode": str(app_info.get("vcode", "None")),
                "author": str(app_info.get("author", "None")),
                "description": str(app_info.get("description", "None")),
                "category": str(app_info.get("category", "None")),
                "tags": str(app_info.get("tags", "None")),
                "min_python_version": str(app_info.get("min_python_version", "None")),
                "target_python_version": str(app_info.get("target_python_version", "None")),
                "compatible_os": str(app_info.get("compatible_os", "None"))
            }
    except FileNotFoundError:
        print(f"{Fore.RED}Error: info.json not found.{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: info.json is not a valid JSON file.{Style.RESET_ALL}")
        sys.exit(1)
    except (KeyError, TypeError) as e:
        print(f"{Fore.RED}Error: info.json is missing some required fields: {e}{Style.RESET_ALL}")
        sys.exit(1)

def check_app_files():
    missing_files = []
    required_files = ["info.json", "requirements.txt", "main.py"]

    for file in required_files:
        if not os.path.exists(os.path.join("app_files", file)):
            missing_files.append(file)

    if missing_files:
        print("=" * 30)
        print(f"{Fore.YELLOW}Files missing: {', '.join(missing_files)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}Please put all required files in the 'app_files' folder.{Style.RESET_ALL}")
        input(f"{Fore.LIGHTGREEN_EX}(Press Enter to Continue.){Style.RESET_ALL}")
        find_app_files()
    else:
        print(f"{Fore.LIGHTGREEN_EX}All required files found.{Style.RESET_ALL}")
        app_info = load_app_info()
        print("=" * 30)
        print(f"{Fore.LIGHTBLUE_EX}Application Info:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Name: {app_info['name']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Version: {app_info['version']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Vercode: {app_info['vcode']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Author: {app_info['author']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Description: {app_info['description']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Category: {app_info['category']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Tags: {app_info['tags']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Min Python Version: {app_info['min_python_version']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target Python Version: {app_info['target_python_version']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Compatible OS: {app_info['compatible_os']}{Style.RESET_ALL}")
        print("=" * 30)
        input(f"{Fore.CYAN}(Press Enter to Continue.){Style.RESET_ALL}")
        pack_apps(app_info["name"], app_info["version"])

def find_app_files():
    app_files_path = os.path.abspath("app_files")
    if not os.path.exists(app_files_path):
        try:
            os.mkdir(app_files_path)
            print(f"{Fore.GREEN}'app_files' folder created.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: Failed to create 'app_files' folder: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)

    print("=" * 30)
    print(f"{Fore.YELLOW}Please put your app files in the 'app_files' folder.{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Path: {app_files_path}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1. main.py{Style.RESET_ALL}")
    print(f"{Fore.CYAN}2. info.json{Style.RESET_ALL}")
    print(f"{Fore.CYAN}3. requirements.txt{Style.RESET_ALL}")
    print("=" * 30)
    input(f"{Fore.LIGHTGREEN_EX}(Press Enter to Continue.){Style.RESET_ALL}")
    check_app_files()

def main():
    print("=" * 40)
    print(f"{Fore.LIGHTGREEN_EX}Welcome to the PY OS Improved Application Package Maker.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Please read the application development standard before proceeding.{Style.RESET_ALL}")
    input(f"{Fore.LIGHTGREEN_EX}(Press Enter to Continue.){Style.RESET_ALL}")
    find_app_files()

if __name__ == "__main__":
    main()
