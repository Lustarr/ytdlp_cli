"""
https://www.youtube.com/watch?v=ucZl6vQ_8Uo
"""

import sys
import os
from urllib.parse import unquote
from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func
import requests

def main():
  """
  program entry
  """
  ytdl_opts = {
    "postprocessors": [{
      "key": "FFmpegVideoConvertor",
      "preferedformat": "mp4",
    }],
    "verbose": False,
    "force_keyframes_at_cuts": True,
    "quiet": True,
    "overwrites": True,
  }
  oembed_url = "https://www.youtube.com/oembed"

  try:
    # check url
    url = input("Pls enter URL...\n")
    response = requests.get(url, timeout=5)
    if not response.ok:
      print("\n@url fail")
      return

    if response.url != url:
      print("redirecting to " + response.url)
      url = response.url
    params = {"url": url, "format": "json"}
    response = requests.get(oembed_url, params=params, timeout=5)
    if "https://www.youtube.com/watch?" not in unquote(response.url):
      print("\n@invalid url")
      return

  except Exception as ex:
    print("\n@url except\n" + str(ex))
    return

  # clip decision
  is_clip = input(
    "\nDo you want to clip video? (y/n) *Notice: quality decline to clip precisely\n"
  ).upper()
  if is_clip == "Y":
    try:
      start_sec = int(input("Pls enter positive integer as start second...\n"))
      end_sec = int(input("Pls enter positive integer as end second...\n"))
      if start_sec < 0 or end_sec < 0:
        print("\n@negative number entered")
        return

      elif start_sec >= end_sec:
        print("\n@start second exceed end second")
        return

    except Exception as ex:
      print("\n@invalid number\n" + str(ex))
      return

    ytdl_opts.update(
      {"download_ranges": download_range_func(None, [(start_sec, end_sec)])})
  elif is_clip != "N":
    print("\n@unexpected answer")
    return

  # download action
  try:
    ytdl = YoutubeDL(ytdl_opts)
    print(
      "\n*Downloading now(the longer video is, the longer to wait)")
    # ytdl.download(url) #original method
    info = ytdl.extract_info(url)
    # fullFilename = ytdl.prepare_filename(info, warn=True) #other filename
    # tempFilename = ytdl.prepare_filename(info, "temp") #other filename
    filename = ytdl.prepare_filename(info)
    print(f"\ndownload {filename} successfully")
    return

  except Exception as ex:
    print("\n@download except\n" + str(ex))
    return

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
  except Exception as ex:
    print("\n" + f"main except {ex}")
  finally:
    tmp = input("\nPls press enter to close...\n")
