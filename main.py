import argparse
import json
import logging

from src.super6_auto_picker.client import Super6Client
from src.super6_auto_picker.utils.file_utils import read_predictions
from src.super6_auto_picker.make_prediction import main as make_predictions_main
from src.super6_auto_picker.get_odds import main as get_odds_main

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    parser = argparse.ArgumentParser(description='Super6 Auto Picker')
    parser.add_argument('--optimise', action='store_true', help='Optimise predictions even if already submitted')
    args = parser.parse_args()

    client = Super6Client()
    try:
        client.login()
        logging.info("Login attempted. Check login_result.png for results.")

        if args.optimise:
            logging.info("Optimise flag detected. Running intelligent_pick_and_submit...")

            # Get odds and make predictions
            get_odds_main()
            make_predictions_main()

            # Submit predictions
            client.intelligent_pick_and_submit()
        else:
            result = client.auto_pick_and_submit()
            if result == 'already_submitted':
                logging.info("You have already submitted your prediction. See already_submitted.png for details.")
            else:
                logging.info("Auto-pick and submission attempted. Check submission_result.png for results.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
