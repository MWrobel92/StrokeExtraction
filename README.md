# Stroke Extraction

This code has been developed as a part of the author's doctoral thesis. The preliminary version of the algorithm has been published in: M. Wróbel et.al. (2019) [_A Greedy Algorithm for Extraction of Handwritten Strokes_](https://link.springer.com/chapter/10.1007/978-3-030-20915-5_42) In: _Artificial Intelligence and Soft Computing. ICAISC 2019. Lecture Notes in Computer Science_, vol 11509. Springer, Cham. If you use this code for scientific purposes, please cite that paper.

# Instalation with Docker

Use the following command in the main project folder to build a docker image.
```
docker build -t stroke-extraction .
```

Then, use the following command to run the application.
```
docker run -v ./data:/src/app/data stroke-extraction tx.png
```