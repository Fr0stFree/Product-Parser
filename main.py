import sys
import json
from pprint import pprint
from bs4 import BeautifulSoup as bs
import PySimpleGUI as GUI
import requests


# Абракадабра для имитации человекоподобности для сервера сайта


class Parser:
    GUI.theme('Kahyak')
    GUI.set_options(font='Franklin 10')
    WINDOW_SIZE = 1000, 600
    WINDOW_TITLE = 'Product Parser'
    DEFAULT_URL = 'https://mi-shop.com/ru/catalog/smartphones/'
    PARAM_INPUT_SIZE = 15, 1
    PARAM_TITLE_SIZE = 13, 1
    TEXT_PARAM_SIZE = 12, 1
    BUTTON_SIZE = 10, 1
    BUTTON_CLEAR_PAD = 18,0
    OUTPUT_TEXTBOX_PAD = 15, 15
    USER_AGENT_HEADER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  \
                        (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 \
                        Yowser/2.5 Safari/537.36'

    def __init__(self):
        # Data storage
        self.page = None
        self.data = []
        self.clean_data = []

        # Input
        BUTTON_REQUEST = GUI.Button('Request', size=self.BUTTON_SIZE, key='-REQUEST-')
        INPUT_URL = GUI.Input(default_text=self.DEFAULT_URL, expand_x=True, key='-URL-')
        BUTTON_OPEN = GUI.Button('Open', size=self.BUTTON_SIZE, key='-OPEN-')
        BUTTON_SHOW_PAGE = GUI.Button('Show Page', size=self.BUTTON_SIZE, key='-PAGE-')
        
        # Find
        BUTTON_FIND = GUI.Button('Find', size=self.BUTTON_SIZE, key='-FIND-')
        TEXT_FIND = GUI.Text(text='', size=self.TEXT_PARAM_SIZE)
        TEXT_FIND_CONTAINER = GUI.Text(text='Container type:', size=self.TEXT_PARAM_SIZE)
        INPUT_FIND_CONTAINER = GUI.Input(default_text='div', size=self.PARAM_INPUT_SIZE, key='-CONTAINER-')
        TEXT_FIND_SELECTOR_TYPE = GUI.Text(text='Selector type:', size=self.TEXT_PARAM_SIZE)
        INPUT_FIND_SELECTOR_TYPE = GUI.Input(default_text='class', size=self.PARAM_INPUT_SIZE, key='-SELECTOR_TYPE-')
        TEXT_FIND_SELECTOR_NAME = GUI.Text(text='Selector name:', size=self.TEXT_PARAM_SIZE)
        INPUT_FIND_SELECTOR_NAME = GUI.Input(default_text='product-card__body', size=self.PARAM_INPUT_SIZE, key='-SELECTOR_NAME-')

        # Parse
        BUTTON_PARSE = GUI.Button('Parse', key='-PARSE-', size=self.BUTTON_SIZE)
        TEXT_PARSE = GUI.Text(text='', size=self.TEXT_PARAM_SIZE)
        TEXT_PARSE_CONTAINER = GUI.Text(text='Container type:', size=self.TEXT_PARAM_SIZE)
        TEXT_PARSE_SELECTOR_TYPE = GUI.Text(text='Selector type:', size=self.TEXT_PARAM_SIZE)
        TEXT_PARSE_SELECTOR_NAME = GUI.Text(text='Selector name:', size=self.TEXT_PARAM_SIZE)
        TEXT_PARAM_NAME = GUI.Text(text='Save as:', size=self.TEXT_PARAM_SIZE)
        
        BUTTON_CLEAR_1 = GUI.Button('Clear', key='-CLEAR_PARAM_1-', size=self.BUTTON_SIZE, pad=self.BUTTON_CLEAR_PAD)
        TEXT_PARAM_1 = GUI.Text(text='Parameter 1', size=self.PARAM_TITLE_SIZE, justification='center')
        INPUT_PARSE_CONTAINER_1 = GUI.Input(default_text='div', key='-PARAM_CONTAINER_1-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_1 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_1-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_1 = GUI.Input(default_text='product-card__type', key='-PARAM_SELECTOR_NAME_1-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_1 = GUI.Input(default_text='Категория',key='-PARAM_NAME_1-', size=self.PARAM_INPUT_SIZE)

        BUTTON_CLEAR_2 = GUI.Button('Clear', key='-CLEAR_PARAM_2-', size=self.BUTTON_SIZE, pad=self.BUTTON_CLEAR_PAD)
        TEXT_PARAM_2 = GUI.Text(text='Parameter 2', size=self.PARAM_TITLE_SIZE, justification='center')
        INPUT_PARSE_CONTAINER_2 = GUI.Input(default_text='div', key='-PARAM_CONTAINER_2-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_2 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_2-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_2 = GUI.Input(default_text='product-card__title', key='-PARAM_SELECTOR_NAME_2-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_2 = GUI.Input(default_text='Наименование',key='-PARAM_NAME_2-', size=self.PARAM_INPUT_SIZE)

        BUTTON_CLEAR_3 = GUI.Button('Clear', key='-CLEAR_PARAM_3-', size=self.BUTTON_SIZE, pad=self.BUTTON_CLEAR_PAD)
        TEXT_PARAM_3 = GUI.Text(text='Parameter 3', size=self.PARAM_TITLE_SIZE, justification='center')
        INPUT_PARSE_CONTAINER_3 = GUI.Input(default_text='span', key='-PARAM_CONTAINER_3-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_3 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_3-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_3 = GUI.Input(default_text='price__new', key='-PARAM_SELECTOR_NAME_3-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_3 = GUI.Input(default_text='Цена',key='-PARAM_NAME_3-', size=self.PARAM_INPUT_SIZE)

        BUTTON_CLEAR_4 = GUI.Button('Clear', key='-CLEAR_PARAM_4-', size=self.BUTTON_SIZE, pad=self.BUTTON_CLEAR_PAD)
        TEXT_PARAM_4 = GUI.Text(text='Parameter 4', size=self.PARAM_TITLE_SIZE, justification='center')
        INPUT_PARSE_CONTAINER_4 = GUI.Input(default_text='div', key='-PARAM_CONTAINER_4-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_4 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_4-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_4 = GUI.Input(default_text='product-card__reviews', key='-PARAM_SELECTOR_NAME_4-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_4 = GUI.Input(default_text='Популярность',key='-PARAM_NAME_4-', size=self.PARAM_INPUT_SIZE)

        BUTTON_CLEAR_5 = GUI.Button('Clear', key='-CLEAR_PARAM_5-', size=self.BUTTON_SIZE, pad=self.BUTTON_CLEAR_PAD)
        TEXT_PARAM_5 = GUI.Text(text='Parameter 5', size=self.PARAM_TITLE_SIZE, justification='center')
        INPUT_PARSE_CONTAINER_5 = GUI.Input(default_text='div', key='-PARAM_CONTAINER_5-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_5 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_5-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_5 = GUI.Input(default_text='product-card__evaluation', key='-PARAM_SELECTOR_NAME_5-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_5 = GUI.Input(default_text='Оценка',key='-PARAM_NAME_5-', size=self.PARAM_INPUT_SIZE)
        
        #  Output
        EVENT_MESSAGE_START = GUI.Text(text='Event message:')
        EVENT_MESSAGE = GUI.Text(text='', enable_events=True, key='-MESSAGE-')
        OUTPUT_TEXTBOX = GUI.Multiline(key='-OUTPUT-', disabled=True, expand_x=True, expand_y=True, pad=self.OUTPUT_TEXTBOX_PAD)

        BUTTON_SAVE = GUI.Button('Save',  key='-SAVE-', size=self.BUTTON_SIZE)
        BUTTON_CLEAR = GUI.Button('Clear', key='-CLEAR-', size=self.BUTTON_SIZE)
        BUTTON_CLOSE = GUI.Button('Close', key='-CLOSE-', size=self.BUTTON_SIZE)

        LAYOUT = [
            [BUTTON_OPEN, BUTTON_REQUEST, INPUT_URL],
            [BUTTON_SHOW_PAGE, GUI.Push(), TEXT_PARSE, TEXT_PARAM_1, TEXT_PARAM_2, TEXT_PARAM_3, TEXT_PARAM_4, TEXT_PARAM_5],
            [TEXT_FIND_CONTAINER, INPUT_FIND_CONTAINER, GUI.Push(), TEXT_PARSE_CONTAINER, INPUT_PARSE_CONTAINER_1, INPUT_PARSE_CONTAINER_2, INPUT_PARSE_CONTAINER_3, INPUT_PARSE_CONTAINER_4, INPUT_PARSE_CONTAINER_5],
            [TEXT_FIND_SELECTOR_TYPE, INPUT_FIND_SELECTOR_TYPE, GUI.Push(),TEXT_PARSE_SELECTOR_TYPE, INPUT_PARSE_SELECTOR_TYPE_1, INPUT_PARSE_SELECTOR_TYPE_2, INPUT_PARSE_SELECTOR_TYPE_3, INPUT_PARSE_SELECTOR_TYPE_4, INPUT_PARSE_SELECTOR_TYPE_5],
            [TEXT_FIND_SELECTOR_NAME, INPUT_FIND_SELECTOR_NAME, GUI.Push(),TEXT_PARSE_SELECTOR_NAME, INPUT_PARSE_SELECTOR_NAME_1, INPUT_PARSE_SELECTOR_NAME_2, INPUT_PARSE_SELECTOR_NAME_3, INPUT_PARSE_SELECTOR_NAME_4, INPUT_PARSE_SELECTOR_NAME_5],
            [GUI.Push(), TEXT_PARAM_NAME, INPUT_PARSE_PARAM_NAME_1, INPUT_PARSE_PARAM_NAME_2, INPUT_PARSE_PARAM_NAME_3, INPUT_PARSE_PARAM_NAME_4, INPUT_PARSE_PARAM_NAME_5],
            [BUTTON_FIND, GUI.Push(), BUTTON_PARSE, BUTTON_CLEAR_1, BUTTON_CLEAR_2, BUTTON_CLEAR_3, BUTTON_CLEAR_4, BUTTON_CLEAR_5],
            [EVENT_MESSAGE_START, EVENT_MESSAGE],
            [OUTPUT_TEXTBOX],
            [BUTTON_SAVE, GUI.Push(), BUTTON_CLEAR, BUTTON_CLOSE],
        ]
        self.window = GUI.Window(
            title=self.WINDOW_TITLE,
            layout=LAYOUT,
            size=self.WINDOW_SIZE,
        )

    def run(self):
        while True:
            event, values = self.window.read()

            if event == '-OPEN-':
                self.load_data(source=GUI.popup_get_file('Open', no_window=True))

            if event == '-REQUEST-':
                self.request_data(source=values['-URL-'])

            if event == '-FIND-':
                self.find_data(
                    container=values['-CONTAINER-'],
                    attrs={values['-SELECTOR_TYPE-']: values['-SELECTOR_NAME-']},
                )
            
            if event == '-PAGE-':
                if self.page:
                    self.window['-OUTPUT-'].update(self.page)
                else:
                    self.window['-MESSAGE-'].update('page is not loaded')

            if event == '-PARSE-':
                params = []
                stop = False
                for param_number in range(1, 6):
                    name = values[f'-PARAM_NAME_{param_number}-'].strip()
                    container = values[f'-PARAM_CONTAINER_{param_number}-'].strip()
                    selector_type = values[f'-PARAM_SELECTOR_TYPE_{param_number}-'].strip()
                    selector_name = values[f'-PARAM_SELECTOR_NAME_{param_number}-'].strip()
                    fields = [name, container, selector_type, selector_name]
                    if all(fields):
                        param = {
                            'name': name,
                            'container': container,
                            'attrs': {selector_type: selector_name},
                        }
                        params.append(param)

                    elif any(fields):
                        stop = True
                        self.window['-MESSAGE-'].update(f'not all fields have been completed in the column №{param_number}')

                if not stop:
                    self.parse_data(params)

            if event in [f'-CLEAR_PARAM_{i}-' for i in range(1, 6)]:
                param_number = event.split('_')[-1].replace('-','')
                self.clear_param(param_number)

            if event == '-SAVE-':
                self.save_data()

            if event == '-CLEAR-':
                self.clear_data()

            if event in [GUI.WIN_CLOSED, '-CLOSE-']:
                break

    def load_data(self, source):
        if source:
            with open(source, mode='r', encoding='utf-8') as html_file:
                self.page = bs(html_file, 'html.parser')
            self.window['-MESSAGE-'].update(f"collecting data from '{source}'")
            self.window['-OUTPUT-'].update(self.page.prettify())


    def request_data(self, source):
        self.window['-MESSAGE-'].update(f"collecting data from '{source}'")
        try:
            session = requests.Session()
            session.headers['User-Agent'] = self.USER_AGENT_HEADER
            response = session.get(source)
            self.page = bs(response.text, 'html.parser')

        except Exception as e:
            self.window['-MESSAGE-'].update('some error occured')
            self.window['-OUTPUT-'].update(e)
        

    def find_data(self, container, attrs):
        if not self.page:
            self.window['-MESSAGE-'].update('page is not loaded')
            return
        
        self.data = self.page.find_all(container, attrs=attrs)
        if not self.data:
            self.window['-MESSAGE-'].update('objects are not found')
            self.window['-OUTPUT-'].update(self.page.prettify())
            return

        self.window['-MESSAGE-'].update(f'{len(self.data)} objects are found, object example:')
        self.window['-OUTPUT-'].update(self.data[0].prettify())      
     
    def save_data(self):
        if not self.clean_data:
            self.window['-MESSAGE-'].update('no clean data to save')
            return
    
        path = GUI.popup_get_file('Save as', no_window=True, save_as=True)
        path = f'{path}.json' if not path.endswith('.json') else path
        with open(path, mode='w', encoding='utf-8') as file:
            json.dump(self.clean_data, file, ensure_ascii=False, indent=4)

    def clear_param(self, param_number):
        self.window[f'-PARAM_CONTAINER_{param_number}-'].update('')
        self.window[f'-PARAM_SELECTOR_TYPE_{param_number}-'].update('')
        self.window[f'-PARAM_SELECTOR_NAME_{param_number}-'].update('')
        self.window[f'-PARAM_NAME_{param_number}-'].update('')

    def clear_data(self):
        self.window['-MESSAGE-'].update('')
        self.window['-OUTPUT-'].update('')
        self.page = None
        self.data = []
        self.clean_data = []

    def parse_data(self, params):
        if not self.data:
            self.window['-MESSAGE-'].update('no data to parse')
            return

        if not params:
            self.window['-MESSAGE-'].update('no parameters are set')
            return

        self.clean_data.clear()
        for obj in self.data:
            buff = {}
            for param in params:
                try:
                    value = obj.find(param['container'], attrs=param['attrs']).text.strip()
                except AttributeError:
                    value = None
                buff[param['name']] = value
            self.clean_data.append(buff)

        self.window['-MESSAGE-'].update('data have been parsed successfuly')
        self.window['-OUTPUT-'].update(self.clean_data)


if __name__ == '__main__':
    parser = Parser()
    parser.run()
    parser.window.close()
    sys.exit()
