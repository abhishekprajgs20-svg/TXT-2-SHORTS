import os
import time
from creator import ShortCreator
from config import Config
from utils import cleanup_dir

def main():
    cfg = Config()
    creator = ShortCreator(cfg)
    
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    os.makedirs(cfg.TEMP_DIR, exist_ok=True)
    
    print("Starting Short Creator...")
    while True:
        try:
            creator.process_next()
        except Exception as e:
            print(f"Error in main loop: {e}")
        time.sleep(cfg.POLL_INTERVAL)

if __name__ == "__main__":
    main()