import numpy as np
from PIL import Image,ImageEnhance,ImageOps,ImageFont,ImageDraw
import os
import sys

def sum_tiffStack(tiff_stack):
 tiff_img = Image.open(tiff_stack)
 tiff_stack = []
 for i in range(tiff_img.n_frames):
  tiff_img.seek(i)
  tiff_stack.append(np.array(tiff_img))
 return np.array(tiff_stack)

tiff_stack=sys.argv[1]
string_file=sys.argv[2]
annotate_images=sys.argv[3]

if annotate_images=='yes':
 with open (string_file, "r") as myfile:
  string=myfile.readlines()

summed_image=np.sum(sum_tiffStack(tiff_stack),axis=0)
scale_factor=sum_tiffStack(tiff_stack).shape[2]/960
summed_image = 255*(summed_image - np.min(summed_image))/np.ptp(summed_image).astype(int)
summed_image = (summed_image).astype('uint8')

if annotate_images=='yes':
 summed_image=np.pad(summed_image, ((int(150*scale_factor),0),(0,0)), 'constant',constant_values=(summed_image.min()))
 im=Image.fromarray(summed_image)
 draw = ImageDraw.Draw(im)
 font = ImageFont.truetype(r'/share/Arial.ttf', int(16*scale_factor))
 draw.text((0, int(0*scale_factor)),string[0],fill=(int(summed_image.max())),font=font)
 scale_length=float([s for s in string[0].split() if s.replace('.','',1).isdigit()][-1])
 pix_size=float([s for s in string[1].split() if s.replace('.','',1).isdigit()][-1])/10
 draw.line((int(50*scale_factor),int(200*scale_factor),int((50+scale_length/pix_size)*scale_factor),int(200*scale_factor)), fill=0,width=int(5*scale_factor))
 draw.text((0, int(25*scale_factor)),string[1],fill=(int(summed_image.max())),font=font)
 draw.text((0, int(50*scale_factor)),string[2],fill=(int(summed_image.max())),font=font)
 draw.text((0, int(75*scale_factor)),string[3],fill=(int(summed_image.max())),font=font)
 draw.text((0, int(100*scale_factor)),string[4],fill=(int(summed_image.max())),font=font)
 draw.text((0, int(125*scale_factor)),string[5],fill=(int(summed_image.max())),font=font)
 im=ImageOps.autocontrast(im, cutoff=5, ignore=None)
else:
 im=Image.fromarray(summed_image)
os.remove(tiff_stack)
im.save(tiff_stack[:-5]+'.tif')
os.remove(string_file)
