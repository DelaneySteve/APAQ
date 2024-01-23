from model.model import Model

from argparse import ArgumentParser, Namespace


def get_args() -> Namespace:
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
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    RF_model = Model()
    RF_model.train(args.aug_airports_load_file)
    RF_model.save_trained_model(args.model_dump_dir)
