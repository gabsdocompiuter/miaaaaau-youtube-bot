import datetime
import dateutil.relativedelta
from instaloader import Instaloader, Profile

from announcements_terms import get_annoucements_terms


class InstagramDownloader:
    def __init__(self, username, password, temp_folder):
        self.instagram_user = username
        self.instagram_pass = password
        self.temp_folder = temp_folder

        self.load_session()

    def load_session(self):
        print('loading session...')

        pattern = '@{profile}---{filename}'

        self.loader = Instaloader(filename_pattern=pattern)
        self.loader.load_session_from_file(self.instagram_user)

    def download_last_memes(self, days):
        print('getting following profiles...')

        today = datetime.date.today()
        limit_date = today - dateutil.relativedelta.relativedelta(days=days)

        profile = Profile.from_username(
            self.loader.context, self.instagram_user)

        for follower in profile.get_followees():
            print('scraping from ' + follower.username)

            for post in follower.get_posts():
                if post.date_local.date() < limit_date:
                    break

                is_video = post.get_is_videos()
                if is_video[0] and not self.text_contains_announcements(post.caption):
                    self.loader.download_post(
                        post, target=self.temp_folder)
                    print('')
            print('')

    def text_contains_announcements(self, text):
        if not text:
            return False

        lower_text = text.lower()

        for term in get_annoucements_terms():
            if lower_text.__contains__(term):
                return True

        return False
