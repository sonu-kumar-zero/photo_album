from PySide6.QtCore import QPointF, QRectF
from items.enums.handle_position import HandlePosition

class ResizeAlgorithm:
    
    @staticmethod
    def resize(
        rect: QRectF,
        handle: HandlePosition,
        delta: QPointF,
        min_width: float,
        min_height: float,
        keep_aspect_ratio: bool = False
    ) -> QRectF:
        """Resize the image to fit within the specified dimensions while maintaining aspect ratio."""
        # Implement the resizing logic here
        
        if handle in {
            HandlePosition.TOP_LEFT,
            HandlePosition.TOP_RIGHT,
            HandlePosition.BOTTOM_LEFT,
            HandlePosition.BOTTOM_RIGHT
        }:
            return ResizeAlgorithm._resize_corner(
                rect=rect,
                handle=handle,
                delta=delta,
                min_width=min_width,
                min_height=min_height,
                keep_aspect_ratio=keep_aspect_ratio
            )
            
        return ResizeAlgorithm._resize_edge(
            rect=rect,
            handle=handle,
            delta=delta,
            min_width=min_width,
            min_height=min_height,
            keep_aspect_ratio=keep_aspect_ratio
        )
        
    @staticmethod
    def _resize_corner(
        rect: QRectF,
        handle: HandlePosition,
        delta: QPointF,
        min_width: float,
        min_height: float,
        keep_aspect_ratio: bool,
    ) -> QRectF:

        aspect_ratio = (
            rect.width() / rect.height()
            if rect.height() > 0
            else 1.0
        )

        width_delta = delta.x()
        height_delta = delta.y()

        if handle in {
            HandlePosition.TOP_LEFT,
            HandlePosition.BOTTOM_LEFT,
        }:
            width_delta = -width_delta

        if handle in {
            HandlePosition.TOP_LEFT,
            HandlePosition.TOP_RIGHT,
        }:
            height_delta = -height_delta

        width = max(
            min_width,
            rect.width() + width_delta,
        )

        height = max(
            min_height,
            rect.height() + height_delta,
        )

        if keep_aspect_ratio:
            width_change = abs(width - rect.width())
            height_change = abs(height - rect.height())

            if width_change >= height_change:
                height = width / aspect_ratio
            else:
                width = height * aspect_ratio

            width = max(min_width, width)
            height = max(min_height, height)

        # Keep the opposite corner fixed.
        if handle == HandlePosition.BOTTOM_RIGHT:
            return QRectF(
                rect.left(),
                rect.top(),
                width,
                height,
            )

        if handle == HandlePosition.BOTTOM_LEFT:
            return QRectF(
                rect.right() - width,
                rect.top(),
                width,
                height,
            )

        if handle == HandlePosition.TOP_RIGHT:
            return QRectF(
                rect.left(),
                rect.bottom() - height,
                width,
                height,
            )

        if handle == HandlePosition.TOP_LEFT:
            return QRectF(
                rect.right() - width,
                rect.bottom() - height,
                width,
                height,
            )

        return QRectF(rect)     
        

    @staticmethod
    def _resize_edge(
        rect: QRectF,
        handle: HandlePosition,
        delta: QPointF,
        min_width: float,
        min_height: float,
        keep_aspect_ratio: bool,
    ) -> QRectF:

        new_rect = QRectF(rect)

        aspect_ratio = (
            rect.width() / rect.height()
            if rect.height() > 0
            else 1.0
        )

        if handle == HandlePosition.LEFT:
            new_left = min(
                rect.left() + delta.x(),
                rect.right() - min_width,
            )

            width = rect.right() - new_left

            if keep_aspect_ratio:
                height = max(
                    min_height,
                    width / aspect_ratio,
                )

                center_y = rect.center().y()

                new_rect = QRectF(
                    new_left,
                    center_y - height / 2,
                    width,
                    height,
                )
            else:
                new_rect.setLeft(new_left)

        elif handle == HandlePosition.RIGHT:
            width = max(
                min_width,
                rect.width() + delta.x(),
            )

            if keep_aspect_ratio:
                height = max(
                    min_height,
                    width / aspect_ratio,
                )

                center_y = rect.center().y()

                new_rect = QRectF(
                    rect.left(),
                    center_y - height / 2,
                    width,
                    height,
                )
            else:
                new_rect.setWidth(width)

        elif handle == HandlePosition.TOP_CENTER:
            new_top = min(
                rect.top() + delta.y(),
                rect.bottom() - min_height,
            )

            height = rect.bottom() - new_top

            if keep_aspect_ratio:
                width = max(
                    min_width,
                    height * aspect_ratio,
                )

                center_x = rect.center().x()

                new_rect = QRectF(
                    center_x - width / 2,
                    new_top,
                    width,
                    height,
                )
            else:
                new_rect.setTop(new_top)

        elif handle == HandlePosition.BOTTOM_CENTER:
            height = max(
                min_height,
                rect.height() + delta.y(),
            )

            if keep_aspect_ratio:
                width = max(
                    min_width,
                    height * aspect_ratio,
                )

                center_x = rect.center().x()

                new_rect = QRectF(
                    center_x - width / 2,
                    rect.top(),
                    width,
                    height,
                )
            else:
                new_rect.setHeight(height)

        return new_rect

