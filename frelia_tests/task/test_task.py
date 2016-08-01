import frelia.task


def test_decorate():
    decorator = frelia.task.Task.decorate('craft', ['uni'])
    func = lambda uni: 'craft'
    got = decorator(func)
    assert got.target == 'craft'
    assert got.task_func == func
    assert got.deps == ['uni']
