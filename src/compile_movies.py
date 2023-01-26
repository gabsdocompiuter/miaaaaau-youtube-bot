from moviepy.editor import *
from glob import glob

import random


class CompileMovies:
    def __init__(self, temp_folder, video_max_duration, compilation_max_duration):
        self.temp_folder = temp_folder
        self.video_max_duration = int(video_max_duration)
        self.compilation_max_duration = int(compilation_max_duration)
        self.__clips = []

    def compile_videos(self):
        print()
        print('starting compilation process...')

        videos_to_add = self.get_videos()
        videos_added = []
        video_duration = 0

        while videos_to_add and video_duration <= self.compilation_max_duration:
            video = self.select_video(videos_to_add, videos_added)

            if not video:
                continue

            print('adding video ' + video.file_name)
            videos_to_add.remove(video)
            videos_added.append(video)
            video_duration += video.duration

            clip = VideoFileClip(video.video_path).resize(height=720)
            self.__clips.append(clip)

        if not videos_added:
            return

        print('compiling')
        compiled_video = concatenate_videoclips(
            self.__clips, method='compose', padding=0.3)
        compiled_video.write_videofile('youtube/compiled_video.mp4')

        return videos_added

    def select_video(self, videos_to_add, videos_added):
        selecting_video = True
        video = None

        while selecting_video and videos_to_add:
            video = random.choice(videos_to_add)

            if video.duration > self.video_max_duration:
                videos_to_add.remove(video)
                continue

            if not videos_added:
                selecting_video = False
            else:
                if video.instagram_account != videos_added[-1].instagram_account:
                    selecting_video = False
                elif len(videos_to_add) == 1:
                    videos_to_add.remove(video)
        return video

    def get_videos(self):
        paths = glob(self.temp_folder + '/*.mp4')
        videos = []

        for video_path in paths:
            video_info = self.get_movie_info(video_path)
            videos.append(video_info)

        return videos

    def get_movie_info(self, video_path):
        file_name = video_path.split('\\')[-1]
        instagram_account = file_name.split('---')[0]

        clip = VideoFileClip(video_path)

        movie_info = MovieInfo(instagram_account=instagram_account,
                               file_name=file_name,
                               video_path=video_path,
                               duration=clip.duration,
                               width=clip.w,
                               height=clip.h)

        clip.close()
        return movie_info


class MovieInfo:
    def __init__(self, instagram_account, file_name, video_path, duration, width, height):
        self.instagram_account = instagram_account
        self.file_name = file_name
        self.video_path = video_path
        self.duration = duration
        self.widht = width
        self.height = height
