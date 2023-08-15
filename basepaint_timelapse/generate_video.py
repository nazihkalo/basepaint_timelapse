import cv2
import numpy as np

# from IPython.display import Video, display


# Convert hex to RGB
def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))

def generate_video(data,palette_mapping_dict, output_file = './timelapse.mp4' ):
  # Given data and palette mapping
  # palette_mapping_dict = {0: '#070B16', 1: '#FDEA73', 2: '#B13F1B', 3: '#20B6D6'}
  # data = [(50, 50, 1), (100, 100, 2), (30, 30, 3), (140, 140, 0)]  # Sample data for demonstration
  # data = df_day_5_list
  
  # Initialize canvas
  canvas_size = (170, 170, 3)
  canvas = np.zeros(canvas_size, dtype=np.uint8)
  
  # Calculate the new FPS
  # Calculate the new FPS
#   new_fps = len(data) / 30
#   new_fps = min(120, new_fps)  # Cap FPS to a maximum of 60
  new_fps = 480
  
  # Create a video writer for MP4 output
  fourcc = cv2.VideoWriter_fourcc(*'H264') # Note the change here
  out = cv2.VideoWriter(output_file, fourcc, new_fps, (170,170))
  
  # Reset the canvas for re-drawing
  canvas = np.zeros(canvas_size, dtype=np.uint8)
  
  # Draw on canvas and save frames
  for (x, y, colorIndex) in data:
      color = hex_to_rgb(palette_mapping_dict[colorIndex])
      canvas[y, x] = color
      out.write(canvas)
  
  # Release video writer
  out.release()
  
