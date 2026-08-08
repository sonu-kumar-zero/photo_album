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
    ) -> QRectF:
        """Resize the image to fit within the specified dimensions while maintaining aspect ratio."""
        # Implement the resizing logic here
        
        new_rect = QRectF(rect)
        
        if handle == HandlePosition.BOTTOM_RIGHT:
            new_rect.setWidth(
                max(
                    min_width, 
                    rect.width() + delta.x()
                )
            )
            new_rect.setHeight(
                max(
                    min_height, 
                    rect.height() + delta.y()
                )
            )
        elif handle == HandlePosition.RIGHT:
            new_rect.setWidth(
                max(
                    min_width, 
                    rect.width() + delta.x()
                )
            )

        elif handle == HandlePosition.LEFT:
            new_left = rect.left() + delta.x()
            
            new_left = min(
                new_left, 
                rect.right() - min_width
            )
            
            new_rect.setLeft(new_left)

        elif handle == HandlePosition.BOTTOM_CENTER:
            new_rect.setHeight(
                max(
                    min_height, 
                    rect.height() + delta.y()
                )
            )

        elif handle == HandlePosition.TOP_CENTER:
            new_top = rect.top() + delta.y()
            
            new_top = min(
                new_top, 
                rect.bottom() - min_height
            )
            
            new_rect.setTop(new_top)
            
        elif handle == HandlePosition.TOP_LEFT:
            new_left = rect.left() + delta.x()
            new_top = rect.top() + delta.y()
            
            new_left = min(
                new_left, 
                rect.right() - min_width
            )
            new_top = min(
                new_top, 
                rect.bottom() - min_height
            )
            
            new_rect.setLeft(new_left)
            new_rect.setTop(new_top)

        elif handle == HandlePosition.TOP_RIGHT:
            new_top = rect.top() + delta.y()
            
            new_top = min(
                new_top, 
                rect.bottom() - min_height
            )
            
            new_rect.setTop(new_top)
            new_rect.setWidth(
                max(
                    min_width, 
                    rect.width() + delta.x()
                )
            )
        
        elif handle == HandlePosition.BOTTOM_LEFT:
            new_left = rect.left() + delta.x()
            
            new_left = min(
                new_left, 
                rect.right() - min_width
            )
            
            new_rect.setLeft(new_left)
            new_rect.setHeight(
                max(
                    min_height, 
                    rect.height() + delta.y()
                )
            )
            

        return new_rect