import cv2
 
cap=cv2.VideoCapture(0)
cap2=cv2.VideoCapture(1)
i=0

weight = 1280
height = 720
fps = 30


cap.set(3, weight)  #设置宽度
cap.set(4, height)  #设置长度


cap2.set(3, weight)  #设置宽度
cap2.set(4, height)  #设置长度

#cap.set(5, fps)  
#cap2.set(5, fps) 
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))





width = cap.get(3)
height  = cap.get(4)
fps  = cap.get(5)
Fourcc  = cap.get(6)


#打印信息
print(width ,height, fps, Fourcc)
while(1):
    ret ,frame = cap.read()
    ret2 ,frame2 = cap2.read()
    left = int((weight-512)/2)
    right = int((weight-512)/2+512)
    up = int((height-512)/2)
    down = int((height-512)/2+512)
    frame = frame[up:down,left:right]
    frame2 = frame2[up:down,left:right]

    k=cv2.waitKey(1)
    if k==27:
        break
    elif k==ord('s'):
        cv2.imwrite('./photo/L'+str(i)+'.jpg',frame)
        cv2.imwrite('./photo/R'+str(i)+'.jpg',frame2)
        i+=1
        print("save!")
    cv2.imshow("capture1", frame)
    cv2.imshow("capture2", frame2)

cap.release()
cv2.destroyAllWindows()