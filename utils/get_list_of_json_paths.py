import os


def get_list_of_json_paths(path_ini, remove_extension=False):
    paths = []

    # If the path is a file, put only this file in the list
    if os.path.isfile(path_ini):
        if path_ini.endswith(".json"):
            paths.append(path_ini)

    # If the path is a directory, create a list of all the json files in the
    # directory tree
    elif os.path.isdir(path_ini):
        for root, dirs, files in os.walk(path_ini):
            for name in files:
                if name.endswith(".json"):
                    paths.append(os.path.join(root, name))

    if len(paths) == 0:
        print("No .json files found in the specified path.")
        quit()

    # Remove .json extension
    if remove_extension:
        paths = [os.path.splitext(f)[0] for f in paths]

    return paths
