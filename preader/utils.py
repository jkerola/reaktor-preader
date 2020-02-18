import re


def read_file(file):
    '''Format and return file data in a list of dictionaries for
    database purposes. Strips empty spaces and version numbers from select data.'''
    packages_list = []
    package = {}
    description = ''
    with open(file) as packages_file:
        for line in packages_file:
            if line.startswith('Package'):
                formatted_line = line.lstrip('Package:').rstrip('\n')
                formatted_line = re.sub(r'\(.*?\)', '', formatted_line)
                package['name'] = formatted_line.strip()
            if line.startswith('Depends'):
                formatted_line = line.lstrip('Depends:').rstrip('\n')
                formatted_line = re.sub(r'\(.*?\)', '', formatted_line)
                package['depends'] = formatted_line.strip()
            if line.startswith('Description') or line.startswith(' '):
                description += line.lstrip('Description:').lstrip()
            if line.startswith('\n'):
                package['description'] = description.replace('\n', ' ')
                packages_list.append(package)
                package = {}
                description = ''
        return packages_file.name, packages_list


def filter_duplicate_names(package_list):
    '''Removes duplicate packages from the given list, returns a filtered list'''
    filtered_packages = []
    duplicate_package_names = []
    for package in package_list:
        if package.name not in duplicate_package_names:
            duplicate_package_names.append(package.name)
            filtered_packages.append(package)
    return filtered_packages

if __name__ == "__main__":
    name, packages = read_file('status.raspberry')
    print(packages)
