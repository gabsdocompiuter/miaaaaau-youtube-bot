from dotenv import load_dotenv
from instagram_downloader import InstagramDownloader
# from file_utils import delete_trash_files

import os
import file_utils


def main():
    print('starting bot...')

    load_dotenv()

    instagram_user = os.environ.get('instagram_username')
    instagram_pass = os.environ.get('instagram_password')
    temp_folder = 'temp'

    scraper = InstagramDownloader(instagram_user, instagram_pass, temp_folder)
    scraper.download_last_memes(days=1)
    file_utils.delete_trash_files(temp_folder)


if __name__ == '__main__':
    main()
