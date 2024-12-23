#Image Editor
from PIL import (Image, ImageDraw, ImageFont,
                                                     ImageColor)
from glob import glob, iglob
#from time import sleep
import os.path as path
import os

curdir=os.getcwd()
#print(curdir)


class ImageHandler():
    """ Class that handles backend image editing"""
    xtra=[]
    fontdir=path.join(curdir, 'fonts')
    displayPort=None
    def __init__(self):
        self.name = 'HandlerNoel'
        self.image = None
        self.origin = None
        self.resolution = 0
        self.format = None
        self.resized = None
        self.files = []
        self.fonts = []
        self.font = None
        self.calledSave=0
        self.fontdir = os.walk(self.fontdir)
        roots=None
        for root, directories, contents in self.fontdir:
            # joining together the root folder where
            # the directory exists of every files along 
            # with its name                
           for name in contents:
              #print(os.path.join(root, name))
              #print (name)
              if  name.endswith('ttf'):
                  #print(name)
                  self.fonts.append(name)
           roots=root
        self.fonts.insert(0, roots)
        #print('fonts', self.fonts)
        
        
    def load(self):
        #loads images into memory
        if not self.files:
            try:
                self.name = str(
                    input('name or path to image file ')
                        )
                self.image = Image.open(self.name)
            except Exception as e:
                print(e)
                self.searchFile()
                self.load()
        else:
            try:
                ask = int(input('Choice '))
                self.image = Image.open(
                                        self.files[ask-1])
            except Exception:
                print('Error processing request')
                exit()
                
        self.origin = self.image.copy()
        print('image resolution: ', self.image.size)
        self.getMethod()
        #return self.image 
    
    def resize(self):
        res = []
        for y in range(2):
            r = int(input('image resolution '))
            res.append(r)
            
        self.resolution = res
        #print (type (self.resolution))
        try:
            self.resized = self.image.resize(self.resolution)
            self.resized.show()
            self.image=self.resized
            print('Image resized to', res)
        except Exception:
            print ('unable to set resolution for image')
           
           
    def rotate(self, angle=0):
        try:
            ask = int(input('Angle of rotation'))
            self.image = self.image.rotate(ask)
        except ValueError:
            print('Unable to rotate image: input not an interger') 
    
    def flip(self):
        docs = '''
                    L to flip image left
                    R to flip image right
                    U to flip image vertically upward
                    D to flip image vertically downward
                    '''
        dirn=0
        if not dirn:
            print(docs)
            ask = str(input(
                        'Input direction to flip image in '))
            dirn = ask.lower()
            
        if dirn in 'lr':
            self.image = self.image.transpose(
                                    Image.FLIP_LEFT_RIGHT)
            
        elif dirn in 'ud':
            self.image = self.image.transpose(
                                    Image.FLIP_TOP_BOTTOM)      
        else:
            print("Invalid command")
            
            
    def waterMark(self):
        # setting up parameters
        print('  Y -- Yes \n  N -- No')
        quest='  Create water-mark on current image ?'
        ask = str(input(quest))
        ask = ask.lower()
        if ask == 'y':
            pass
        else:
            print('  Discarding currrent image..')
            sleep(.8)
            print(
            '  Creating blank image for water-mark')
            sleep(.4)
            print(
            '  >>>>>>>>>>>>>>>>>>')
            print('  Done')
            # retrieving color interger from user
            print('  Use color values between 0 and 256')             
            for a in ('Ist,', '2nd', '3rd'):
                try:
                    col=int(input(
                                '{} interger input '.format(a)))
                    self.xtra.append(col)
                except ValueError:
                    self.xtra.append(0)
            self.xtra.append(255)
            print('  ', self.xtra)
            quest = '  Using default scale 100x100 can \
                          scale using resize method'
            print(quest)      
            self.image= Image.new('RGBA', (100,100),
                                     (255,255,255,0))
                                     
        for a in ('Ist,', '2nd', '3rd'):
            try:
                col=int(input(
                            '{} interger input '.format(a)))
                self.xtra.append(col)
            except ValueError:
                self.xtra.append(0)
        self.xtra.append(255)
        print('  ', self.xtra)
        print('  Available fonts...')
        n=1
        for i in self.fonts[1:]:
            print('  {}. '.format(n), i)
            n+=1
        try:
            font = int(input('  choose font'))
        except ValueError:
            print('Using default font')
            font=1
        try:
            tsize  = int(input('Size of font'))
            self.font =\
                 ImageFont.truetype(path.join(
            self.fonts[0], self.fonts[font]), tsize)
        except ValueError:
            print('Invalid Input using default size')
            self.font =\
                         ImageFont.truetype(path.join(
            self.fonts[0], self.fonts[font]), 20)
        print('Position of text \n C for  Center')
        txtpos=[]
        pos ='  00 for Center or input  {} position'
        for p in ('X', 'Y'):
            try:
                userpos= int(input(pos.format(p)))
                txtpos.append(userpos)
            except ValueError:
                txtpos.append('00')
        text = str(input('  Text for the image '))
        watermark = ImageDraw.Draw(self.image)
        left, top, right, bottom = self.font.getbbox(
                                                        text) 
        size = right - left, bottom - top
        print('  size', size)
        if size > self.image.size:
            self.image.resize(size)#resizing
        im_size=self.image.size
        if im_size[0]-size[0] >= 35:
            pass
        x=size[0]
        y=size[1]
        if type(txtpos[0]) != type(2): #for the x-axis
            x=100//2 -x//2
        else:
            x=size[0]
        if type(txtpos[1]) != type(2): #for the y-axis
            y=100//2 -y//2
        else:
            y=size[1]
        col=tuple(self.xtra)
        watermark.text((x,y), text, font=self.font,
                                                                fill=col) 
        print('  Done -- Used ', text, 'as watermark')      
        '''stopped at water-mark text stuff and size
              and positioning '''
        #new.convert('L')      
        
    def grayScale(self):
        self.image = self.image.convert('RGBA')   
        new_image = Image.new('RGBA',
                             self.image.size)

        for x in range(self.image.width):
            for y in range(self.image.height):
                r, g, b, a = self.image.getpixel((x, y))
                gray = int(
                    0.2989 * r + 0.587 * g + 0.114 * b
                    )
                new_image.putpixel((x, y),
                                     (gray, gray, gray, a)
                                     )
        self.image = new_image
       # return gray
         
         
    def  swapBands(self):
        self.image = self.image.convert('RGBA')
        r,g,b,a = self.image.split()
        self.image = Image.merge('RGBA', (b, g, r,a))
        
          
    def searchFile(self):
        self.files = []
        formatS = '''JPEG
                      PNG
                      BMP
                      GIF
                      PPM
                      TIFF
                      JPG
                      WEBP'''
        print('File format supported: ', formatS) 
        print('Choose the corresponding file to edit')
        try:
            fName = str(
                input("Name extension of file ")
                    )
        except Exception as e:
            print(e)
            exit() 
        for fileN in iglob("**."+fName.lower()):
            #file,ext=os.path.splitext(fileN)
            #im=Image.open(fileN)
            #im.thumbnail(size,Image.ANTIALIAS)
            #im.save(file+".thumbnail","JPEG")
            self.files.append(fileN)
        if not self.files:
            print(f"No {fName} file found")
        num = 1 
        for f in self.files:
            print('   ', num, ':', f)
            num += 1
                   
    def getMethod(self):
        num = 1
        methods = ('load', 'resize', 'rotate', 'flip',
                         'searchFile', 'grayScale',
                         'getMethod', 'swapBands',
                        'waterMark', 'restore', 'save',
                         'show', 'quit')
        print('To use a method pick the\
                   corresponding number ')               
        for mtd in methods:
            print('  ', num, ': ', mtd)
            num += 1
            
                                                
    def useMethod(self):
        try:
            which = int(input('Method? '))
        except ValueError:
            print ('Error: Input not an interger')
            which = None
            
        methods = (self.load, self.resize, self.rotate, 
                          self.flip, self.searchFile,
                          self.grayScale, self.getMethod,
                          self.swapBands, self.waterMark,
                          self.restore, self.save, self.show,
                          self.quit)
        
        if which != None:
            try:
                methods[which-1]()
            except IndexError:
                print('Method not available')
                
                
    def restore(self):
        self.image=self.origin.copy()
         
    def show(self):
        if self.displayPort:
            # give space to the view Port module
            pass
            
    def save(self):
        editorPath='Edited Assets'
        editorPath=path.join(os.getcwd(), editorPath)
        os.makedirs(editorPath, exist_ok=True)
        ask = str(input (
                            'Do you want to save image? ')
                         )
        if ask.lower() == 'y':
            name = str(input('name the file '))
            formatS = '''
                              JPEG
                              PNG
                              BMP
                              GIF
                              PPM
                              TIFF
                              WEBP'''
            print('Supported formats include ',
                       formatS)
            form = ''
            form = str(input('Output format '))
            if not form:
                print('Saving with default format...')
                self.image.save(os.path.join(editorPath,
                                         name)
                                     )
                self.calledSave += 1
            else:
                form =  "."+form.lower()
                try:
                    self.image.save(
                      os.path.join(editorPath, name)+form
                                         )
                except ValueError as vr:
                    print(vr)
                    self.calledSave += 1
                    if self.calledSave < 3:
                        self.save()
                    else:print(f"Cant save file {vr}")
            print('Saved to', editorPath)
        
        
    def quit(self):
        quit()
  
    
        
def imageEditor():
    global editor     
    editor = ImageHandler ()
    editor.load()
    editor.getMethod()
    done = 0
    while not done:
        editor.useMethod()
        if editor.calledSave:
            done=1
            ask = str(input('Do you want to continue? '))
            if ask.lower() == 'y':
                editor = Handler ()
                editor.load()
                #editor.getMethod()
                # commented the above because its
                # already called in the class' body'
                done=0
                
def main(args=None, kwargs=None):
    imageEditor()
    
                      
if __name__ == '__main__':
    main()  
    