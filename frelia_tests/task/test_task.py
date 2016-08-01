import frelia.task


def test_decorate(uni_task):
    decorator = frelia.task.Task.decorate(uni_task)
    def craft(uni): pass
    func = craft
    got = decorator(func)
    assert got.target == 'craft'
    assert got.task_func == func
    assert got.deps == ['uni']
