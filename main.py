from src.super6_auto_picker.client import Super6Client

def main():
    client = Super6Client()
    try:
        client.login()
        print("Login attempted. Check browser output or logs for results.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
