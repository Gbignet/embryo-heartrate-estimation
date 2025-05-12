# Heart Rate Detection from Video

This project uses OpenCV to analyze an infrared video of a chicken heart and estimate its heart rate by detecting variations in contour areas.

## 📁 Project Structure

project

-> main.py

-> requirements.txt

-> day3_chicken_heartbeat.mp4

-> README.md



---

## ⚙️ Installation

1. **Clone the repository (if needed)**  
   Or simply place all the files in the same folder.

2. **Create a virtual environment (optional but always recommended)**


```bash
python -m venv venv
venv\Scripts\activate  # On Windows

3. Install dependencies

pip install -r requirements.txt

From the project/ folder, run:

python main.py


❗ Notes
If you get an error related to cv2.imshow, make sure you are not using opencv-python-headless.


Work is separated into multiple parts:

Step 0: The video will be "cut" into frames that we will analyse separately


Step 1: Image are usually opened in the RGB format (or some variation of it). In our current use case, the value of green, blue and red wont help as much
for the segmentation process.
We will convert the frame into a HSV format
(but HSV images here)
This part will facillitate the segmentation process by having a threshold



Part 2 dealing with noise:
Our image is met with noise due to the poor quality of the video. The noise is removed using an opening, which is an erosion followed by a dilation (the white noise are removed with dilation and the dilation is here to prevent the AoI(Area of Interrest) from shrinking)

![Mask Image](Project/snapshot/mask.jpg)
![Open_Morph](Project/snapshot/opening_morph.jpg)


Notice: As you can see, the opening isnt perfect, but we know the region of interrest is present along with some clutter
I decide to choose the largest area. This is choosen in favor of having a stricter threshold because it might fail to detect the AoI in some frames

Part 3: beat detection:

Now that we have our AoI we will use it to determine the heartrate..
As the embryo heart "beat", the RoI becomes larger and spikes at a maximum area values before going back down.
A heartbeat is determined when it detects the local maximum area.

