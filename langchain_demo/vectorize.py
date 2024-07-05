"""
Vectorize your local project
"""

import argparse

from utils.data import traverse
from utils.vector import vectorize


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', type=str, help="directory of the workspace to be vectorized", default='.')
    parser.add_argument('--chunk_size', type=int, help="chunk size when splitting", default=512)
    parser.add_argument('--overlap_size', type=int, help="chunk overlap when splitting", default=32)
    parser.add_argument('--batch_size', type=int, help="embedding batch size", default=16)
    parser.add_argument('--output_path', type=str, help="path to save the vectors", default='vectors')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    files = traverse(args.workspace)
    vectorize(files, args)
