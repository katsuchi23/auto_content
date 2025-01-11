from pathlib import Path

def ensure_output_dirs():
    """
    Create required output directories if they don't exist.
    Creates directories for:
    - output/
        - images/
        - audio/
        - video/
    
    Returns:
        None
    """
    output_dirs = [
        "output/images",
        "output/audio",
        "output/video"
    ]
    
    for dir_path in output_dirs:
        path = Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)