import os
from yt_dlp import YoutubeDL
from moviepy import VideoFileClip

def download_video(video_url, output_dir='downloads'):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        video_filename = ydl.prepare_filename(info)
    return video_filename

def extract_audio(video_file, audio_dir='audio', audio_format='wav'):
    os.makedirs(audio_dir, exist_ok=True)
    audio_filename = os.path.splitext(os.path.basename(video_file))[0] + f'.{audio_format}'
    audio_filepath = os.path.join(audio_dir, audio_filename)

    with VideoFileClip(video_file) as video:
        audio = video.audio
        audio.write_audiofile(audio_filepath, codec='pcm_s16le', logger=None)

    return audio_filepath

def download_and_extract_audio(video_url):
    print("Downloading video...")
    video_file = download_video(video_url)
    print(f"Video downloaded to {video_file}")

    print("Extracting audio...")
    audio_file = extract_audio(video_file)
    print(f"Audio extracted to {audio_file}")

    return audio_file

if __name__ == '__main__':
    test_url = input("Enter a video URL: ")
    audio_path = download_and_extract_audio(test_url)
    print(f"Audio file available at: {audio_path}")

