import os
import re
import cv2
import numpy as np
from exporters.exporter import Exporter
from utils.image_utils import qimage_to_rgb

class KITTIExporter(Exporter):

    def export(self, frame_index, img1, img2, export_dir):
        img1_rgb = qimage_to_rgb(img1)
        img2_rgb = qimage_to_rgb(img2)

        os.makedirs(os.path.join(export_dir, "flow_occ"), exist_ok=True)
        os.makedirs(os.path.join(export_dir, "image_2"), exist_ok=True)

        idx = f"{frame_index:06d}"  # Use frame index as base filename

        cv2.imwrite(os.path.join(export_dir, "image_2", f"{idx}_10.png"), cv2.cvtColor(img1_rgb, cv2.COLOR_RGB2BGR))
        cv2.imwrite(os.path.join(export_dir, "image_2", f"{idx}_11.png"), cv2.cvtColor(img2_rgb, cv2.COLOR_RGB2BGR))

        flow_h = img1.height()
        flow_w = img1.width()
        flow_img = np.zeros((flow_h, flow_w, 3), dtype=np.uint16)
        flow_img[..., 0] = 1       # occlusion mask
        flow_img[..., 1] = 2**15   # fx = 0 encoded
        flow_img[..., 2] = 2**15   # fy = 0 encoded

        cv2.imwrite(os.path.join(export_dir, "flow_occ", f"{idx}_10.png"), flow_img)
        print(f"Saved frame pair {idx}_10 and {idx}_11 with zero flow.")

