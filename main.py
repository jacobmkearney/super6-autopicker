from src.super6_auto_picker.client import Super6Client

def main():
    client = Super6Client()
    try:
        client.login()
        print("Login attempted. Check login_result.png for results.")
        result = client.auto_pick_and_submit()
        if result == 'already_submitted':
            print("You have already submitted your prediction. See already_submitted.png for details.")
        else:
            print("Auto-pick and submission attempted. Check submission_result.png for results.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
