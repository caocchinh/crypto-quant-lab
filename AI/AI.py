import torch
import pandas as pd
import numpy as pd
import matplotlib as plt

scalar = torch.tensor(7)
vector = torch.tensor([7,7])
matrix = torch.tensor([[1,2,3],[4,5,6]])
random = torch.rand(2,2,2,3,4,2,2,1,2,2,4,5,5,2)
image = torch.rand(size=(3,5,5),dtype=torch.float16)
image2 = torch.rand(size=(3,5,5),dtype=torch.float32)

print(image.size(),image.device,image.dtype )

