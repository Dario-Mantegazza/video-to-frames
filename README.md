# video-to-frames
A Python class for converting a video to multiple frames. Used for creating datasets for CNNs from videos

# Basic use
This bit of code creates frames at the same video resolution

```
raw_data_path = "/path/to/video/folder/"
output_frames_folder_path = "/path/to/frames/"

vc = VideoToFramesConverter(
    input_path=raw_data_path,
    output_path=output_frames_folder_path,
)

vc.convert()
```
This creates frames at lower resolution

```
final_resolution_x = 128
final_resolution_y = 96

vc = VideoToFramesConverter(
    input_path=raw_data_path,
    output_path=output_frames_folder_path, final_resolution_x=final_resolution_x,
    final_resolution_y=final_resolution_y,
)
vc.convert()
```
If you forgot some settings you can always print themand change them
```
raw_data_path = "/path/to/video/folder/"
output_frames_folder_path = "/path/to/frames/"

vc = VideoToFramesConverter(
    input_path=raw_data_path,
    output_path=output_frames_folder_path,
)

vc.current_settings()
vc.change_input_path("/new/path/to/video/files")
vc.change_output_path("/new/output/path")
vc.change_resolution(new_resolution_x=16, new_resolution_y=9)
vc.convert()
```
