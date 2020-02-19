"""Parse numpy binary format."""
# ------------ Import
# Standard library imports
import os.path as osp
import zipfile
from typing import List, Union

# Third party imports
import numpy as np


# ----------- function
def get_headers_of_numpy(path: str) -> (List[str], List[tuple], List[str],
                                        List[Union[int, float, complex]]):
    """Get header info of numpy binary format."""
    read_magic = np.lib.format.read_magic
    read_header = np.lib.format._read_array_header
    read_array = np.lib.format.read_array

    name_list = []
    shape_list = []
    dtype_list = []
    value_list = []

    try:
        if path.endswith(".npy"):
            with open(path, 'rb') as fp:
                ver = read_magic(fp)
                shape, _, dtype = read_header(fp, ver)

                name = osp.basename(path)
                name_list.append(name[:-4])
                shape_list.append(shape)
                dtype_list.append(str(dtype))
                value_list.append(None)

        elif path.endswith(".npz"):
            with zipfile.ZipFile(path) as archive:
                for name in archive.namelist():
                    if not name.endswith('.npy'):
                        continue

                    fp_npy = archive.open(name)
                    ver = read_magic(fp_npy)
                    shape, _, dtype = read_header(fp_npy, ver)

                    name_list.append(name[:-4])
                    shape_list.append(shape)
                    dtype_list.append(str(dtype))

                    value = None
                    if (not shape
                            and str(dtype).startswith(('int', 'float',
                                                       'complex'))):
                        fp_npy.seek(0, 0)
                        value = read_array(fp_npy).item()
                    value_list.append(value)

    except (zipfile.BadZipFile, ValueError, FileNotFoundError):
        pass

    return name_list, shape_list, dtype_list, value_list
