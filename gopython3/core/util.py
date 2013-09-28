from pip.req import InstallRequirement


def parse_requirements(requirements_string):
    """ Convert requirements.txt contents into machine-friendly form

        Returns iterable like this:
            (('package_name', 'X.Y.Z'), ...)
    """
    deps = []
    for line in requirements_string.split('\n'):
        requirement = InstallRequirement.from_line(line)
        for version in requirement.absolute_versions:
            deps.append((requirement.name, version))
            break
        else:
            deps.append((requirement.name, None))
    return deps
