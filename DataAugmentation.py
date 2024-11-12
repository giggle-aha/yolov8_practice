import process

data_path = 'data/ImgAndLabel'
save_path = 'data/endData'
method_list = {'methods': {'random_brightness': [True],
                           'random_channel': [True],
                           'random_contrast': [True],
                           'random_resize': [True, [True]],
                           'random_gauss': [True],
                           'random_flip': [True],
                           'random_rotation': [True],
                           'random_translate': [True],
                           'random_perspective': [True, [30, True, False, 42, False]]},
               'task': 'detect'
               }
process.process(data_path, save_path, method_list, single=True)
