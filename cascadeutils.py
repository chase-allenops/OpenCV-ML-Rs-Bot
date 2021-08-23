import os 

def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write('negative/' + filename +'\n')

# C:/Users/chase/Desktop/Python/OpenCV/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=C:/Users/chase/Desktop/Python/OpenCVBots/machine-learning/positive/
# C:/Users/chase/Desktop/Python/OpenCV/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec
# C:/Users/chase/Desktop/Python/OpenCV/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 230 -numNug 200 -numStages 12

# C:/Users/chase/Desktop/Python/OpenCV/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 200 -numNeg 1000 -numStages 12 -w 24 -h 24 -maxFalseAlarmRate 0.3 -minHitRate 0.999