def convert_image_to_img_source(image_file: str) -> str:
    """
    Loads an image file and base64-encodes it as an HTML 'img' source.

    Notes:
        The file ending is used as the source file type.

    Args:
        image_file: The image file to load.

    Returns:
        The 'img' source attribute.
    """
    import base64
    import pathlib

    with open(image_file, "rb") as img:
        img_data = base64.b64encode(img.read()).decode()
        suffix = pathlib.Path(image_file).suffix.replace(".", "").lower()
        return f"data:image/{suffix};base64,{str(img_data)}"
