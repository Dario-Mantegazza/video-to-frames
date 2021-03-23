import errno
import glob
import os
from tqdm import tqdm
import cv2


class VideoToFramesConverter:
    def __init__(self, input_path: str, output_path: str, final_resolution_x: int = None,
                 final_resolution_y: int = None):
        """
        Init of the class
        :param input_path:path of the folder containing the files or path of the file
        :param output_path: path of the output folder
        :param final_resolution_x: optional, use it if you want to resize the video
        :param final_resolution_y: optional, use it if you want to resize the video
        """
        # assert type(final_resolution_x) is int, "final_resolution_x is not an integer: %r" % final_resolution_x
        # assert type(final_resolution_y) is int, "final_resolution_y  is not an integer: %r" % final_resolution_y
        assert self._check_folder(input_path), "input path doesn't exists"
        self._input_path = input_path
        self._output_path = output_path
        self._final_resolution = (final_resolution_x, final_resolution_y)

    def convert(self):
        """
        Call for coverting a video
        :return:
        """
        for video_file in tqdm(glob.glob(self._input_path + "*"), desc="Converting Videos"):
            filename, _ = os.path.splitext(os.path.basename(video_file))
            data_path = os.path.join(self._output_path, filename + "/")
            self._check_create_folder(data_path)
            self._converter_helper(video_file, data_path)
        print("Completed")

    def current_settings(self):
        """
        print current settings
        :return: nothing
        """
        print(f"{self._input_path=}\n{self._output_path=}\n{self._final_resolution=}")

    def change_resolution(self, new_resolution_x: int, new_resolution_y: int):
        """
        change resolution after class init for resizing final frames
        :param new_resolution_x: final width of the frames
        :param new_resolution_y: final height of the frames

        """
        assert type(new_resolution_x) is int, "new_resolution_x is not an integer: %r" % new_resolution_x
        assert type(new_resolution_y) is int, "new_resolution_y is not an integer: %r" % new_resolution_y
        self._final_resolution = (new_resolution_x, new_resolution_y)

    def change_input_path(self, new_path: str):
        """
        change input path after class init
        :param new_path: new input path
        """
        assert self._check_folder(new_path), "new input path doesn't exists"
        self._input_path = new_path

    def change_output_path(self, new_path: str):
        """
        change output path after class init
        :param new_path: new output path
        """
        self._output_path = new_path

    def _converter_helper(self, file: str, subfolder: str):
        vidcap = cv2.VideoCapture(file)
        success, image = vidcap.read()
        count = 0
        width = int(vidcap.get(3))
        height = int(vidcap.get(4))
        if self._final_resolution[0] is None or self._final_resolution[1] is None:
            self._final_resolution = (width, height)
        while success:
            if width > self._final_resolution[0]:
                frame = cv2.resize(image, self._final_resolution, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            else:
                frame = image

            cv2.imwrite(
                os.path.join(
                    subfolder,
                    f"{count}".zfill(6) +
                    f"_{self._final_resolution[0]}_{self._final_resolution[1]}.jpg"),
                frame)  # save frame as JPEG file
            success, image = vidcap.read()
            count += 1

    @staticmethod
    def _check_folder(folder_path: str):
        return os.path.exists(os.path.dirname(folder_path))

    @staticmethod
    def _check_create_folder(folder_path: str):
        if not os.path.exists(os.path.dirname(folder_path)):
            try:
                os.makedirs(os.path.dirname(folder_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
