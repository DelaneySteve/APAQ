from argparse import ArgumentParser
from research.make_model import MakeModel

parser = ArgumentParser(description="Read file from Command line.")
parser.add_argument("--aug-airports-load-file", required=True, 
                    type=str, help="file path for information about each airport")
parser.add_argument("--model_dump_dir", required=True, 
                    type=str, help="path to directory to store model")

args = parser.parse_args()

AUG_AIRPORTS_LOAD_PATH_FILE = args.aug_airports_load_file # augmented airports file
MODEL_DUMP_PATH_DIR = args.model_dump_dir #path to dump model

RF_model = MakeModel()
RF_model.train_fit(AUG_AIRPORTS_LOAD_PATH_FILE)
RF_model.save_model(MODEL_DUMP_PATH_DIR)
