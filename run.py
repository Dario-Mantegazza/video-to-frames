from video_to_frames import VideoToFramesConverter

if __name__ == "__main__":

    raw_data_path = "/media/manted/manted_data/data/anomaly_detection/step_3_data/raw/"
    output_frames_folder_path = "/media/manted/manted_data/data/anomaly_detection/step_3_data/frames/"
    final_resolution_x = 128
    final_resolution_y = 96
    vc = VideoToFramesConverter(input_path=raw_data_path,
                                output_path=output_frames_folder_path)
    vc.convert()
  