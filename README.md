# Currency_converter
Currency_converter is a graphical interface designed with PyQt5 allows to convert currencies and view the rates history graph. 
Rates can be retrieved from two free APIs: free.currconv and finnhub.io.

The application is in the form of 3 tabs:
- Options
- Currency converter
- Historical graph

# What does the program do ?
## Main window
- A rectangle placed at the top left constantly displays the day of the week, the current date and time according to the format chosen by the user
- A status message area at the bottom of the window

## Option tab
- The user can choose their API from a drop-down menu
- For each API a key is proposed by default but it can be modified and saved
- The API key displayed changes depending on the API selected in the drop-down menu
- A 'TEST' button is used to check the validity of the inserted API key, if the API key is wrong, the program proposes to restore the previous one
- The graph theme can be modified ('Light' or 'Dark')
- The date and hour format can be modified
- The 'Save all' button allows to save all the preferences in a JSON file, these preferences will be loaded directly the next time the application is started.

## Currency Converter
- The input field is checked to ensure that an integer or float number is inserted
- Two drop-down menus allow to select the currencies
- A 'swipe' button allows to reverse the currency pair
- The 'convert' button converts the amount inserted using the API chosen by the user
- An output area displays the converted value, this value can be directly selected by the cursor
- Additional information area displayed at the bottom gives the conversion of one unit of the currency (ex : 1 EURO = 1.2 US Dollar), the area also displays the local name of the currency, its symbol as well as the date and time of the last update
- A 'copy' button allows to directly copy the result obtained to the clipboard
- A 'clear' button is used to clear the input field, the output area and the additional information area

## Historical graph
- Two drop-down menus allow to select the currencies
- A 'swipe' button allows to reverse the currency pair
- A 'VIEW' button allows to retrieve historical data from the API and represent it graphically
- A graph frame showing the historical rate curve
- The graph displays the rates on the y axis, the date on the x axis (according to the format chosen by the user) and a title displaying the selected currency pair and the start and end date of the measurement
- A column on the right displays graph statistics (start / end date of the measurement, duration of the measurement, last rate, last variation, total variation, min / max / mean
- A drop-down menu allow to select the range time of the measurement
- The 'Save the graph' button allows to save the image of the graph in the current folder in .png format
- The 'Copy rate value' copies the code of the chosen currency pairs, the dates (timestamps) and their corresponding rate to the clipboard in the form of a dictionary

## Additional info
- The data used to draw the graph of historical rates is only taken from free.currconv
- A thread periodically analyzes the state of the Internet connection by connecting to the Google DNS, if a cut is noticed certain buttons launching processes requiring Internet will be disabled during the cut
- Each time current tab change, the title at the top of the window changes to the name of the selected tab
- The program retrieves the information regarding the name of currencies, their code, their local name, etc. from the currencies.json file (retrieved from https://gist.github.com/Fluidbyte/2973986)
- Each time the application is started, the save.json file is loaded in order to apply the user's preferences (API chosen, the scope of the historical data in days 'range', the choosen graph theme, the choice to display graph grid or not, the time format and the date format). 
- The name of the APIs as well as their key are entered in the save.json file, these are browsed each time the application is started in order to fill in the API comboBoxes in the option tab and to pre-fill the field dedicated to API keys.

# Screenshots
## Currency Converter tab 
![conv_1](https://user-images.githubusercontent.com/11463619/117135045-b81cbe80-ada6-11eb-882c-c0583fc42bd2.png)
## Conversion
![conv_2](https://user-images.githubusercontent.com/11463619/117135049-b8b55500-ada6-11eb-97ba-4e8b1c082130.png)
## Graph visualisation
![graph_1](https://user-images.githubusercontent.com/11463619/117135053-b8b55500-ada6-11eb-93be-b0dd4ba82d23.png)
## Option tab
![opt_1](https://user-images.githubusercontent.com/11463619/117135054-b94deb80-ada6-11eb-857d-8404625424f2.png)
## Data copied to clipboard
![copy_1](https://user-images.githubusercontent.com/11463619/117135051-b8b55500-ada6-11eb-8830-459ab4be7ab7.png)
## Graph image saved
![save_img](https://user-images.githubusercontent.com/11463619/117135056-b94deb80-ada6-11eb-8a97-787ae8791439.png)

# Requirments
- `Python 3.8`
- `numpy`
- `PyQt5`
- `pyqtgraph`
- `pyperclip`
