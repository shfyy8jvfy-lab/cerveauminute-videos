#!/bin/sh
# Traitement de la voix Zion Aquila : ~2 demi-tons plus grave + coffre (bas-médium, compression, légère saturation, petite salle)
# Usage : sh voix.sh entree.mp3 sortie.mp3
ffmpeg -y -loglevel error -i "$1" -af "asetrate=44100*0.89,aresample=44100,atempo=1/0.89,highpass=f=45,equalizer=f=110:t=q:w=1.0:g=6,equalizer=f=220:t=q:w=1.2:g=3,equalizer=f=3500:t=q:w=1.5:g=2,acompressor=threshold=-22dB:ratio=4:attack=5:release=120:makeup=4,asoftclip=type=tanh:threshold=0.9,aecho=0.8:0.6:30|60:0.12|0.08" -ar 44100 -b:a 192k "$2"
