"""
Post processing tools
"""
import os

import numpy as np

def extrac4dir(dir_path, search):
    """
    Extrar the epsilon, mean free path, total time and efficienci of all file in some directory.

    Parameters
    ----------
    dir_path : str
      Path to the directory with the outputs files.
    search : list
      List with the number of acceptor to search only this effienci.

    Return
    ------
    out : matrix
    """
    dirs = os.listdir(path=dir_path)
    out = np.zeros((len(dirs), len(search) + 3))

    for num_file, file_path in enumerate(dirs):
        with open(os.path.join(dir_path, file_path), 'r') as file:
            cnt = 0

            while True:
                line = file.readline()
                if 'path' in line:
                    line_split = line.split()
                    out[num_file][0] = float(line_split[3])
                elif 'Epsilon' in line:
                    line_split = line.split()
                    out[num_file][1] = float(line_split[1])
                elif 'Total time =' in line:
                    line_split = line.split()
                    out[num_file][2] = float(line_split[3])
                elif 'Nº acceptors' in line:
                    line = file.readline()
                    while True:
                        line = file.readline()
                        # Remove all spaces
                        line_without_space = ''.join(line.split())
                        line_split = line_without_space.split('|')

                        # End of file
                        if '+--------------' in line:
                            break

                        if line_split[1] == str(search[cnt]):
                            out[num_file][cnt + 3] = float(line_split[4])
                            cnt += 1

                    break

                if '' == line:
                    break

    return out


def diference2(efficience, eff_matrix):
    """
    Squared difference between the simulated efficiencies (matrix) and a given.

    Parameters
    ----------
    efficience : array_like
      Efficience to compare
    eff_matrix : matrix
      Matrix give for extrac4dir.

    Return
    ------
    """
    diff_matrix = np.zeros((eff_matrix.shape[0], eff_matrix.shape[1] + 1))

    diff_matrix[:, :3] = eff_matrix[:, :3]
    diff_matrix[:, 4:] = eff_matrix[:, 3:]

    # Diff
    for i in range(diff_matrix.shape[0]):
        diff_matrix[i][3] = sum((diff_matrix[i][4:] - efficience)**2)

    return diff_matrix
