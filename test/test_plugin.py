# %% Imports
import unittest
import os
from libopensesame.experiment import experiment
import PyQt5
# from qtpy.QtWidgets import QApplication

logfile_path = os.path.join(os.path.dirname(__file__), r'./data/tmp.csv')
experiment_path = os.path.join(os.path.dirname(__file__), r'data')

crashing_experiments = [
    "fail_testmarkers_os4_init_twice.osexp",
    "fail_testmarkers_os4_invalid_device_address.osexp",
    "fail_testmarkers_os4_invalid_device_tag.osexp",
    "fail_testmarkers_os4_invalid_marker_value.osexp",
    "fail_testmarkers_os4_invalid_object_dur.osexp",
    "fail_testmarkers_os4_marker_duration_error.osexp",
    "fail_testmarkers_os4_no_init_obj.osexp",
    "fail_testmarkers_os4_no_matching_device_tags.osexp",
    "fail_testmarkers_os4_same_value_twice.osexp",
    "fail_testmarkers_os4_wrong_address.osexp"
]

normal_experiments = [
    "pass_testmarkers_os4_basic.osexp",
    "pass_testmarkers_os4_multiple_devices.osexp",
    "pass_testmarkers_os4_no_marker_objects.osexp"
]

class runExperiments(unittest.TestCase):
    
    def test_runTests(self):
        # app = QApplication([])
                
        for experiment_file in normal_experiments:
            print(f"Testing {experiment_file}")
            e = experiment(
                logfile = logfile_path,
                experiment_path = experiment_path,
                string = os.path.join(experiment_path, experiment_file)
            )
            e.var.canvas_backend = r'legacy'
            e.run()
            self.assertEqual(True, True)
            
    def test_runTestsCrash(self):
        # app = QApplication([])
        for experiment_file in crashing_experiments:
            print(f"Testing {experiment_file}")
            e = experiment(
                logfile = logfile_path,
                experiment_path = experiment_path,
                string = os.path.join(experiment_path, experiment_file)
            )
            e.var.canvas_backend = r'legacy'
            
            with self.assertRaises(Exception) as exception:  # TODO: Exception types!
                e.run()
            print(e)

if __name__ == '__main__':
    unittest.main()
