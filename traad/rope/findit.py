from eagertools import emap
import rope.contrib.findit

import traad.trace
from traad.rope.validate import validate


def location_to_tuple(location):
    return (location.resource.path,
            location.region,
            location.offset,
            location.unsure,
            location.lineno)


def _find_locations(project, func, path, offset):
    """Common implementation for occurrences and
    implementations.

    """
    path = project.to_relative_path(path)
    results = func(
        project.proj,
        project.proj.get_resource(path),
        offset)
    return emap(location_to_tuple, results)


@traad.trace.trace
@validate
def find_occurrences(project, offset, path):
    """Find occurrences of a symbol at a point in a file.

    ``path`` may be absolute or relative. If ``path`` is relative,
    then it must to be relative to the root of the project.

    Args:
      project: The traad Project object.
      offset: The offset into ``path`` of the symbol.
      path: The path to the resource containing the symbol to
        search for.

    Returns: A sequence of tuples of the form (path, (region-start,
      region-stop), offset, unsure, lineno).
    """

    return _find_locations(
        project,
        rope.contrib.findit.find_occurrences,
        path,
        offset)


@traad.trace.trace
@validate
def find_implementations(project, offset, path):
    """Find the places a given method is overridden.

    ``path`` may be absolute or relative. If ``path`` is relative,
    then it must to be relative to the root of the project.

    Args:
      project: The traad Project object.
      offset: The offset into ``path`` of the method name.
      path: The path to the resource containing the method name to
        search for.

    Returns: A sequence of tuples of the form (path, (region-start,
      region-stop), offset, unsure, lineno).
    """

    return _find_locations(
        project,
        rope.contrib.findit.find_implementations,
        path,
        offset)


@traad.trace.trace
@validate
def find_definition(self, code, offset, path):
    """Find the definition location of a symbol.

    ``path`` may be absolute or relative. If ``path`` is relative,
    then it must to be relative to the root of the project.

    Args:
      code: The source code containing the method symbol.
      offset: The offset into ``code`` of the symbol.
      path: The path to the resource containing ``code``.

    Returns: A tuple of the form (path, (region-start,
      region-stop), offset, unsure, lineno).

    """

    path = self._to_relative_path(path)
    return location_to_tuple(
        rope.contrib.findit.find_definition(
            self.proj,
            code,
            offset,
            self.proj.get_resource(path)))
