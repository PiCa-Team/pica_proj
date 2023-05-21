from typing import Optional, Tuple

import cv2
import numpy as np

from model.supervision.detection.core import Detections
from model.supervision.detection.utils import generate_2d_mask
from model.supervision.draw.color import Color
from model.supervision.draw.utils import draw_polygon, draw_text
from model.supervision.geometry.core import Position
from model.supervision.geometry.utils import get_polygon_center
from model.supervision.geometry.core import Point

class PolygonZone:
    def __init__(
        self,
        polygon: np.ndarray,
        frame_resolution_wh: Tuple[int, int],
        triggering_position: Position = Position.BOTTOM_CENTER,
    ):
        self.polygon = polygon
        self.frame_resolution_wh = frame_resolution_wh
        self.triggering_position = triggering_position
        self.mask = generate_2d_mask(polygon=polygon, resolution_wh=frame_resolution_wh)
        self.current_count = 0

    def trigger(self, detections: Detections) -> np.ndarray:
        anchors = (
            np.ceil(
                detections.get_anchor_coordinates(anchor=self.triggering_position)
            ).astype(int)
            - 1
        )
        is_in_zone = self.mask[anchors[:, 1], anchors[:, 0]]
        self.current_count = np.sum(is_in_zone)
        return is_in_zone.astype(bool), self.current_count


class PolygonZoneAnnotator:
    def __init__(
        self,
        zone: PolygonZone,
        color: Color,
        thickness: int = 2,
        text_color: Color = Color.black(),
        text_scale: float = 0.5,
        text_thickness: int = 1,
        text_padding: int = 10,
    ):
        self.zone = zone
        self.color = color
        self.thickness = thickness
        self.text_color = text_color
        self.text_scale = text_scale
        self.text_thickness = text_thickness
        self.text_padding = text_padding
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.center = get_polygon_center(polygon=zone.polygon)

    def annotate(self, scene: np.ndarray, label: Optional[str] = None) -> np.ndarray:
        annotated_frame = draw_polygon(
            scene=scene,
            polygon=self.zone.polygon,
            color=self.color,
            thickness=self.thickness,
        )

        # 상자 위치 조절 및 텍스트 입력 부분
        annotated_frame = draw_text(
            scene=annotated_frame,
            text='CNT: '+str(self.zone.current_count) if label is None else label,
            text_anchor=Point(10,100),
            background_color=Color.black(),
            text_color=self.text_color,
            text_scale=self.text_scale,
            text_thickness=self.text_thickness,
            text_padding=self.text_padding,
            text_font=self.font,
        )

        return annotated_frame
