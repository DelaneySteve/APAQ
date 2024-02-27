import sys
from argparse import ArgumentParser

from src.model.model import Model

SAVE_MODEL_PATH = './model/rf_model.pickle'


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Read file from Command line.')
    parser.add_argument(
        '--airports_augmented_dataset',
        required=True,
        type=str,
        help='file path for information about each airport',
    )
    return parser


def main(args: list[str]) -> None:
    parser = setup_parser()
    args = parser.parse_args(args)
    rf_model = Model()
    rf_model.train(args.airports_augmented_dataset)
    rf_model.save_trained_model(SAVE_MODEL_PATH)


if __name__ == '__main__':
    main(sys.argv[1:])
