
from dotenv import load_dotenv, find_dotenv, set_key
import os

load_dotenv()

video_title = os.environ.get('video_title')
video_number = int(os.environ.get('video_number'))


title = f'{video_title} #{video_number}'

print(title)

set_key(find_dotenv(), 'video_number', str(video_number + 1))
