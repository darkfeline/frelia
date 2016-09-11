import pytest

import mir.frelia.task


def test_happy_path(craft_task, uni_task):
    manager = mir.frelia.task.TaskManager()
    manager.add(craft_task)
    manager.add(uni_task)
    got = manager.run()
    assert got == 'uni craft'


def test_run_no_tasks():
    manager = mir.frelia.task.TaskManager()
    got = manager.run()
    assert got is None


def test_add_duplicate_task(uni_task):
    manager = mir.frelia.task.TaskManager()
    manager.add(uni_task)
    with pytest.raises(mir.frelia.task.DuplicateTargetError) as excinfo:
        manager.add(uni_task)
    assert excinfo.value.target == 'uni'


def test_missing_dependency(craft_task):
    manager = mir.frelia.task.TaskManager()
    manager.add(craft_task)
    with pytest.raises(mir.frelia.task.MissingDependenciesError) as excinfo:
        manager.run()
    assert excinfo.value.deps == {'uni'}


def test_dependency_cycle(craft_task, bad_uni_task):
    manager = mir.frelia.task.TaskManager()
    manager.add(craft_task)
    manager.add(bad_uni_task)
    with pytest.raises(mir.frelia.task.DependencyCycleError):
        manager.run()
