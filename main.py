import sys
import json

from bs4 import BeautifulSoup as bs
import PySimpleGUI as GUI
import requests


# Абракадабра для имитации человекоподобности для сервера сайта
USER_AGENT_HEADER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  \
                    (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 \
                    Yowser/2.5 Safari/537.36'


class Interface:
    GUI.theme('Gray Gray Gray')
    GUI.set_options(font='Franklin 10')
    WINDOW_SIZE = (1000, 600)
    DEFAULT_URL = 'https://mi-shop.com/ru/catalog/smartphones/'
    PARAM_INPUT_SIZE = 15, 1
    TEXT_PARAM_SIZE = 12, 1
    BUTTON_SIZE = 10, 1

    def __init__(self):
        # Request
        INPUT_URL = GUI.Input(default_text=self.DEFAULT_URL, expand_x=True, key='-URL-')
        BUTTON_REQUEST = GUI.Button('Request', size=self.BUTTON_SIZE, key='-REQUEST-')

        # Open
        BUTTON_OPEN = GUI.Button('Open', size=self.BUTTON_SIZE, key='-OPEN-')
        
        # Find
        TEXT_FIND = GUI.Text(text='Browse', size=self.PARAM_INPUT_SIZE)
        TEXT_FIND_CONTAINER = GUI.Text(text='Container type:', size=self.TEXT_PARAM_SIZE)
        INPUT_FIND_CONTAINER = GUI.Input(default_text='div', size=self.PARAM_INPUT_SIZE, key='-CONTAINER-')
        TEXT_FIND_SELECTOR_TYPE = GUI.Text(text='Selector type:', size=self.TEXT_PARAM_SIZE)
        INPUT_FIND_SELECTOR_TYPE = GUI.Input(default_text='class', size=self.PARAM_INPUT_SIZE, key='-SELECTOR_TYPE-')
        TEXT_FIND_SELECTOR_NAME = GUI.Text(text='Selector name:', size=self.TEXT_PARAM_SIZE)
        INPUT_FIND_SELECTOR_NAME = GUI.Input(default_text='product-card__body', size=self.PARAM_INPUT_SIZE, key='-SELECTOR_NAME-')
        BUTTON_FIND = GUI.Button('Find', size=self.BUTTON_SIZE, key='-FIND-')

        # Parse
        TEXT_PARSE = GUI.Text(text='', size=self.TEXT_PARAM_SIZE)
        TEXT_PARSE_CONTAINER = GUI.Text(text='Container type:', size=self.TEXT_PARAM_SIZE)
        TEXT_PARSE_SELECTOR_TYPE = GUI.Text(text='Selector type:', size=self.TEXT_PARAM_SIZE)
        TEXT_PARSE_SELECTOR_NAME = GUI.Text(text='Selector name:', size=self.TEXT_PARAM_SIZE)
        TEXT_PARAM_NAME = GUI.Text(text='Save as:', size=self.TEXT_PARAM_SIZE)
        
        TEXT_PARAM_1 = GUI.Text(text='Param1', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_CONTAINER_1 = GUI.Input(default_text='div', key='-PARAM_CONTAINER_1-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_1 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_1-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_1 = GUI.Input(default_text='product-card__type', key='-PARAM_SELECTOR_NAME_1-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_1 = GUI.Input(default_text='Категория',key='-PARAM_NAME_1-', size=self.PARAM_INPUT_SIZE)

        TEXT_PARAM_2 = GUI.Text(text='Param2', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_CONTAINER_2 = GUI.Input(default_text='div', key='-PARAM_CONTAINER_2-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_2 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_2-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_2 = GUI.Input(default_text='product-card__title', key='-PARAM_SELECTOR_NAME_2-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_2 = GUI.Input(default_text='Наименование',key='-PARAM_NAME_2-', size=self.PARAM_INPUT_SIZE)

        TEXT_PARAM_3 = GUI.Text(text='Param3', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_CONTAINER_3 = GUI.Input(default_text='span', key='-PARAM_CONTAINER_3-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_3 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_3-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_3 = GUI.Input(default_text='price__new', key='-PARAM_SELECTOR_NAME_3-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_3 = GUI.Input(default_text='Цена',key='-PARAM_NAME_3-', size=self.PARAM_INPUT_SIZE)

        TEXT_PARAM_4 = GUI.Text(text='Param4', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_CONTAINER_4 = GUI.Input(default_text='span', key='-PARAM_CONTAINER_4-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_TYPE_4 = GUI.Input(default_text='class', key='-PARAM_SELECTOR_TYPE_4-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_SELECTOR_NAME_4 = GUI.Input(default_text='price__new', key='-PARAM_SELECTOR_NAME_4-', size=self.PARAM_INPUT_SIZE)
        INPUT_PARSE_PARAM_NAME_4 = GUI.Input(default_text='Популярность',key='-PARAM_NAME_4-', size=self.PARAM_INPUT_SIZE)

        BUTTON_PARSE = GUI.Button('Parse', key='-PARSE-')
        BUTTON_SAVE = GUI.Button('Save',  key='-SAVE-')
        BUTTON_CLEAR = GUI.Button('Clear', key='-CLEAR-')
        BUTTON_CLOSE = GUI.Button('Close', key='-CLOSE-')

        TEXT_MESSAGE = GUI.Text(text='', enable_events=True, key='-MESSAGE-')
        OUTPUT_TEXTBOX = GUI.Multiline(key='-OUTPUT-', disabled=True, expand_x=True, expand_y=True)
        COLUMN_PARAM = GUI.Column(
            [
                [TEXT_PARSE, TEXT_PARAM_1, TEXT_PARAM_2, TEXT_PARAM_3, TEXT_PARAM_4],
                [TEXT_PARSE_CONTAINER, INPUT_PARSE_CONTAINER_1, INPUT_PARSE_CONTAINER_2, INPUT_PARSE_CONTAINER_3, INPUT_PARSE_CONTAINER_4],
                [TEXT_PARSE_SELECTOR_TYPE, INPUT_PARSE_SELECTOR_TYPE_1, INPUT_PARSE_SELECTOR_TYPE_2, INPUT_PARSE_SELECTOR_TYPE_3, INPUT_PARSE_SELECTOR_TYPE_4],
                [TEXT_PARSE_SELECTOR_NAME, INPUT_PARSE_SELECTOR_NAME_1, INPUT_PARSE_SELECTOR_NAME_2, INPUT_PARSE_SELECTOR_NAME_3, INPUT_PARSE_SELECTOR_NAME_4],
                [TEXT_PARAM_NAME, INPUT_PARSE_PARAM_NAME_1, INPUT_PARSE_PARAM_NAME_2, INPUT_PARSE_PARAM_NAME_3, INPUT_PARSE_PARAM_NAME_4],
            ],
        )
        COLUMN_OUTPUT = GUI.Column(
            [
                [TEXT_MESSAGE],
                [OUTPUT_TEXTBOX],
                [BUTTON_SAVE],
            ]
        )
        COLUMN_FIND = GUI.Column(
            [
                [TEXT_FIND_CONTAINER, INPUT_FIND_CONTAINER],
                [TEXT_FIND_SELECTOR_TYPE, INPUT_FIND_SELECTOR_TYPE],
                [TEXT_FIND_SELECTOR_NAME, INPUT_FIND_SELECTOR_NAME],
                [BUTTON_FIND],
            ],
        )
        LAYOUT = [
            [BUTTON_REQUEST, INPUT_URL],
            [BUTTON_OPEN],
            [COLUMN_FIND, COLUMN_PARAM],
            [COLUMN_OUTPUT],
            [BUTTON_PARSE],
            [GUI.Push(), BUTTON_CLEAR, BUTTON_CLOSE],
        ]
        self.window = GUI.Window(
            title='Product Parser',
            layout=LAYOUT,
            size=self.WINDOW_SIZE,
        )


def load_data(source):
    with open(source, mode='r', encoding='utf-8') as html_file:
        soup = bs(html_file, 'html.parser')
    return soup


def request_data(source):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT_HEADER
    response = session.get(url)
    soup = bs(response.text, 'html.parser')
    return soup


def find_data(soup, container, attrs):
    products = soup.find_all(container, attrs=attrs)
    return products


def parse_data(products, params):
    parsed_data = []
    for product in products:
        product_data = {}
        for param in params:
            product_data[param['name']] = product.find(param['container'], attrs=param['attrs']).text.strip()
        parsed_data.append(product_data)
    return parsed_data


def save_data(data):
    file_path = GUI.popup_get_file('Save as', no_window=True, save_as=True)
    if not file_path.endswith('.json'):
        file_path += '.json'
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    interface = Interface()
    soup = None
    data = []
    parsed_data = {}

    while True:
        event, values = interface.window.read()
        if event == '-OPEN-':
            file_path = GUI.popup_get_file('Open', no_window=True)
            if file_path:
                interface.window['-MESSAGE-'].update(f"Collecting data from '{file_path}'")
                soup = load_data(source=file_path)
                interface.window['-OUTPUT-'].update(soup.prettify())

        if event == '-REQUEST-':
            url = values['-URL-']
            interface.window['-MESSAGE-'].update(f"Collecting data from '{url}'")
            try:
                soup = request_data(source=url)
                interface.window['-OUTPUT-'].update(soup.prettify())
            except Exception as e:
                interface.window['-OUTPUT-'].update(e)

        if event == '-FIND-':
            if soup:
                container = values['-CONTAINER-']
                attrs = {values['-SELECTOR_TYPE-']: values['-SELECTOR_NAME-']}
                data = find_data(soup, container, attrs)
                interface.window['-MESSAGE-'].update(f'Products found: {len(data)}\nProduct example:')
                interface.window['-OUTPUT-'].update(data[0].prettify())
            else:
                interface.window['-MESSAGE-'].update('Data not found')

        if event == '-PARSE-':
            if not data:
                interface.window['-MESSAGE-'].update('No data to parse')
            else:
                params = []
                names = values['-PARAM_NAME-'].replace(' ', '').split(',')
                containers = values['-PARAM_CONTAINER-'].replace(' ', '').split(',')
                selector_types = values['-PARAM_SELECTOR_TYPE-'].replace(' ', '').split(',')
                selector_names = values['-PARAM_SELECTOR_NAME-'].replace(' ', '').split(',')
                params_count = len(names)
                if not params_count == len(names) == len(containers) == len(selector_types) == len(selector_names):
                    interface.window['-MESSAGE-'].update('Params quantity is not identical')
                else:
                    for i in range(params_count):
                        param = {
                            'name': names[i],
                            'container': containers[i],
                            'attrs': {selector_types[i]: selector_names[i]},
                        }
                        params.append(param)
                    parsed_data = parse_data(data, params)
                    interface.window['-MESSAGE-'].update('Data parsed')
                    interface.window['-OUTPUT-'].update(parsed_data)

        if event == '-SAVE-':
            if parsed_data:
                save_data(parsed_data)
            else:
                interface.window['-MESSAGE-'].update('No data to save')

        if event == '-CLEAR-':
            interface.window['-MESSAGE-'].update('')
            interface.window['-OUTPUT-'].update('')
            soup = None
            data = []
            parsed_data = {}

        if event in [GUI.WIN_CLOSED, '-CLOSE-']:
            break

    interface.window.close()
    sys.exit()
