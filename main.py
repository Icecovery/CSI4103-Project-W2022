import os

def export_env_var():
    os.environ["PAPER_HEIGHT"] = "279"
    os.environ["PAPER_WIDTH"] = "216"

def main():
    export_env_var()
    print(os.environ)

if __name__ == "__main__":
    main()
