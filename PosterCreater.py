from PIL import Image,ImageDraw,ExifTags,ImageFont
import sys,os
from datetime import datetime

def FixO(oimg):
    print('oimg')
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
            
        exif=dict(oimg._getexif().items())

        if exif[orientation] == 3:
            oimg=oimg.rotate(180, expand=True)
        elif exif[orientation] == 6:
            oimg=oimg.rotate(270, expand=True)
        elif exif[orientation] == 8:
            oimg=oimg.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # cases: oimg don't have getexif
        pass
    oimg = oimg.resize((790,1050))
    return oimg

def wrap(dtext):
    if dtext[0:4]+' -' in dtext:
        dtext = dtext.replace(dtext[0:4]+' -',dtext[0:4]+'.')
    elif dtext[0:4]+' .' in dtext:
        dtext = dtext.replace(dtext[0:4]+' .',dtext[0:4]+'.')
    elif dtext[0:4]+'_' in dtext:
        dtext = dtext.replace(dtext[0:4]+'_',dtext[0:4]+'.')
    elif dtext[0:4]+'-' in dtext:
        dtext = dtext.replace(dtext[0:4]+'-',dtext[0:4]+'.')
    elif dtext[0:4]+' _' in dtext:
        dtext = dtext.replace(dtext[0:4]+' _',dtext[0:4]+'.')
    elif dtext[0:4]+' ' in dtext:
        dtext = dtext.replace(dtext[0:4]+' ',dtext[0:4]+'.')
    if not(dtext[5] == ' '):
        dtext = dtext[0:5]+' '+dtext[5:]
                      
    imgx = Image.new(mode = "RGB", size = (2480, 3508),color = (255,255,255))
    drwt = ImageDraw.Draw(imgx)
    dfont = ImageFont.truetype("timesbold.ttf", 56) #<- fontSize
    w, h = drwt.textsize(dtext, spacing= 30, font = dfont)
    if w > 840:
        lspace = 0
        for i in range(1,len(dtext)):
            ws, hs = drwt.textsize(dtext[0:i], font = dfont)
            if dtext[i] == " ":
                lspace = i
            if ws > 840:
                 return (dtext[0:4]," -"+dtext[5:lspace],dtext[lspace+1:])
    imgx.close()
    return (dtext[0:4]," -"+dtext[5:]," ")

def log(Text):
    print(Text)
    with open(logf,'a+',encoding = 'utf-8') as f:
        f.write(datetime.now().strftime("%d/%m/%Y-%H:%M:%S") + " -> " +Text+"\n")   

if __name__ == '__main__':
    poster = 0
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y-%H%M%S")
    logf = dt_string + ".log"

    if len(sys.argv) == 1 :
        log("Need an argument to procced.\n")
    else:
        log("Input Folder path = " + sys.argv[1])
        if os.path.isdir(sys.argv[1] + "\\images") :
            ip = sys.argv[1] + "\\images\\"
            log("images folder path = " + sys.argv[1] + "\\images")
            if os.path.isdir(sys.argv[1]+'\\'+sys.argv[1].split('\\')[-1]):
                log("Save folder path already exist.")
                pass
            else:
                os.mkdir(sys.argv[1]+'\\'+sys.argv[1].split('\\')[-1])
                log("Save folder path not exist and is created.")
            log("Save folder path = "+sys.argv[1]+'\\'+sys.argv[1].split('\\')[-1]+"\n")
            os.system("rename \""+ip+"*.*\" *.jpg")
            log("rename all file from "+ip+" to jpg file format.\n")
            if os.path.isfile(sys.argv[1] + "\\Name\\name.txt"):
                with open(sys.argv[1] + '\\Name\\name.txt','r') as f:
                    log("input name.txt path = " + sys.argv[1] + '\\Name\\name.txt\n')
                    fl = f.read().splitlines()
                    log("Input movie name = " + str(len(fl)) + " items.")
                    log(str(len(fl)//4) + " poster(s) will create.")
                    log(str(len(fl)%4) + " item(s) will left to create poster.\n")
                    for i in range(len(fl)//4):
                        g = i*4
                        log("Pending poster = " + str(int(g/4+1)).zfill(3)+'.jpg')
                        #Blank image with color: white and size: 2480, 3508
                        img = Image.new(mode = "RGB", size = (2480, 3508),color = (255,255,255))
                        log("Create A4 plain paper.")
                        
                        #Shaine Logo at 700,150,1080,415
                        shaine = Image.open("shaine.png")
                        shaine = shaine.resize((1080,415))
                        img.paste(shaine,(700, 150),shaine)
                        log("Add title image.")

                        #Blue line from 0,595+(blue line width/2) to 2480,595+(blue line width/2) with width 220
                        bline = ImageDraw.Draw(img)
                        blw = 220
                        bline.line([(0,595+(blw/2)),(2480,595+(blw/2))], fill = (25,25,195), width = blw)
                        log("Draw Blue line.")

                        #Welcome message from (2480-wmsg.textsize.width/2) to (595+(220-wmsg.textsize.hight/2))
                        wmsg = ImageDraw.Draw(img)
                        wfont = ImageFont.truetype("timesbold.ttf", 96) #<- fontSize
                        wtext = 'Myanmar Subtitle Movies For You (HD)'
                        w,h = wmsg.textsize(wtext, font = wfont)
                        wmsg.text(((2480-w)/2, 595+(220-h)/2), wtext, fill = (255,255,255), font = wfont)
                        log("Add title txet to Blue line.")
                        
                        #imgw = 790 imgh = 1050 text = 215 margin = 85 imgx 300 y = 900 x2 = 1390 y2 = 2205
                        if os.path.isfile(ip+fl[g][0:4]+'.jpg') :
                            img1 = Image.open(ip+fl[g][0:4]+'.jpg')
                            log("Image 1 = "+ip+fl[g][0:4]+'.jpg '+str(img1.size))
                            img1 = FixO(img1)
                            img.paste(img1,(300,900))
                        else:
                            log(ip+fl[g][0:4]+'.jpg not exists.')
                            log("Poster "+str(int(g/4+1)).zfill(3)+'.jpg is skip.\n')
                            img.close()
                            continue
                            
                        if os.path.isfile(ip+fl[g+1][0:4]+'.jpg') :
                            img2 = Image.open(ip+fl[g+1][0:4]+'.jpg')
                            log("Image 2 = "+ip+fl[g+1][0:4]+'.jpg '+str(img2.size))
                            img2 = FixO(img2)
                            img.paste(img2,(1390,900))
                        else:
                            log(ip+fl[g+1][0:4]+'.jpg not exists.')
                            log("Poster "+str(int(g/4+1)).zfill(3)+'.jpg is skip.\n')
                            img.close()
                            continue                        

                        if os.path.isfile(ip+fl[g+2][0:4]+'.jpg') :
                            img3 = Image.open(ip+fl[g+2][0:4]+'.jpg')
                            log("Image 3 = "+ip+fl[g+2][0:4]+'.jpg '+str(img3.size))
                            img3 = FixO(img3)
                            img.paste(img3,(300,2165))
                        else:
                            log(ip+fl[g+2][0:4]+'.jpg not exists.')
                            log("Poster "+str(int(g/4+1)).zfill(3)+'.jpg is skip.\n')
                            img.close()
                            continue

                        if os.path.isfile(ip+fl[g+3][0:4]+'.jpg') :
                            img4 = Image.open(ip+fl[g+3][0:4]+'.jpg')
                            log("Image 4 = "+ip+fl[g+3][0:4]+'.jpg '+str(img4.size))
                            img4 = FixO(img4)
                            img.paste(img4,(1390,2165))
                        else:
                            log(ip+fl[g+3][0:4]+'.jpg not exists.')
                            log("Poster "+str(int(g/4+1)).zfill(3)+'.jpg is skip.\n')
                            img.close()
                            continue

                        #DrwText
                        drw1 = ImageDraw.Draw(img)
                        dfont = ImageFont.truetype("timesbold.ttf", 56) #<- fontSize
                        dtext = wrap(fl[g])
                        dx,dy = 300,900+1050
                        w, h = drw1.textsize(dtext[0]+dtext[1]+dtext[2], spacing= 30 ,font = dfont)
                        drw1.text((dx,dy+(170-h)/2-((170-h)/2)/2), dtext[0], fill="Red", spacing=30,font = dfont)
                        drw1.text((dx+drw1.textsize(dtext[0], spacing= 30 ,font = dfont)[0],dy+(170-h)/2-((170-h)/2)/2), dtext[1],fill=(0,0,0) ,font = dfont)
                        drw1.text((dx,30+dy+(170-h)/2+((170-h)/2)/2), dtext[2],fill=(0,0,0) ,font = dfont)
                        log("Movie title 1 = "+dtext[0]+dtext[1]+" "+dtext[2])

                        drw2 = ImageDraw.Draw(img)
                        dfont = ImageFont.truetype("timesbold.ttf", 56) #<- fontSize
                        dtext = wrap(fl[g+1])
                        dx,dy = 1390,900+1050
                        w, h = drw2.textsize(dtext[0]+dtext[1]+dtext[2], spacing= 30 ,font = dfont)
                        drw2.text((dx,dy+(170-h)/2-((170-h)/2)/2), dtext[0], fill="Red", spacing=30,font = dfont)
                        drw2.text((dx+drw2.textsize(dtext[0], spacing= 30 ,font = dfont)[0],dy+(170-h)/2-((170-h)/2)/2), dtext[1],fill=(0,0,0) ,font = dfont)
                        drw2.text((dx,30+dy+(170-h)/2+((170-h)/2)/2), dtext[2],fill=(0,0,0) ,font = dfont)
                        log("Movie title 2 = "+dtext[0]+dtext[1]+" "+dtext[2])

                        drw3 = ImageDraw.Draw(img)
                        dfont = ImageFont.truetype("timesbold.ttf", 56) #<- fontSize
                        dtext = wrap(fl[g+2])
                        dx,dy = 300,900+1050+215+1050
                        w, h = drw3.textsize(dtext[0]+dtext[1]+dtext[2], spacing= 30 ,font = dfont)
                        drw3.text((dx,dy+(170-h)/2-((170-h)/2)/2), dtext[0], fill="Red", spacing=30,font = dfont)
                        drw3.text((dx+drw3.textsize(dtext[0], spacing= 30 ,font = dfont)[0],dy+(170-h)/2-((170-h)/2)/2), dtext[1],fill=(0,0,0) ,font = dfont)
                        drw3.text((dx,30+dy+(170-h)/2+((170-h)/2)/2), dtext[2],fill=(0,0,0) ,font = dfont)
                        log("Movie title 3 = "+dtext[0]+dtext[1]+" "+dtext[2])

                        drw4 = ImageDraw.Draw(img)
                        dfont = ImageFont.truetype("timesbold.ttf", 56) #<- fontSize
                        dtext = wrap(fl[g+3])
                        dx,dy = 1390,900+1050+215+1050
                        w, h = drw4.textsize(dtext[0]+dtext[1]+dtext[2], spacing= 30 ,font = dfont)
                        drw4.text((dx,dy+(170-h)/2-((170-h)/2)/2), dtext[0], fill="Red", spacing=30,font = dfont)
                        drw4.text((dx+drw4.textsize(dtext[0], spacing= 30 ,font = dfont)[0],dy+(170-h)/2-((170-h)/2)/2), dtext[1],fill=(0,0,0) ,font = dfont)
                        drw4.text((dx,30+dy+(170-h)/2+((170-h)/2)/2), dtext[2],fill=(0,0,0) ,font = dfont)
                        log("Movie title 4 = "+dtext[0]+dtext[1]+" "+dtext[2])

                        img.save(sys.argv[1]+'\\'+sys.argv[1].split('\\')[-1]+'\\'+str(int(g/4+1)).zfill(3)+'.jpg')
                        log("Poster save to "+sys.argv[1]+'\\'+sys.argv[1].split('\\')[-1]+'\\'+str(int(g/4+1)).zfill(3)+'.jpg')
                        img.close()
                        log("Poster "+str(int(g/4+1)).zfill(3)+".jpg was created successfully\n")
                        poster += 1
                os.system('explorer "'+sys.argv[1]+'\\'+sys.argv[1].split('\\')[-1]+'\\"')
                log(str(poster)+"/"+str(len(fl)//4) +" poster(s) was created.\n")
            else:
                log(sys.argv[1] + "\\Name\\name.txt not exists\n")
        else:
            log(sys.argv[1] + "\\images folder not exists\n")
    input("Press ENTER_KEY to see log...")
    os.system("start "+logf)
