# PBAss18
<br>
<h2> Installation of the tool:</h2>
<h3> Install Python 3.6 with miniconda: </h3>
<a href="https://conda.io/miniconda.html" target="_blank" rel="noopener">Download miniconda3</a><br>
<p>download: installer for miniconda for python 3.6 for your OS</p>
<p>install miniconda3</p>
<h3> conda Installs: </h3>
<p>go to: /miniconda3/scripts</p>
<h5> Install PIL command:</h5>
<p>conda install pillow</p>
<h5> Install Keras command:</h5>
<p>conda install keras</p>
<h5> Install Theano command:</h5>
<p>conda install theano</p>
<h5> Install matplotlib command:</h5>
<p>conda install matplotlib</p>
<h3> pip Installs: </h3>
<p>go to: /miniconda3/scripts</p>
<h5> Install sklearn command:</h5>
<p>pip install sklearn</p>
<h5> Install lime command:</h5>
<p>pip install lime</p>

<h3> Change backend to Theano: </h3>
<p> (download or clone the application)<br>
go to /Regression Model Explainer<br>
../miniconda3/python starter.py<br>
close the window to change from tensaflow to theano backennd</p>
<p>Change backend to Theano:<br>
open file at:<br>
../Users/yourusername/.keras/keras.json<br>
change from<br>
{<br>
    "floatx": "float32",<br>
    "epsilon": 1e-07,<br>
    "backend": "tensorflow",<br>
    "image_data_format": "channels_last"<br>
}<br>
<br>
to:<br>
<br>
{<br>
    "floatx": "float32",<br>
    "epsilon": 1e-07,<br>
    "backend": "theano",<br>
    "image_data_format": "channels_last"<br>
}</p>
<h3> Run the app: </h3>
<p>go to /Regression Model Explainer<br>
(download or clone the application)<br>
../miniconda3/python starter.py<br>
or simple run starter.py (if cloned in IDE)</p>
<br>
<h2> Short manual for the tool:</h2>
<a href="https://github.com/hoerli/PBAss18/blob/prototype/Regression%20Model%20Explainer/short_manual.pdf" target="_blank" rel="noopener">Short Manual</a>

