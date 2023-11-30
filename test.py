import tkinter
import unittest
from main import MainApplication

class TestApplication(unittest.TestCase):
    
    def setUp(self) -> None:
        self.app = MainApplication(testing=True) 

    
    def test_all_views_load(self):
        """Ensure all views load without error."""
        
        all_views = self.app.view_map.keys()
        
        for view in all_views:
            try:
                
                
                # Add global state where required
                if view == "plan_detail":
                    self.app.GLOBAL_STATE['plan_name'] = 'Plan 0'
                elif view == "camp_detail":
                    self.app.GLOBAL_STATE['camp_id_to_view'] = 1
                elif view == "edit_resources":
                    self.app.GLOBAL_STATE['camp_id_for_resources'] = 1
                elif view == "add_edit_camp":
                    self.app.GLOBAL_STATE['plan_id_for_camp'] = 1
                    self.app.GLOBAL_STATE['camp_id'] = 1
                elif view == "refugee_profile":
                    self.app.GLOBAL_STATE['refugee_id_to_view'] = 1

                
                self.app.switch_to_view(view)
            except:
                self.fail(f"View {view} failed to load.")

if __name__ == "__main__":
    unittest.main()