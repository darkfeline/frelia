"""Simple task and dependency management.

Tasks are functions that provide a target and optionally has dependencies.
When running tasks, the tasks will be topologically sorted and then called.
A task with dependencies will be called after its dependencies and will be
passed the results of their calls.

"""

import inspect

import networkx as nx


class TaskManager:

    def __init__(self):
        self.tasks = {}
        self.results = {}

    def add(self, task):
        """Add task to be run."""
        if task.target in self.tasks:
            raise DuplicateTargetError(task.target)
        self.tasks[task.target] = task

    def run(self):
        """Run tasks."""
        self._check_deps()
        graph = self._build_graph()
        targets = self._topological_sort(graph)
        target = None
        for target in targets:
            task = self.tasks[target]
            self._run_task(task)
        return self.results.get(target, None)

    def _check_deps(self):
        targets = set(self.tasks)
        for task in self.tasks.values():
            missing = set(task.deps) - targets
            if missing:
                raise MissingDependenciesError(missing)

    def _build_graph(self):
        """Build graph of tasks."""
        graph = nx.DiGraph()
        for target, task in self.tasks.items():
            graph.add_node(target)
            graph.add_edges_from((dep, target) for dep in task.deps)
        return graph

    @staticmethod
    def _topological_sort(graph):
        try:
            return nx.topological_sort(graph)
        except nx.NetworkXUnfeasible as e:
            raise DependencyCycleError from e

    def _run_task(self, task):
        """Run a task.

        Call the task function with the results of its dependencies and store
        the task's result.

        """
        results = self.results
        args = [results[dep] for dep in task.deps]
        result = task.task_func(*args)
        results[task.target] = result


class Task:

    """A task to run.

    target is a string.  deps is a sequence of strings.

    """

    def __init__(self, target, task_func, deps=()):
        self.target = target
        self.task_func = task_func
        self.deps = deps

    def __repr__(self):
        return '<{cls} at 0x{id:x}: {target!r}, {deps!r}>'.format(
            cls=type(self).__name__,
            id=id(self),
            target=self.target,
            deps=self.deps)

    @classmethod
    def decorate(cls, func):
        """Create a Task by decorating a function.

        deps is a sequence of Tasks.

        """
        signature = inspect.signature(func)
        return cls(
            func.__name__,
            func,
            [param.name for param in signature.parameters.values()])


class DuplicateTargetError(ValueError):

    def __init__(self, target):
        self.target = target
        super().__init__(target)


class MissingDependenciesError(Exception):

    def __init__(self, deps):
        self.deps = deps
        super().__init__(deps)


class DependencyCycleError(Exception): pass
