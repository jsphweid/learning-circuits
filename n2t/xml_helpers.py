def formulate_line(xml_tag_text: str, content: str) -> str:
    special_char_mapping = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
    }
    formatted_content = special_char_mapping[content] if content in special_char_mapping else content
    return f"<{xml_tag_text}> {formatted_content} </{xml_tag_text}>"
