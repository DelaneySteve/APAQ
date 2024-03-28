import sys
from argparse import ArgumentParser

from src.model.model import Model
from src.push_pull_models.push_model import upload_multipart_model

SAVE_MODEL_PATH = './model/rf_model.pickle'
DEFAULT_DATA_PATH = './data/airports_augmented_dataset.json'

def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Read file from Command line.')
    parser.add_argument(
        '--airports_augmented_dataset',
        nargs = '?',
        const = DEFAULT_DATA_PATH,
        required=False,
        type=str,
        default = DEFAULT_DATA_PATH,
        help='file path for information about each airport',
    )
    return parser


def main(args: list[str]) -> None:
    parser = setup_parser()
    args = parser.parse_args(args)
    rf_model = Model()
    rf_model.train(args.airports_augmented_dataset)
    rf_model.save_trained_model(SAVE_MODEL_PATH)
    model_id = upload_multipart_model('rf_model.pickle', SAVE_MODEL_PATH)
    print(model_id)
if __name__ == '__main__':
    main(sys.argv[1:])
