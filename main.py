import argparse

from src.super6_auto_picker.client import Super6Client

def main():
    parser = argparse.ArgumentParser(description='Super6 Auto Picker')
    parser.add_argument('--optimise', action='store_true', help='Optimise predictions even if already submitted')
    args = parser.parse_args()

    client = Super6Client()
    try:
        client.login()
        print("Login attempted. Check login_result.png for results.")

        if args.optimise:
            # Implement logic to edit predictions
            pass
        else:
            result = client.auto_pick_and_submit()
            if result == 'already_submitted':
                print("You have already submitted your prediction. See already_submitted.png for details.")
            else:
                print("Auto-pick and submission attempted. Check submission_result.png for results.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
