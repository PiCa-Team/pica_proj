from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Callable, Generator, Optional, Tuple

import cv2
import numpy as np
import pandas as pd
import os

from model.density import density


@dataclass
class VideoInfo:
    """
    A class to store video information, including width, height, fps and total number of frames.

    Attributes:
        width (int): width of the video in pixels
        height (int): height of the video in pixels
        fps (int): frames per second of the video
        total_frames (int, optional): total number of frames in the video, default is None

    Examples:
        ```python
        >>>

        >>> video_info = VideoInfo.from_video_path(video_path='video.mp4')

        >>> video_info
        VideoInfo(width=3840, height=2160, fps=25, total_frames=538)

        >>> video_info.resolution_wh
        (3840, 2160)
        ```
    """

    width: int
    height: int
    fps: int
    total_frames: Optional[int] = None

    @classmethod
    def from_video_path(cls, video_path: str) -> VideoInfo:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise Exception(f"Could not open video at {video_path}")

        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.release()
        return VideoInfo(width, height, fps, total_frames)

    @property
    def resolution_wh(self) -> Tuple[int, int]:
        return self.width, self.height


class VideoSink:
    """
    Context manager that saves video frames to a file using OpenCV.

    Attributes:
        target_path (str): The path to the output file where the video will be saved.
        video_info (VideoInfo): Information about the video resolution, fps, and total frame count.

    Examples:
        ```python
        >>>

        >>> video_info = VideoInfo.from_video_path(video_path='source_video.mp4')

        >>> with VideoSink(target_path='target_video.mp4', video_info=video_info) as s:
        ...     frame = ...
        ...     s.write_frame(frame=frame)
        ```
    """

    def __init__(self, target_path: str, video_info: VideoInfo):
        self.target_path = target_path
        self.video_info = video_info
        self.__fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.__writer = None

    def __enter__(self):
        self.__writer = cv2.VideoWriter(
            self.target_path,
            self.__fourcc,
            self.video_info.fps,
            self.video_info.resolution_wh,
        )
        return self

    def write_frame(self, frame: np.ndarray):
        self.__writer.write(frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        video = self.__writer
        self.__writer.release()



def get_video_frames_generator(source_path: str) -> Generator[np.ndarray, None, None]:
    """
    Get a generator that yields the frames of the video.

    Args:
        source_path (str): The path of the video file.

    Returns:
        (Generator[np.ndarray, None, None]): A generator that yields the frames of the video.

    Examples:
        ```python
        >>>

        >>> for frame in get_video_frames_generator(source_path='source_video.mp4'):
        ...     ...
        ```
    """
    video = cv2.VideoCapture(source_path)
    if not video.isOpened():
        raise Exception(f"Could not open video at {source_path}")
    success, frame = video.read()
    while success:
        yield frame
        success, frame = video.read()
    video.release()

# 승강장 면적
thresholds = 50
def process_video(
    source_path: str,
    save_folder : str,
    target_path: str,
    callback: Callable[[np.ndarray, int], np.ndarray],
    CLASS_ID,
    model
) -> io.BytesIO:
    """
    Process a video file by applying a callback function on each frame and saving the result to a target video file.

    Args:
        source_path (str): The path to the source video file.
        target_path (str): The path to the target video file.
        callback (Callable[[np.ndarray, int], np.ndarray]): A function that takes in a numpy ndarray representation of a video frame and an int index of the frame and returns a processed numpy ndarray representation of the frame.

    Examples:
        ```python
        >>>

        >>> def process_frame(scene: np.ndarray) -> np.ndarray:
        ...     ...

        >>> process_video(
        ...     source_path='source_video.mp4',
        ...     target_path='target_video.mp4',
        ...     callback=process_frame
        ... )
        ```
    """
    source_video_info = VideoInfo.from_video_path(video_path=source_path)
    
    # save_folder 없으면 save_folder 만들어주기
    if not os.path.exists(save_folder) :
        os.mkdir(save_folder)
    
    # df = pd.DataFrame(columns=['COUNT'])
    # 초기 max_count 0으로 설정
    max_count = 0
    with VideoSink(target_path=target_path, video_info=source_video_info) as sink:
        for index, frame in enumerate(
            get_video_frames_generator(source_path=source_path)
        ):
            result_frame, in_count, out_count, count = callback(frame, index, CLASS_ID, model)
            # callback : proccess_frame
            sink.write_frame(frame=result_frame)
            
            # 첫 프레임에서는 max_count가 처음 값
            if index == 0 :
                max_count = count
            
            # count가 max_count보다 높아지면 max_count를 count로 업데이트
            else :
                if max_count < count :
                    max_count = count


            # density 함수 사용하여 밀집도 기준 뽑아내기
            d, density_degree = density(max_count, thresholds)

        result = pd.DataFrame([in_count,out_count, max_count, d, density_degree], index = ['IN', 'OUT','MAX COUNT','DENSITY','DENSITY_DEGREE']).T
        result = result.reset_index().drop(['index'], axis = 1)


        return result