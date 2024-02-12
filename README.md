# APAQ (AirPort Air Quality) Predictor
The AirPort Air Quality (APAQ) Predictor is an API tool that can be used to predict the air quality (particulate matter with diameter less than 10 microns, PM10) in the area near an airport from an aerial image (synthetic or real) of the airport alone.

## Quick Setup
1. Create a virtual environment by executing `make` in the root.
2. Activate the virtual environment by executing `. venv/Scripts/activate` (for Windows) or `. venv/bin/activate` (for Mac/Linux) also in the root directory.
3. Run the program by executing `make run` in the root directory.


## Pre-commit hooks
We use pre-commit hooks and `pre-commit` will be installed when you run `pip install -r requirements-dev.txt`.
Run `pre-commit install` to ensure pre-commit hook run whenever you make a commit. Check that you are able to run all hooks locally by running `pre-commit run --all-files`

## Train a Random Forest Model
1. Execute: `python -m src.model.main --airports_augmented_dataset DATA_FILE_PATH` where DATA_FILE_PATH is the local path to the training dataset 
2. The trained model will save as a pickle file automatically to src/model/rf_model.pickle.

