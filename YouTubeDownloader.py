from pytube import YouTube
import pytube.exceptions


def on_progress(stream, chunk, bytes_remaining):
    """Callback function to check progress"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    # printing download status
    # print(f"\rStatus: {round(pct_completed, 2)} %", end="")
    print(f"\rStatus: [{round(pct_completed/2)*'#'}{(50-round(pct_completed/2))*'-'}] {round(pct_completed, 2)} %", end="")


def start_downloader(yt_url, retry_count=0):
    """YouTube video downloader"""
    if retry_count > 20:
        print("Unable to download")
        return
    try:
        # creating YouTube Video object
        yt_video = YouTube(yt_url, on_progress_callback=on_progress)
        # printing title of video
        print("Title:", yt_video.title)
        # printing thumbnail of video
        print("Thumbnail:", yt_video.thumbnail_url)

        print("Download Options")
        # filtering audio based on extension and file type
        yt_options = list(yt_video.streams.filter(type="audio"))
        count = 0
        print("Audio")
        for option in yt_options:
            print(
                f"{count:4} "
                f"itag:{option.itag}, "
                f"type:{option.type}, "
                f"quality:{option.abr:>7}, "
                f"ext:{option.mime_type.split('/')[1]:>5}, "
                f"size:{round(yt_video.streams.get_by_itag(option.itag).filesize / (10 ** 6), 2):>7} MB, "
                f"codec:{option.codecs}")
            count += 1
        # filtering video based on extension and file type (audio + video)=progressive
        yt_options = list(yt_video.streams.filter(progressive=True, type="video"))
        # printing download option
        count = 0
        print("Videos")
        for option in yt_options:
            print(
                f"{count:4} "
                f"itag:{option.itag:>3}, "
                f"type:{option.type}, "
                f"res:{option.resolution:>5}, "
                f"Extension:{option.mime_type.split('/')[1]:>5}, "
                f"size:{round(yt_video.streams.get_by_itag(option.itag).filesize / (10 ** 6), 2):>7} MB")
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
        print("Downloader Error, Retrying...")
        return start_downloader(yt_url, retry_count+1)
    else:
        print("Downloading...")
        # yt_options[option_input].download()
        yt_video.streams.get_by_itag(option_input).download()
        print("\nDownloaded Successfully")


if __name__ == "__main__":
    # get input from user
    url = input("Enter the YouTube Video URL: ")
    start_downloader(url)
