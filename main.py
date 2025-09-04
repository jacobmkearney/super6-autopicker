import argparse
import json
import logging

from src.super6_auto_picker.client import Super6Client
from src.super6_auto_picker.utils.file_utils import read_predictions
from src.super6_auto_picker.make_prediction import main as make_predictions_main
from src.super6_auto_picker.get_odds import main as get_odds_main


def main():
    parser = argparse.ArgumentParser(description='Super6 Auto Picker')
    parser.add_argument('--optimise', action='store_true', help='Optimise predictions even if already submitted')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging and screenshots')
    args = parser.parse_args()

    # Configure logging level based on debug flag
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)

    client = Super6Client(debug=args.debug, headless=(not args.debug))
    try:
        client.login()
        logger.info("logged into super 6")

        if args.optimise:
            logger.info("optimising")

            # Get odds and make predictions
            get_odds_main()
            make_predictions_main()

            # Submit predictions
            client.intelligent_pick_and_submit()
        else:
            result = client.auto_pick_and_submit()
            if result == 'already_submitted':
                logger.info("already submitted scores")
    finally:
        client.close()

if __name__ == "__main__":
    main()
