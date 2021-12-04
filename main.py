from src.ClipHandler import ClipHandler
from src.ClipCompilationCreator import ClipCompilationCreator
from src.parser import get_arg_parser
from src.DriveUploader import DriveUploader
import os
import time
import logging

logging.getLogger().setLevel(logging.INFO)
games = {
    "fortnite": "Fortnite",
    "lol": "League of Legends",
    "apexl": "Apex Legends",
    "valo": "Valorant",
    "fallg": "Fall Guys"
}

parser = get_arg_parser()
args = parser.parse_args()
game = games.get(args.game, args.game)
ch = ClipHandler(game, args.asset_path, args.output_path)
ch.get_clips(
    number_of_clips=args.number_of_clips,
    timespan=args.timespan,
    language=args.language,
    min_length=args.min_length,
    max_creator_clips=args.max_creator_clips,
    min_clip_duration=args.min_clip_duration,
)
vcc = ClipCompilationCreator(game, args.asset_path, args.output_path)
vcc.create_compilation()
du = DriveUploader(game)
print(f"\n{du}")
print("\n**********Done!**********\n")