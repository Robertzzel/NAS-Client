class FileDetails:
    def __init__(self, name, size, is_dir):
        self.name = name
        self.size = size
        self.is_dir = is_dir

    def __str__(self):
        return f"FileDetails: Name={self.name}, Size={self.size}, IsDir={self.is_dir}"