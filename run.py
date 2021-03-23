from video_to_frames import VideoToFramesConverter

if __name__ == "__main__":
    raw_data_path = "/path/to/video/folder/"
    output_frames_folder_path = "/path/to/frames/"

    # this create frames at the same video resolution
    vc = VideoToFramesConverter(
        input_path=raw_data_path,
        output_path=output_frames_folder_path,
    )
    vc.convert()
    final_resolution_x = 128
    final_resolution_y = 96

    # this create frames at lower resolution
    vc2 = VideoToFramesConverter(
        input_path=raw_data_path,
        output_path=output_frames_folder_path, final_resolution_x=final_resolution_x,
        final_resolution_y=final_resolution_y,
    )
    vc2.convert()

    # if you forgot some settings you can always print them
    vc2.current_settings()
    # and change them
    vc2.change_input_path("/new/path/to/video/files")
    vc2.change_output_path("/new/output/path")
    vc2.change_resolution(new_resolution_x=16, new_resolution_y=9)
    vc2.convert()