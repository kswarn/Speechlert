# Speechlert
A python script that gives out a notification alert when a specific word/phrase is identified in real time audio. Thus, the name, Speechlert. 

It makes use of the python speech recognition module to detect and capture real time audio and store it in a file. The audio is converted to text and then the specific pattern is searched for in the text. 

The objective of the project is to give out a notification alert immediately when a particular word or phrase is spoken, thus, capturing live audio, converting to text and searching for the pattern needs to happen simultaneously every t seconds. 

The real time audio used here is the audio from a Zoom call. In the Zoom application, the audio output is redirected to another application called ---- which is then sent as input to the python script. This created a pipeline from the Zoom call to our local python script.

In order to run this project on your system, you have to install this application from ----. After installation, at the source of the real time audio, the output channel must be redirected to this application instead of speakers or headphones. 

Once the audio is successfully redirected to the python script using this pipeline, the audio is then divided into chunks of a suitable t seconds value. For each chunk, the process of speech-to-text is carried out and is followed by searching for the specific pattern. 

Once the pattern is identified, a notification alert is given out as output. 
