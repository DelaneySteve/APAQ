import sys
from argparse import ArgumentParser

from src.model.model import Model

SAVE_MODEL_PATH = 'src/model/model_new.pickle'


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Read file from Command line.')
    parser.add_argument(
        '--aug-airports-load-file',
        required=True,
        type=str,
        help='file path for information about each airport',
    )
    return parser


def main(args: list[str]) -> None:
    parser = setup_parser()
    args = parser.parse_args(args)
    rf_model = Model()
    rf_model.train(args.aug_airports_load_file)
    rf_model.save_trained_model(SAVE_MODEL_PATH)


if __name__ == '__main__':
    main(sys.argv[1:])
