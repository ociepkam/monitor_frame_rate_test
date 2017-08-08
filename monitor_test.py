from psychopy import visual, event, core
from prettytable import PrettyTable
import numpy as np
import random

from screen import get_screen_res

__author__ = 'ociepkam'


def create_win(screen_color, show_mouse=True):
    screen_res = get_screen_res()
    win = visual.Window(screen_res.values(), fullscr=True, monitor='TestMonitor',
                        units='pix', screen=0, color=screen_color)
    event.Mouse(visible=show_mouse, newPos=None, win=win)
    win.flip()
    return win, screen_res


def run_test_1(win, _, number_of_frames=100):
    resp_clock = core.Clock()
    frames_times = []
    for i in range(number_of_frames):
        win.callOnFlip(resp_clock.reset)
        win.flip()
        win.flip()
        frames_times.append(resp_clock.getTime())
    return "empty screen", frames_times


def run_test_2(win, screen_res, number_of_frames=100):
    text = visual.TextStim(win=win, antialias=True, font=u'Arial', text='Move mouse.',
                           height=40, wrapWidth=screen_res['width'], color=u'white',
                           alignHoriz='center', alignVert='center')
    event.Mouse(visible=True, newPos=None, win=win)
    text.setAutoDraw(True)
    win.flip()

    _, frames_times = run_test_1(win, screen_res, number_of_frames)

    event.Mouse(visible=False, newPos=None, win=win)
    text.setAutoDraw(False)
    win.flip()
    return "mouse moves", frames_times


def run_test_3(win, screen_res, number_of_frames=100):
    text = visual.TextStim(win=win, antialias=True, font=u'Arial', text='Text',
                           height=40, wrapWidth=screen_res['width'], color=u'white',
                           alignHoriz='center', alignVert='center')
    resp_clock = core.Clock()
    frames_times = []
    for i in range(number_of_frames):
        win.callOnFlip(resp_clock.reset)
        text.setAutoDraw(True)
        win.flip()
        text.setAutoDraw(False)
        win.flip()
        frames_times.append(resp_clock.getTime())

    return "text shows", frames_times


def run_test_4(win, screen_res, number_of_frames=100):
    text_list = []
    for _ in range(number_of_frames):
        horizontal = screen_res['width'] * random.random() - screen_res['width'] / 2.0
        vertical = screen_res['height'] * random.random() - screen_res['height'] / 2.0
        text = visual.TextStim(win=win, antialias=True, font=u'Arial', text='Text',
                               height=40, wrapWidth=screen_res['width'], color=u'white',
                               pos=(horizontal, vertical))
        text_list.append(text)

    resp_clock = core.Clock()
    frames_times = []
    for text in text_list:
        win.callOnFlip(resp_clock.reset)
        text.setAutoDraw(True)
        win.flip()
        win.flip()
        frames_times.append(resp_clock.getTime())

    for text in text_list:
        text.setAutoDraw(False)

    return "text shows everywhere", frames_times


def run_test_5(win, _, number_of_frames=100):
    image = visual.ImageStim(win, image='test_image.jpg', interpolate=True)

    resp_clock = core.Clock()
    frames_times = []
    for i in range(number_of_frames):
        image.setAutoDraw(True)
        win.callOnFlip(resp_clock.reset)
        win.flip()
        image.setAutoDraw(False)
        win.flip()
        frames_times.append(resp_clock.getTime())
    return "image shows", frames_times


def test_info(test_results, test_name, number_of_elem=10):
    random.shuffle(test_results)
    random_elem = test_results[:number_of_elem]
    mean = np.mean(test_results)
    median = np.median(test_results)
    std = np.std(test_results)
    res_sum = sum(test_results)
    minimum = min(test_results)
    maximum = max(test_results)
    mean_frame_rate = 1./mean

    return {'name': test_name, 'test_results': test_results, 'random_elem': random_elem,
            'mean': mean, 'median': median, 'std': std, 'sum': res_sum, 'min': minimum,
            'max': maximum, 'mean_frame_rate': mean_frame_rate}


def run_tests(tests_to_run, number_of_frames=100):
    win, screen_res = create_win('black', False)
    all_results = []
    for test in tests_to_run:
        test_name, test_res = test(win, screen_res, number_of_frames)
        info = test_info(test_results=test_res, test_name=test_name)
        all_results.append(info)

    table = PrettyTable()
    table.field_names = ["Test name", "mean", "median", "std", "sum",
                         "min", "max", "mean frame rate", "few random elements"]
    for elem in all_results:
        table.add_row([elem['name'], elem['mean'], elem['median'], elem['std'], elem['sum'],
                       elem['min'], elem['max'], elem['mean_frame_rate'], elem['random_elem']])

    print table

functions_list = [run_test_1, run_test_2, run_test_3, run_test_4, run_test_5]
run_tests(functions_list, 200)
