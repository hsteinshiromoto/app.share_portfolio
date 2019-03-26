import git #pip3 install gitpython
import os
import warnings
import glob

def get_file(path, pattern=None, extension=None, latest=True):
    """
    Find (latest) files with a pattern

    :param path: str
    :param pattern: str., optional
    :param extension: str., optionals
    :param latest: bool., optional
    :return: str or list
    """

    if not extension:
        extension = ""

    list_file_names = glob.glob("{0}/*{1}".format(path, extension))

    if list_file_names == []:
        msg = "Expected files in {}. Found none.".format(path)
        warnings.warn(msg)
        return None

    elif pattern:
        list_pattern = [file_name for file_name in
                        list_file_names if re.search(pattern, file_name)]

        list_file_names = list_pattern

        if list_file_names == []:
            msg = "Expected files with pattern {0} in {1}. Found none."\
                .format(pattern, path)
            warnings.warn(msg)
            return None

    if latest == True:
        output = os.path.basename(max(list_file_names,
                                      key=os.path.getctime))

    else:
        output = [os.path.basename(item) for item in list_file_names]

    print("Found file(s) {}.".format(output))

    return output


def get_paths():
    """
    Generates the paths of a repository based on cookie cutter data science

    :return: dict
    """

    # Get repo name
    git_repo = git.Repo(__file__, search_parent_directories=True)
    repo = git_repo.git.rev_parse("--show-toplevel")

    paths = {"repo": repo, "base":{}, "src":{}, "data":{}, "app":{}}

    for base_dir in ["data", "notebooks", "src", "model", "logs", "app"]:

        paths["base"][base_dir] = os.path.join(repo, base_dir)
        test = paths["base"][base_dir].split(base_dir)[-1]
        assert len(test) == 0

    for src_dir in ["conf", "data", "notebooks", "tests", "utils",
                    "visualize", "conf", "model"]:

        src_base_dir = paths.get("base").get("src")
        paths["src"][src_dir] = os.path.join(src_base_dir, src_dir)
        test = paths["src"][src_dir].split(src_dir)[-1]
        assert len(test) == 0

    for data_dir in ["raw", "interim", "processed"]:

        data_base_dir = paths.get("base").get("data")
        paths["data"][data_dir] = os.path.join(data_base_dir, data_dir)
        test = paths["data"][data_dir].split(data_dir)[-1]
        assert len(test) == 0

    for app_dir in ["templates", "static"]:
        app_base_dir = paths.get("base").get("app")
        paths["app"][app_dir] = os.path.join(app_base_dir, app_dir)

    return paths
