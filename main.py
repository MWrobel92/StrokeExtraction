import numpy as np
import sys
import skimage.io as io
import warnings
import time
from src.extraction import stroke_extraction
from src.draw import prepare_plots


def run_extraction(file_name, save_plots=False, print_log=True):

    # Read an input image in greyscale
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        input_image = io.imread('data/' + file_name, as_gray=True)

    # Do the extraction
    start_time_extraction = time.time()
    extracted_strokes = stroke_extraction(input_image)
    time_extraction = time.time() - start_time_extraction
    if print_log:
        print(f'Number of extrated strokes: {len(extracted_strokes)}')
        print(f'Elapsed time: {time_extraction} s')

    # Save the results
    name = file_name.split('.')[0]
    points_array = []
    polynomials_array = []
    for s in extracted_strokes:
        points_array.append(str(s))
        polynomials_array.append(s.vector_of_features())
    with open('data/' + name + '_output_points.txt', 'w+') as f:
        for line in points_array:
            f.write(line)
            f.write('\n')
    np.savetxt('data/' + name + '_output_polynomials.csv', polynomials_array, delimiter=',')

    # Make plots
    if save_plots:
        fig1, fig2 = prepare_plots(extracted_strokes, 'data/' + file_name)
        fig1.write_html('data/' + name + '_plot_raw.html')
        fig2.write_html('data/' + name + '_plot_approx.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_name = sys.argv[1]
    else:
        input_name = 'tx.png'
    show = not ('no-plots' in sys.argv)

    run_extraction(input_name, show)
