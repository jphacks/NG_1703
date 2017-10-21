#!/bin/bash
SOURCEMOV="hage.MOV"
SOURCEMP4="hage.mp4"
DEST_WAV="kuso.wav"
DEST_PNG="kuso.png"
ffmpeg -i $SOURCEMOV -map 0:1 -vn -ac 2 -acodec pcm_s24le -f wav $DEST_WAV && ffmpeg -i $SOURCEMOV -ss 1 -vframes 1 -f image2 $DEST_PNG
