import re

def read_file(file):
    '''Read, format and return package file name and data in a dictionary'''
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
            if line.startswith('Original-Maintainer'):
                package['description'] = description.replace('\n', ' ')
                packages_list.append(package)
                package = {}
                description = ''
        return packages_file.name, packages_list


if __name__ == "__main__":
    name, packages = read_file('status.real')
    print(packages)
