from pathlib import Path as BasePath
from shutil import copytree, copy2 as copy

# Set path type and copy of path
PathType = type(BasePath())
PathCopy = 'project.core.path.Path'


class Path(PathType):
    def copy(self, destination: BasePath) -> None:
        """
        Copy path
        :param destination:
        :return:
        """
        # Check, is folder
        if self.is_dir():
            # If it is, use shutil copytree
            func = copytree
            destination /= self.name
        else:
            # Else use copy (copy2)
            func = copy

        src = str(self.resolve())
        dest = str(destination.resolve())

        func(src, dest)

    def clone(self) -> PathCopy:
        """
        Clone path
        :return:
        """
        return type(self)(self)
