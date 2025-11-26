import hashlib
import os

class Labyrinth:
    def __init__(self):
        self.generated_files = {}

    def generate_next_step(self, current_path: str) -> str:
        """
        Generates a fake 'next file' path based on the current path.
        This creates an infinite graph.
        """
        # Create a deterministic hash based on the path
        hash_object = hashlib.md5(current_path.encode())
        hash_hex = hash_object.hexdigest()[:8]
        
        # Generate a plausible filename
        next_filename = f"secret_config_{hash_hex}.yaml"
        
        # In a real graph, we might want to vary the folder depth
        return os.path.join(os.path.dirname(current_path), "hidden", next_filename)

    def get_content_hint(self, next_path: str) -> str:
        return f"\n\n[REFERENCE] Configuration moved to: {next_path}\n"

labyrinth = Labyrinth()
