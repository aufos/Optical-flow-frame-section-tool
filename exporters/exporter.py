from abc import ABC, abstractmethod

class Exporter(ABC):
    @abstractmethod
    def export(self, frame_index, img1, img2, export_dir):
        pass