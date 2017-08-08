from psychopy import visual, event, core
from prettytable import PrettyTable
import numpy as np
import random

from screen import get_frame_rate, get_screen_res


def create_win(screen_color, show_mouse=True):
    screen_res = get_screen_res()
    win = visual.Window(screen_res.values(), fullscr=True, monitor='TestMonitor',
                        units='pix', screen=0, color=screen_color)
    event.Mouse(visible=show_mouse, newPos=None, win=win)
    win.flip()
    frames_per_sec = get_frame_rate(win=win)
    return win, screen_res, frames_per_sec


def run_test_1(win, number_of_frames=100):
    resp_clock = core.Clock()
    frames_times = []
    for i in range(number_of_frames):
        win.callOnFlip(resp_clock.reset)
        win.flip()
        win.flip()
        frames_times.append(resp_clock.getTime())

    return frames_times


def test_info(test_results, test_name, number_of_elem=10):
    random.shuffle(test_results)
    random_elem = test_results[:number_of_elem]
    mean = np.mean(test_results)
    median = np.median(test_results)
    std = np.std(test_results)

    return {'name': test_name, 'test_results': test_results, 'random_elem': random_elem,
            'mean': mean, 'median': median, 'std': std}


def run_tests():
    win, screen_res, frames_per_sec = create_win('black', False)
    all_results = []
    test_1 = run_test_1(win, 10)
    all_results.append(test_info(test_1, "empty screen"))

    table = PrettyTable()
    table.field_names = ["Test name", "few random elements", "mean", "median", "std"]
    for elem in all_results:
        table.add_row([elem['name'], elem['random_elem'], elem['mean'], elem['median'], elem['std']])

    print table


run_tests()
