import os

def export_env_var():
    os.environ["CSV_DIR"] = "Temp"
    os.environ["PATH_CSV"] = "path.csv"

def main():
    export_env_var()

if __name__ == "__main__":
    main()
