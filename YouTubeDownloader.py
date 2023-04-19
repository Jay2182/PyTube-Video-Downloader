import pytube.exceptions
from pytube import YouTube


def on_progress(stream, chunk, bytes_remaining):
    """Callback function to check progress"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    # printing download status
    print(f"\rStatus: {round(pct_completed, 2)} %", end="")


def start_downloader(yt_url):
    """YouTube video downloader"""
    # get input from user
    print("Link:", yt_url)

    try:
        # creating YouTube Video object
        yt_video = YouTube(yt_url, on_progress_callback=on_progress)
        # printing title of video
        print("Title:", yt_video.title)
        # printing thumbnail of video
        print("Thumbnail:", yt_video.thumbnail_url)

        print("Download Options")
        # filtering video based on extension and file type (audio + video)=progressive
        yt_options = list(yt_video.streams.filter(progressive=True, file_extension="mp4", type="video"))
        # printing download option
        count = 0
        for option in yt_options:
            print(
                f"{count:4} itag:{option.itag}, type:{option.type}, res:{option.resolution}, size:{yt_video.streams.get_by_itag(option.itag).filesize / (10 ** 6)} MB")
            count += 1

        # getting download option from user
        option_input = int(input("Enter itag (-1 for exit): "))
        if option_input == -1:
            print("Exiting...")
            exit(1)

    except ValueError:
        print("Please Enter valid input... Try again")
    except KeyError:
        print("Key Error, Please Try Again...")
    except pytube.exceptions.PytubeError:
        print("Downloader Error, Please Try Again...")
    else:
        print("Downloading...")
        # yt_options[option_input].download()
        yt_video.streams.get_by_itag(option_input).download()
        print("Downloaded Successfully")


if __name__ == "__main__":
    url = input("Enter the YouTube Video URL: ")
    start_downloader(url)
