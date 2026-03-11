from pathlib import Path
import subprocess

# Resolve repo root from this script location
repo_root = Path(__file__).parent.parent.parent.resolve()  # .github/scripts -> repo root

def main():
    print("Decrypting submission...")
    subprocess.run(["python", str(repo_root / "encryption" / "decrypt.py")], check=True)

    print("Scoring submission...")
    subprocess.run(["python", str(repo_root / "leaderboard" / "score_submission.py")], check=True)

    print("Updating leaderboard...")
    subprocess.run(["python", str(repo_root / "leaderboard" / "update_leaderboard.py")], check=True)

if __name__ == "__main__":
    main()
