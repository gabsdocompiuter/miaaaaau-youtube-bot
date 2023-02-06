from compile_movies import CompileMovies
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv, set_key
from instagram_downloader import InstagramDownloader
from youtube_uploader import YoutubeUploader

import os
import file_utils


def main():
    print('starting bot...')

    load_dotenv()
    instagram_user = os.environ.get('instagram_username')
    instagram_pass = os.environ.get('instagram_password')
    video_max_duration = int(os.environ.get('video_max_duration'))
    compilation_max_duration = int(os.environ.get('compilation_max_duration'))
    temp_folder = os.environ.get('temp_folder')
    youtube_folder = os.environ.get('youtube_folder')
    video_title = os.environ.get('video_title')
    how_many_days_to_search = int(os.environ.get('how_many_days_to_search'))
    video_tags = os.environ.get('video_tags').split(';')
    video_number = int(os.environ.get('video_number'))

    file_utils.delete_folder_files(temp_folder)

    scraper = InstagramDownloader(instagram_user, instagram_pass, temp_folder)
    scraper.download_last_memes(days=how_many_days_to_search)
    file_utils.delete_trash_files(temp_folder)

    compiler = CompileMovies(temp_folder=temp_folder,
                             video_max_duration=video_max_duration,
                             compilation_max_duration=compilation_max_duration,
                             youtube_folder=youtube_folder)
    videos_added = compiler.compile_videos()

    if not videos_added:
        return

    uploader = YoutubeUploader()

    video_file = f'{youtube_folder}/compiled_video.mp4'
    description = create_description(videos_added)
    title = f'{video_title} #{video_number}'

    uploader.upload_video(video_file, title, description, video_tags)

    set_key(find_dotenv(), 'video_number', str(video_number + 1))
    file_utils.delete_folder_files(temp_folder)
    file_utils.delete_folder_files(youtube_folder)


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
