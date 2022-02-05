"""
Yellow Nameplate: [Blur, Mask, Gray, Canny, Dilate, Contour]
White Nameplate: [Blur, Brightness, Contrast, Mask, Gray, Canny, Dilate, Erode, Contour]
"""
import numpy as np

LOCATIONS = {
    'chat': (0, 700, 450, 380),
    'mini_map': (1670, 0, 320, 280),
    'mini_map_cropped': (1730, 45, 130, 130),
    'portrait': (0, 0, 320, 140),
    'skill_bar': (450, 960, 1040, 120)
}

RECOGNITION = {
    'nameplates': {
        'colors': {
            'yellow': {
                'gaussian_blur': {
                    'kernel': (7, 7),
                    'sigma_x': 7
                },
                'mask': {
                    'lower_hue': 30,
                    'lower_saturation': 215,
                    'lower_value': 80,
                    'upper_hue': 45,
                    'upper_saturation': 240,
                    'upper_value': 255
                },
                'canny': {
                    'threshold_1': 120,
                    'threshold_2': 120
                },
                'dilation': {
                    'kernel': np.ones((5, 5), np.uint8),
                    'iterations': 9
                },
                'erosion': {
                    'kernel': np.ones((5, 5), np.uint8),
                    'iterations': 3
                },
                'contour': {
                    'min_area': 1500,
                    'max_area': 10000
                }
            },
            'white': {
                'gaussian_blur': {
                    'kernel': (5, 5),
                    'sigma_x': 2
                },
                'brightness': {
                    'level': 0
                },
                'contrast': {
                    'level': 55
                },
                'mask': {
                    'lower_hue': 0,
                    'lower_saturation': 0,
                    'lower_value': 5,
                    'upper_hue': 100,
                    'upper_saturation': 100,
                    'upper_value': 150
                },
                'canny': {
                    'threshold_1': 140,
                    'threshold_2': 140
                },
                'dilation': {
                    'kernel': np.ones((5, 5), np.uint8),
                    'iterations': 12
                },
                'erosion': {
                    'kernel': np.ones((5, 5), np.uint8),
                    'iterations': 7
                },
                'contour': {
                    'min_area': 1000,
                    'max_area': 15000
                }
            }
        }
    },
    'objects': {
        'mini_map': {
            'crafting_facility': {
                'gaussian_blur': {
                    'kernel': (3, 3),
                    'sigma_x': 17
                },
                'brightness': {
                    'value': 0
                },
                'contrast': {
                    'value': 15
                },
                'mask': {
                    'lower_hue': 21,
                    'lower_saturation': 180,
                    'lower_value': 185,
                    'upper_hue': 30,
                    'upper_saturation': 255,
                    'upper_value': 255
                },
                'canny': {
                    'threshold_1': 120,
                    'threshold_2': 120
                },
                'dilation': {
                    'kernel': np.ones((3, 3), np.uint8),
                    'iterations': 11
                },
                'erosion': {
                    'kernel': np.ones((5, 5), np.uint8),
                    'iterations': 4
                },
                'contour': {
                    'min_area': 280,
                    'max_area': 4000
                }
            },
            'character_marker': {
                'gaussian_blur': {
                    'kernel': (15, 15),
                    'sigma_x': 2
                },
                'brightness': {
                    'level': 5
                },
                'mask': {
                    'lower_hue': 0,
                    'lower_saturation': 160,
                    'lower_value': 120,
                    'upper_hue': 18,
                    'upper_saturation': 255,
                    'upper_value': 255,
                },
                'canny': {
                    'threshold_1': 120,
                    'threshold_2': 120
                },
                'dilation': {
                    'kernel': np.ones((5, 5), np.uint8),
                    'iterations': 1
                },
                'erosion': {
                    'kernel': np.ones((3, 3), np.uint8),
                    'iterations': 1
                },
                'contour': {
                    'min_area': 80,
                    'max_area': 400
                }
            }
        }
    }
}