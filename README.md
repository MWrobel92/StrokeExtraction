# Stroke Extraction

This code has been developed as a part of the author's doctoral thesis. The preliminary version of the algorithm has been published in: M. Wróbel et al. (2019) [_A Greedy Algorithm for Extraction of Handwritten Strokes_](https://link.springer.com/chapter/10.1007/978-3-030-20915-5_42) In: _Artificial Intelligence and Soft Computing. ICAISC 2019. Lecture Notes in Computer Science_, vol 11509. Springer, Cham. If you use this code for scientific purposes, please cite that paper.

# Instalation and usage with Docker

Use the following command in the main project folder to build a docker image.
```
docker build -t stroke-extraction .
```

Then, use one of the following commands to run the application (system dependent).
```
docker run -v ${pwd}/data:/src/app/data stroke-extraction tx.png
```
```
docker run -v ./data:/src/app/data stroke-extraction tx.png
```

The command above runs the application for the example picture _tx.png_ localized in the folder _data_. The results are saved in the same folder. The output files are:
* _tx_output_points.txt_ - coordinates of points that create a stroke, in readable format,
* _tx_output_polynomials.csv_ - coefficients of the polynomials that approximate extracted strokes,
* _tx_plot_raw.html_ - HTML plot with points that create a stroke,
* _tx_plot_approx.html_ - HTML plot with approximated strokes.

If you want to make a stroke extraction from another picture, you can put it into folder _data_ and modify the parameter in the command. You can also add the parameter ```no-plots``` to skip creating HTML plots and get the text output only.

```
docker run -v ${pwd}/data:/src/app/data stroke-extraction tx.png no-plots
```
