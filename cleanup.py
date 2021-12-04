import os
import shutil
# from src.utils import get_valid_game_name

# game_name = get_valid_game_name(game)
location = 'TwitchClips/media/'
for folder in os.listdir(location):
    print(f"Folder: {folder}")
    path = os.path.join(location, folder)
    shutil.rmtree(path, ignore_errors=True, onerror=None)