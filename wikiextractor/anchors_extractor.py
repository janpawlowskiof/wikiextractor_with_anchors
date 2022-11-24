import re
from typing import Dict, List


class AnchorExtractor():
    def __init__(self, paragraphs: List[str]) -> None:
        self.pattern = re.compile(r'Anchor::::title=(?P<title>.*?);id=(?P<id>.*?);label=(?P<label>.*?);')
        self.input_paragraphs = paragraphs
        self.output_paragraphs = []
        self.anchors = []

        self.__current_paragraph_parts = []
        self.__current_paragraph_len = 0

        for paragraph_id in range(len(self.input_paragraphs)):
            self.extract_anchors_from_paragraph(paragraph_id)

    def extract_anchors_from_paragraph(self, paragraph_id: int):
        paragraph = self.input_paragraphs[paragraph_id]
        captured_anchors: List[Dict[str, str]] = self.get_capture_groups(paragraph)
        paragraph_parts: List[str] = self.split_by_regex_without_capture_groups(paragraph)
        assert len(paragraph_parts) == len(captured_anchors) + 1, "There must be an error in code, as number of paragraph splits should be 1 more than the number of groups"

        self.reset_current_paragraph()

        for paragraph_part, captured_anchor in zip(paragraph_parts, captured_anchors):
            self.add_part_to_current_paragraph(paragraph_part)
            anchor_start = self.__current_paragraph_len
            self.add_part_to_current_paragraph(captured_anchor["label"])
            anchor_end = self.__current_paragraph_len

            anchor = {
                "text": captured_anchor["label"],
                "paragraph_id": paragraph_id,
                "start": anchor_start,
                "end": anchor_end,
                "wikipedia_id": captured_anchor["id"],
                "wikipedia_title": captured_anchor["title"],
            }
            self.anchors.append(anchor)

        # add last pargraph part, that is behind the last captured group
        self.add_part_to_current_paragraph(paragraph_parts[-1])

        output_paragraph = "".join(self.__current_paragraph_parts)
        self.output_paragraphs.append(output_paragraph)


    def split_by_regex_without_capture_groups(self, paragraph: str) -> List[str]:
        num_capture_groups = self.pattern.groups
        paragraph_split_with_capture_groups = self.pattern.split(paragraph)
        paragraph_split_without_capture_groups = paragraph_split_with_capture_groups[::num_capture_groups+1]
        return paragraph_split_without_capture_groups

    def get_capture_groups(self, paragraph: str) -> List[Dict[str, str]]:
        return [m.groupdict() for m in self.pattern.finditer(paragraph)]
    
    def reset_current_paragraph(self):
        self.__current_paragraph_parts = []
        self.__current_paragraph_len = 0

    def add_part_to_current_paragraph(self, part: str):
        self.__current_paragraph_parts.append(part)
        self.__current_paragraph_len += len(part)
