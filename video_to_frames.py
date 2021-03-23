import errno
import glob
import os
from tqdm import tqdm
import cv2


class VideoToFramesConverter:
    def __init__(self, input_path: str, output_path: str, final_resolution_x: int = None,
                 final_resolution_y: int = None):
        """

        :param input_path:
        :param output_path:
        :param final_resolution_x:
        :param final_resolution_y:
        """
        assert type(final_resolution_x) is int, "final_resolution_x is not an integer: %r" % final_resolution_x
        assert type(final_resolution_y) is int, "final_resolution_y  is not an integer: %r" % final_resolution_y
        assert self._check_folder(input_path), "input path doesn't exists"
        self.input_path = input_path
        self.output_path = output_path
        self.final_resolution = (final_resolution_x, final_resolution_y)

    def convert(self):
        """

        :return:
        """
        for video_file in tqdm(glob.glob(self.input_path + "*"), desc="Converting Videos"):
            filename, _ = os.path.splitext(os.path.basename(video_file))
            data_path = os.path.join(self.output_path, filename + "/")
            self._check_create_folder(data_path)
            self._converter_helper(video_file, data_path)
        print("Completed")

    def convert_passed_file(self, video_file: str):
        """

        :param video_file:
        :return:
        """
        filename, _ = os.path.splitext(os.path.basename(video_file))
        data_path = os.path.join(self.output_path, filename)
        self._check_create_folder(data_path)
        self._converter_helper(video_file, data_path)

    def current_settings(self):
        """

        :return:
        """
        print(f"{self.input_path=}\n{self.output_path=}\n{self.final_resolution=}")

    def change_resolution(self, new_resolution_x: int, new_resolution_y: int):
        """

        :param new_resolution_x:
        :param new_resolution_y:
        :return:
        """
        assert type(new_resolution_x) is int, "new_resolution_x is not an integer: %r" % new_resolution_x
        assert type(new_resolution_y) is int, "new_resolution_y  is not an integer: %r" % new_resolution_y
        self.final_resolution = (new_resolution_x, new_resolution_y)

    def change_input_path(self, new_path: str):
        """

        :param new_path:
        :return:
        """
        assert self._check_folder(new_path), "new input path doesn't exists"
        self.input_path = new_path

    def change_output_path(self, new_path: str):
        """

        :param new_path:
        :return:
        """
        self.output_path = new_path

    def _converter_helper(self, file: str, subfolder: str):
        vidcap = cv2.VideoCapture(file)
        success, image = vidcap.read()
        count = 0
        if self.final_resolution[0] is None or self.final_resolution[1] is None:
            width = vidcap.get(3)
            height = vidcap.get(4)
        while success:
            frame = cv2.resize(image, self.final_resolution, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(subfolder, f"{count}".zfill(
                6) + f"_{self.final_resolution[0]}_{self.final_resolution[1]}.jpg"),
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
