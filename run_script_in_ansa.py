import ansa
from ansa import script

def main():
    SCRIPT_PATH = "/Shashank/Python/final_debug.py"
    
    # Ensure script execution inside ANSA
    print(f"Loading and executing script: {SCRIPT_PATH}")
    
    # Use LoadExecuteFunc to properly load and execute the script
    script.LoadExecuteFunc(SCRIPT_PATH)

    print("Script execution completed.")

if __name__ == "__main__":
    main()



