import pytube.exceptions
from pytube import YouTube

# get input from user
yt_url = input("Enter the YouTube Video URL: ")
print("Link:", yt_url)

try:
    # creating YouTube Video object
    yt_video = YouTube(yt_url)
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
    print("Please Try Again...")
except pytube.exceptions.PytubeError:
    print("Please Try Again...")
else:
    print("Downloading...")
    # yt_options[option_input].download()
    yt_video.streams.get_by_itag(option_input).download()
    print("Downloaded Successfully")
