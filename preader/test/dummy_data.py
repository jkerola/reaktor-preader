class RealDummy(object):
    '''Test dummy with real data'''
    name = 'real.file'
    data = b'''Package: test-package
Depends: moot, another-test | third-test | fake
Description: Test description
 More test description
 End test description
Homepage: None

Package: another-test
Depends: test-package | fake | third-test
Description: description of said package
 more descriptive text.
Homepage: None

Package: third-test
Depends: another-test, moot | test-package
Description: No More
Homepage: None

ASDASDASDASD'''


class FakeDummy(object):
    '''Fake dummy object'''
    name = 'fake.file'
    data = b'fake data'
