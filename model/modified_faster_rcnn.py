import os
import numpy as np
import torch
import torch.utils.data
from PIL import Image
import timm
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator
from .IA_faster_rcnn import FasterRCNNIA
from model.backbone import TimmToVisionFPN, TimmToVision, resnet50_fpn, calculate_param


def get_model(num_classes):
    # load an instance segmentation model pre-trained on COCO
    # without FPN
    # m = timm.create_model('cspresnet50', pretrained=True, num_classes=0, global_pool='')
    # backbone = TimmToVision(m, 1024)

    # with FPN
    m = timm.create_model('cspresnet50', features_only=True, pretrained=True)
    backbone = TimmToVisionFPN(m)
    # ["0"] rather than [0]
    # roi_pooler = torchvision.ops.MultiScaleRoIAlign(featmap_names=['0', '1', '2', '3'],
    #                                                output_size=7,
    #                                                sampling_ratio=2)

    ## Faster RCNN with inverted attention module
    model = FasterRCNNIA(backbone, num_classes=num_classes)

    return model


