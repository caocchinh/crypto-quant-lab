from tqdm import tqdm


class ProgressBar:
    def __init__(self, length: int, description: str):
        self.length = length
        self.description = description

    def progressBar(self):
        for i in tqdm(range(self.length), position=0, leave=True, desc=self.description):
            yield
