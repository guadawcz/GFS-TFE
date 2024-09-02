import random
import math
import torch
import numpy as np



class CutMix:
    def __init__(self, probability=0.5, min_area=0.02, max_area=1/3, device='cuda'):
        self.probability = probability
        self.min_area = min_area
        self.max_area = max_area
        self.device = device

    def _cutmix(self, x1, x2, width):
        if random.random() > self.probability:
            target_area = random.uniform(self.min_area, self.max_area) * width
            w = int(target_area)
            left = random.randint(0, width - w)
            x1[..., left:left + w] = x2[..., left:left + w]

    def __call__(self, input, labels):
        # print("dnbzdnzdnzdnSDN",input.size())
        batch_size, chan, width = input.size()
        labels = labels.cpu()
        types = torch.unique(labels).tolist()
        for c in types:
            idxes = torch.where(labels == c)[0].tolist()
            for i in range(len(idxes)-1):
                self._cutmix(input[idxes[i]], input[idxes[i+1]], width)
        return input
