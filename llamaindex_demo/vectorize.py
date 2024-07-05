import argparse

from utils.data import traverse
from utils.vector import save_vectors


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', type=str, help="directory of the workspace to be vectorized", default='.')
    parser.add_argument('--lines_per_chunk', type=int, help="chunk lines when splitting", default=40)
    parser.add_argument('--lines_overlap', type=int, help="chunk lines overlap when splitting", default=15)
    parser.add_argument("--max_chars", type=int, help="maximum number of characters in a chunk", default=1500)
    parser.add_argument('--output_path', type=str, help="path to save the vectors", default='vectors')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    files = traverse(args.workspace)
    save_vectors(files, args)
