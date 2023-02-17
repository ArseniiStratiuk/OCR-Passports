# OCR Passports
 OCR Passports with Tesseract and OpenCV. Project for MAN (Minor Academy of Sciences of Ukraine).

---

![](GUI_Dark.png)
| _`GUI.py` on Windows 10 with dark mode and standart 'blue' theme. An example of the program's work._

## Installation of the project

In order to test and check how the program works, you need to download Python and several additional libraries, which are not installed together with the programming language:

- CustomTkinter (customtkinter);
- PIL (pillow);
- OpenCV (opencv-python);
- Imutils (imutils);
- PyTesseract (pytesseract);
- NumPy (numpy).

<br>

To do this, you need to enter the commands below in the command line:

```
pip install customtkinter
```
```
pip install pillow
```
```
pip install opencv-python
```
```
pip install imutils
```
```
pip install pytesseract
```
```
pip install numpy
```

<br>

All that remains is to run the file "GUI.py". Examples of passport photos for processing are placed in the folder "Passports_Photos".

Also make sure that path to the folder with the program does not contain any spaces, Cyrillic and other unwanted symbols. For example:

<i>E:\Завантаження\\& #!,\OCR-Passports\ - Incorrect path that will cause program error <br>
<i>E:\Downloads\OCR-Passports\ - Example of a correct folder path that will not cause problems
