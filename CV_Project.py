# -*- coding: utf-8 -*-
"""Final_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TZj8wy4TipolFsShUSAqhhvTDlXLZAzj
"""



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import cv2
import time
import matplotlib.pyplot as plt


from base64 import b64decode
import time
from transformers import CLIPProcessor, CLIPModel
import torch
from torchvision import transforms
import matplotlib.patches as patches2






# define processor and model
model_id = "openai/clip-vit-base-patch32"

processor = CLIPProcessor.from_pretrained(model_id)
model = CLIPModel.from_pretrained(model_id)

# move model to device if possible
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model.to(device)
color = (255, 0, 0)
print(device)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 2
QUERIES = [
"phone",
"bottle"
]
cam = cv2.VideoCapture(0)


while(True):

  result, camimage = cam.read()

  # transform the image into tensor
  transform = transforms.ToTensor()
  temp = camimage
  rgb = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
  img = transform(rgb).to(device)
  
  img.data.shape
  Tmax = ''
  Smax = 0 
  for querie in QUERIES:
      inputs = processor(
              images=[rgb],  # big patch image sent to CLIP
              return_tensors="pt",  # tell CLIP to return pytorch tensor
              text=querie,  # class label sent to CLIP
              padding=True
          ).to(device)
      score = model(**inputs).logits_per_image.item()
      if score > Smax:
        Tmax = querie
        Smax = score
  print(Tmax)

  patches = img.data.unfold(0,3,3)

# break the image into patches (in height dimension)
  patch = 64

  patches = patches.unfold(1, patch, patch)

# break the image into patches (in width dimension)
  patches = patches.unfold(2, patch, patch)
  
  patches = patches.to(device)
  window = 6
  stride = 1

  scores = torch.zeros(patches.shape[1], patches.shape[2])
  runs = torch.ones(patches.shape[1], patches.shape[2])

  for Y in range(0, patches.shape[1]-window+1, stride): 
      for X in range(0, patches.shape[2]-window+1, stride):
          big_patch = torch.zeros(patch*window, patch*window, 3)
          patch_batch = patches[0, Y:Y+window, X:X+window]
          for y in range(window):
              for x in range(window):
                  big_patch[
                      y*patch:(y+1)*patch, x*patch:(x+1)*patch, :
                  ] = patch_batch[y, x].permute(1, 2, 0)
        # we preprocess the image and class label with the CLIP processor
          inputs = processor(
              images=big_patch,  # big patch image sent to CLIP
              return_tensors="pt",  # tell CLIP to return pytorch tensor
              text=Tmax,  # class label sent to CLIP
              padding=True
          ).to(device) # move to device if possible

        # calculate and retrieve similarity score
          score = model(**inputs).logits_per_image.item()
        # sum up similarity scores from current and previous big patches
        # that were calculated for patches within the current window
          scores[Y:Y+window, X:X+window] += score
        # calculate the number of runs on each patch within the current window
          runs[Y:Y+window, X:X+window] += 1

# # average score for each patch
  scores /= runs

# transform the patches tensor 
  adj_patches = patches.squeeze(0).permute(3, 4, 2, 0, 1).to('cpu')
# normalize scores
  scores = (
      scores - scores.min()) / (scores.max() - scores.min()
  )
# multiply patches by scores

  adj_patches = adj_patches * scores
# rotate patches to visualize
  adj_patches = adj_patches.permute(3, 4, 2, 0, 1)

# clip the scores' interval edges
  for _ in range(1):
      scores = np.clip(scores-scores.mean(), 0, np.inf)

# normalize scores
  scores = (
      scores - scores.min()) / (scores.max() - scores.min()
  )

  scores.shape, patches.shape

# transform the patches tensor 
  adj_patches = patches.squeeze(0).permute(3, 4, 2, 0, 1).to('cpu')
  adj_patches.shape

# multiply patches by scores
  adj_patches = adj_patches * scores
# rotate patches to visualize
  adj_patches = adj_patches.permute(3, 4, 2, 0, 1)
  adj_patches.shape

  detection = scores > 0.55
  np.nonzero(detection)
  y_min, y_max = (
      np.nonzero(detection)[:,0].min().item(),
      np.nonzero(detection)[:,0].max().item()+1
  )
  y_min, y_max
  x_min, x_max = (
      np.nonzero(detection)[:,1].min().item(),
      np.nonzero(detection)[:,1].max().item()+1
  )
  x_min, x_max
  y_min *= patch
  y_max *= patch
  x_min *= patch
  x_max *= patch
  x_min, y_min
  height = y_max - y_min
  width = x_max - x_min

  
  rect = cv2.rectangle(camimage, (x_min, y_min), (x_max, y_max), color, 2)
  rectimg = cv2.putText(rect, Tmax, (x_min,y_max-20) , font, fontScale, color,2, cv2.LINE_AA)
                           
  cv2.imshow("Live",rect)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break
      
cam.release()
cv2.destroyAllWindows()
