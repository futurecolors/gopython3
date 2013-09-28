from pip.req import InstallRequirement


def parse(requirements_string):
    deps = []
    for line in requirements_string.split('\n'):
        requirement = InstallRequirement.from_line(line)
        for version in requirement.absolute_versions:
            deps.append((requirement.name, version))
            break
        else:
            deps.append((requirement.name, None))
    return deps
