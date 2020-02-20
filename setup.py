try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

import npzheader

setup(name="NpzHeader",
      version=npzheader.__version__,
      author="ok97465",
      author_email='ok97465@gmail.com',
      url='https://github.com/ok97465/npzheader',
      description='Viewer header of numpy binary format file',
      keywords=['npz'],
      packages=['npzheader'],
      license='MIT',
      long_description=open('README.md').read(),
      install_requires=['qtpy', 'qdarkstyle', 'numpy', 'scipy'],
      entry_points={
          'console_scripts': ['npz-viewer=npzheader.viewer:run'],
      }
)
