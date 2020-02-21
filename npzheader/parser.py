"""Parse numpy binary format."""
# ------------ Import
# Standard library imports
import os.path as osp
import zipfile
from dataclasses import dataclass
from typing import List, Union, Dict


# Third party imports
import numpy as np
from scipy.io import whosmat, loadmat


# ----------- function
@dataclass
class ItemInfo:
    shape: tuple
    dtype: str
    value: Union[int, float, complex, str, None]


def get_headers_of_numpy(path: str) -> Dict[str, ItemInfo]:
    """Get header info of numpy binary format."""
    ret = {}

    if path is None:
        raise FileNotFoundError

    if path.endswith(".npy"):
        ret = parse_npy(path)
    elif path.endswith(".npz"):
        ret = parse_npz(path)
    elif path.endswith(".mat"):
        ret = parse_mat(path)

    return ret


def parse_npy(path: str) -> Dict[str, ItemInfo]:
    """Parse npy file."""
    read_magic = np.lib.format.read_magic
    read_header = np.lib.format._read_array_header

    ret = {}

    if path.endswith(".npy"):
        with open(path, 'rb') as fp:
            ver = read_magic(fp)
            shape, _, dtype = read_header(fp, ver)

            name = osp.basename(path)
            ret[name[:-4]] = ItemInfo(shape, str(dtype), None)

    return ret


def parse_npz(path: str) -> Dict[str, ItemInfo]:
    """Parse npz file."""
    read_magic = np.lib.format.read_magic
    read_header = np.lib.format._read_array_header
    read_array = np.lib.format.read_array

    ret = {}

    if path.endswith(".npz"):
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if not name.endswith('.npy'):
                    continue

                fp_npy = archive.open(name)
                ver = read_magic(fp_npy)
                shape, _, dtype = read_header(fp_npy, ver)

                value = None
                prefix_available = ('int', 'float', 'complex', '<U', '>U')
                if not shape and str(dtype).startswith(prefix_available):
                    fp_npy.seek(0, 0)
                    value = read_array(fp_npy).item()

                ret[name[:-4]] = ItemInfo(shape, str(dtype), value)

    return ret


def parse_mat(path: str) -> Dict[str, ItemInfo]:
    """Parse mat file."""
    ret = {}

    scalar_item_list = []
    if path.endswith(".mat"):
        mat_infos = whosmat(path)

        for name, shape, dtype in mat_infos:
            ret[name] = ItemInfo(shape, dtype, None)

            if shape == (1, 1) or shape == (1,):
                scalar_item_list.append(name)

        values = loadmat(path, variable_names=scalar_item_list)

        for name in scalar_item_list:
            ret[name].value = values[name].item()

    return ret
