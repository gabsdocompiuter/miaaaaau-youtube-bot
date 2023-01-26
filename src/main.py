from compile_movies import CompileMovies
from datetime import timedelta
from dotenv import load_dotenv
from file_utils import delete_trash_files, delete_temp_files
from instagram_downloader import InstagramDownloader

import os
import file_utils


def main():
    print('starting bot...')

    load_dotenv()
    instagram_user = os.environ.get('instagram_username')
    instagram_pass = os.environ.get('instagram_password')
    video_max_duration = os.environ.get('video_max_duration')
    compilation_max_duration = os.environ.get('compilation_max_duration')
    temp_folder = os.environ.get('temp_folder')

    delete_temp_files(temp_folder)

    scraper = InstagramDownloader(instagram_user, instagram_pass, temp_folder)
    scraper.download_last_memes(days=1)
    file_utils.delete_trash_files(temp_folder)

    compiler = CompileMovies(temp_folder=temp_folder,
                             video_max_duration=video_max_duration,
                             compilation_max_duration=compilation_max_duration)
    videos_added = compiler.compile_videos()

    print(create_description(videos_added))

    # upload to youtube


def create_description(videos_added):
    description = ''
    time = 0

    for video in videos_added:
        description_line = get_seconds_in_minutes(
            time) + ': ' + video.instagram_account + '\n'
        description += description_line
        time += video.duration

    return description


def get_seconds_in_minutes(seconds):
    td = str(timedelta(seconds=seconds))
    td_splited = td.split(':')

    min = td_splited[1]
    sec = td_splited[2].split('.')[0]

    return min + ':' + sec


if __name__ == '__main__':
    main()
