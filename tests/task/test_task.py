import mir.frelia.task


def test_decorate():
    def craft(uni): pass
    got = mir.frelia.task.Task.decorate(craft)
    assert got.target == 'craft'
    assert got.task_func == craft
    assert got.deps == ['uni']
