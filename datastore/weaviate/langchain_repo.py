import subprocess
import os
import shutil

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        exit(1)

if __name__ == "__main__":
    # Step 1: Update git submodules
    print("Updating git submodules...")
    run_command("git submodule update --init --recursive")

    # Step 2: Clone 'docs' folder from Langchain repo into a temporary directory
    print("Cloning Langchain docs...")
    temp_dir = "temp_langchain_docs"
    run_command(f"git clone --depth 1 --filter=blob:none --sparse https://github.com/langchain-ai/langchain {temp_dir}")
    os.chdir(temp_dir)
    run_command("git sparse-checkout set docs")

    # Step 3: Move docs to database/resources/langchain-repo
    print("Moving docs to database/resources/langchain-repo...")
    target_dir = "../database/resources/langchain-repo"
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.move("docs", target_dir)

    # Cleanup: Remove temporary directory and navigate back to original directory
    print("Cleaning up...")
    os.chdir("..")
    shutil.rmtree(temp_dir)

    print("Operation completed successfully.")
