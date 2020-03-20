from src.interface.project_file_interface import ProjectFI

import os
import sys

def test__new_proj():
    proj = ProjectFI(path="tests/", name="ProjectName")

    try:
        assert proj.path == "tests/ProjectName" or proj.path == "tests\\ProjectName"
        assert proj.project != {}


        assert proj.get_key("hola!") == 0
        assert proj.get_key("你好！") == 1
        assert proj.get_key("hola!") == None  # cannot get multiple keys with the same name

        assert proj.valid_key(0)
        assert proj.valid_key(1)
        assert not proj.valid_key(2)

        proj.change_name(0, "hello!")
        assert proj.valid_key(0)
    except AssertionError as e:
        raise e
    finally:

        # users manually deletes/moves projects for safety reasons
        os.rmdir(os.path.join("tests/ProjectName", ProjectFI.dir_deploy))
        os.rmdir(os.path.join("tests/ProjectName", ProjectFI.dir_model))
        os.rmdir(os.path.join("tests/ProjectName", ProjectFI.dir_test))
        os.rmdir(os.path.join("tests/ProjectName", ProjectFI.dir_train))
        os.rmdir(os.path.join("tests/ProjectName", ProjectFI.dir_validator))
        os.remove(os.path.join("tests/ProjectName", ProjectFI.prj_file))
        os.rmdir("tests/ProjectName")


def test__load_empty_proj():
    # setup
    proj_new = ProjectFI(path="tests/", name="ProjectName2")

    assert proj_new.path == "tests/ProjectName2"
    assert proj_new.project != {}

    del proj_new

    # ==== main ====
    proj = ProjectFI.load("tests/ProjectName2/project.yaml")

    assert proj.path == "tests/ProjectName2" or proj.path == "tests\\ProjectName2"
    assert proj.project != {}


    assert proj.get_key("hola!") == 0
    assert proj.get_key("你好！") == 1
    assert proj.get_key("hola!") == None  # cannot get multiple keys with the same name

    assert proj.valid_key(0)
    assert proj.valid_key(1)
    assert not proj.valid_key(2)

    proj.change_name(0, "hello!")
    assert proj.valid_key(0)

    os.rmdir(os.path.join("tests/ProjectName2", ProjectFI.dir_deploy))
    os.rmdir(os.path.join("tests/ProjectName2", ProjectFI.dir_model))
    os.rmdir(os.path.join("tests/ProjectName2", ProjectFI.dir_test))
    os.rmdir(os.path.join("tests/ProjectName2", ProjectFI.dir_train))
    os.rmdir(os.path.join("tests/ProjectName2", ProjectFI.dir_validator))
    os.remove(os.path.join("tests/ProjectName2", ProjectFI.prj_file))
    os.rmdir("tests/ProjectName2")


def test__multi_instance_proj():
    pass

