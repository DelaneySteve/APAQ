import sys
from model.model import Model

from argparse import ArgumentParser


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Read file from Command line.")
    parser.add_argument(
        "--aug-airports-load-file",
        required=True,
        type=str,
        help="file path for information about each airport",
    )
    parser.add_argument(
        "--model_dump_dir",
        required=True,
        type=str,
        help="path to directory to store model",
    )
    return parser


def main(args: list[str]) -> None:
    parser = setup_parser()
    args = parser.parse_args(args)
    rf_model = Model()
    rf_model.train(args.aug_airports_load_file)
    rf_model.save_trained_model(args.model_dump_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
