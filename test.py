import tkinter
import unittest
from main import MainApplication

class TestApplication(unittest.TestCase):
    
    def setUp(self) -> None:
        self.app = MainApplication() 

    
    def test_all_views_load(self):
        """Ensure all views load without error."""
        
        all_views = self.app.view_map.keys()
        
        for view in all_views:
            try:
                self.app.switch_to_view(view)
            except:
                self.fail(f"View {view} failed to load.")

if __name__ == "__main__":
    unittest.main()