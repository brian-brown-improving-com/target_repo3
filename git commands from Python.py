#source_repo_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\source\\source_repo\\"
#source_folder_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\source\\source_repo\\src"
#target_repo_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\target\\target_repo\\"
#target_folder_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\target\\target_repo\\src"

source_repo_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\source\\source_repo\\"
source_folder_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\source\\source_repo\\src"
target_repo_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\target\\"
target_folder_path = "C:\\Users\\brian\\Documents\\git_sync_part_2\\target\\target_repo\\src"

import os
import subprocess

def issue_git_command(git_command_parts, verbose=False):
    # takes a list of keywords that would form a git command (not a single string, although I can't explain why) and issues that command
    returncode = -1
    if len(git_command_parts) < 2:
        print(f"Parameter git_command_parts is expected to be a list of keywords that would form a git command (hint: first item of list is likely 'git').")
        returncode == 0 # False
    if verbose:
        git_command = " ".join(git_command_parts)
        print(f"Attempting command '{git_command}'...")
    process = subprocess.Popen(git_command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    returncode = process.returncode
    if returncode != 0:
        print(f"...git command '{git_command}' failed.")
        print(stderr.decode())
    else:
        if verbose:
            print(f"...git command '{git_command}' succeeded.")
            print(stdout.decode())
    return returncode == 0

def validate_input(path, confirm_path_is_repo=False, attempt_git_pull=False, verbose=False):
    # confirms the existence of a folder, confirms it's a repo (via git status) if desired, and (also if desired) commits a git pull to ensure code is up-to-date
    validation = False
    path_exists = os.path.exists(path)
    if not path_exists:
        print(f"The path '{path}' was not found.  It should be fully-qualified path.")
        return validation
    if not confirm_path_is_repo:
        validation = True
        return validation
    os.chdir(path)
    validation = issue_git_command(['git', 'status'], verbose)
    if not validation:
        print(f"git status failed for path '{path}'")
        return validation
    if attempt_git_pull:
        print(f"Attempting git pull for '{path}'...")
        validation = issue_git_command(['git', 'pull'], verbose)
        if validation:
            print("... git pull succeeded")
        else:
            print("... git pull failed")
    else:
        print(f"The value for 'attempt_git_pull' was False, so git pull was not attempted for repo '{path}'.")
    return validation

def validate_inputs(
        repo_path,
        folder_path,
        attempt_git_pull=False,
        target_branch_name=None):
    validation = False
    validated_folder = validate_input(folder_path, confirm_path_is_repo=False)
    if not validated_folder:
        print(f"Folder-exists validation failed for '{folder_path}'; aborting sync.")
        return validation
    validated_folder_in_repo = folder_path[:len(repo_path)] == repo_path
    if not validated_folder_in_repo:
        print(f"Folder-in-repo validation failed for repo '{repo_path}' and folder '{folder_path}'; aborting sync.")
        return validation
    validated_repo = validate_input(repo_path, confirm_path_is_repo=True, attempt_git_pull=attempt_git_pull)
    if not validated_repo:
        print(f"Repo-is-actually-repo validation failed for repo '{repo_path}'; aborting sync.")
        return validation
    validation = True
    return validation

def sync_repo_folder(
        source_repo_path,
        source_folder_path,
        target_repo_path,
        target_folder_path,
        attempt_git_pull=False, # if False then there won't be any pull
        target_branch_name=None # if None then there won't be any push
        ):
    # validates sources (optionally including a git pull), transfers files between source folders, and optionally attempts a git push

    import shutil

    sync_success = False

    validation = validate_inputs(
        repo_path=source_repo_path,
        folder_path=source_folder_path,
        attempt_git_pull=attempt_git_pull
        )
    if validation:
        validation = validate_inputs(
            repo_path=target_repo_path,
            folder_path=target_folder_path,
            attempt_git_pull=attempt_git_pull,
            target_branch_name=target_branch_name)
    if not validation:
        print("Cannot validate inputs; aborting repo folder sync.")
        return sync_success

    print(f"Attempting file transfer from '{source_repo_path}' to '{target_folder_path}'...")
    shutil.copytree(src=source_folder_path, dst=target_folder_path, dirs_exist_ok=True)
    print(f"... file transfer complete.")

    if target_branch_name:
        print(f"Attempting git push to branch '{target_branch_name}'...")
        sync_success = issue_git_command(['git', 'push', 'origin', target_branch_name], verbose=True)
        if sync_success:
            print(f"... git push succeeded.")
        else:
            print(f"... git push failed.")
    else:
        print("There was no value for 'target_branch_name', so git push was not attempted.")
        sync_success = True

    return sync_success

#sync_repo_folder(source_repo_path, source_folder_path, target_repo_path, target_folder_path, attempt_git_pull=True, target_branch_name="main")
sync_repo_folder(source_repo_path, source_folder_path, target_repo_path, target_folder_path, attempt_git_pull=True)