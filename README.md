# Optical Flow Frame Selection Tool

This is a lightweight annotation tool designed specifically for evaluating real-world optical flow datasets under **zero-motion ground truth** conditions, such as those with only **lighting changes** — as used in our paper.

It enables precise frame pair selection from videos and exports them in **KITTI optical flow format**. The tool is tailored for scenarios where the ground truth flow is expected to be **zero** (i.e., no object or camera motion), ideal for testing how well models distinguish true motion from illumination artifacts.

---

## 📄 Dataset

The frame pairs selected and exported using this tool form the dataset used in our paper and are available in the folder:
dataset_kitti_format/

They follow the official [KITTI optical flow format](http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=flow) for direct compatibility with existing models like [RAFT](https://github.com/princeton-vl/RAFT).

---

## 📚 Paper

This tool and dataset were developed as part of our research project on real-world evaluation of optical flow with varying lighting conditions.
The paper will be available at: Link to be added.
<!-- **[your-paper-link-here]** -->

---

## ⚙️ Features

- Load videos in `.mp4`, `.avi`, `.mov` formats
- Navigate and select frame pairs using:
  - Slider
  - Timestamp input (for coarse selection)
  - _Previous_ / _Next_ buttons (for fine selection)
- Define frame offset (how many frames apart the pair should be)
- Zoom into both frames for pixel-level comparison
- Export frame pairs in **KITTI optical flow format** with a single click

---

## 🛠️ How to Use

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
2. Install the required Python dependencies, run:
    ```bash
    pip install -r requirements.txt
3. Run the tool:
    ```bash
    python main.py
4. In the GUI:
- Load your input video
- Select two frames using the slider, timestamps, or buttons
- Click "Save Frames"
- The selected frame pair will be saved in KITTI format in the directory you specify


## 🔁 Want to Annotate Non-Zero Flow?

If you're interested in manually annotating optical flow for non-zero motion cases, please refer to the tool developed by my group members: https://github.com/IrisPetre99/RP3000.


## 📝 Acknowledgements

This tool was developed as part of the [CSE3000 Research Project](http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=flow) in the Computer Science and Engineering program at [Delft University of Technology (TU Delft)](https://https//github.com/TU-Delft-CSE).

Special thanks to the guidance and support of my supervior, responsible professor and all group members throughout this project.


<!-- 
## Current functionality:

This tool was designed to import and select frames in videos to be used in the evaluation of real-world optical flow datasets. Currently, the tool supports the following functionatilies:

- Import of a video (.mp4, .avi, .mov)
- Selection of frames through a slider.
- Selection of frames via a timestamp input. Used for general. Most hollistic approach. 
- Selection of frames via _Previous_ and _Next_ Buttons. Most granular approach.
- An offset input field, which shows how many many frames apart the two images are. By default, this is set to 1.
- The ability to zoom both images, such that pixels can be very clearly mapped and located between frames. 
- The ability to export the selected frame pairs in KITTI format. -->

