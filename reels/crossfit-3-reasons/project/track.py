# Face track for the "camera": OpenCV Haar (frontal + profile) every 2nd frame -> cam/track.json [t, cx, cy, face_h] (source pixels)
import cv2,json,sys,numpy as np
W='/root/Documents/video-editor-bassam/projects/x7-reel-1'
cap=cv2.VideoCapture(W+'/cutz_orig.mp4');fps=cap.get(cv2.CAP_PROP_FPS)
fr=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
pr=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_profileface.xml')
out=[];i=0;prev=None
while True:
    ok,f=cap.read()
    if not ok:break
    if i%2==0:
        g=cv2.equalizeHist(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY))
        dets=list(fr.detectMultiScale(g,1.08,6,minSize=(36,36)))
        if not dets:
            dets=list(pr.detectMultiScale(g,1.08,6,minSize=(36,36)))+[(g.shape[1]-x-w,y,w,h) for (x,y,w,h) in pr.detectMultiScale(cv2.flip(g,1),1.08,6,minSize=(36,36))]
        # faces of the speaker sit in the middle band and are the largest/closest to the previous one
        dets=[d for d in dets if 250<d[1]+d[3]/2<1500]
        if dets:
            if prev is not None:
                d=min(dets,key=lambda d:abs(d[0]+d[2]/2-prev[0])+abs(d[1]+d[3]/2-prev[1])-2*d[3])
            else:d=max(dets,key=lambda d:d[3])
            c=(float(d[0]+d[2]/2),float(d[1]+d[3]/2),float(d[3]));
            if prev is None or abs(c[0]-prev[0])<260:
                prev=c;out.append([round(i/fps,3),*[round(v,1) for v in c]])
    i+=1
json.dump({'fps':fps,'frames':i,'track':out},open(W+'/cam/track.json','w'))
print('frames',i,'detections',len(out),'of',i//2)
