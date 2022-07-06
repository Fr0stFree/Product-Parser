import sys
import json

from bs4 import BeautifulSoup as bs
import PySimpleGUI as GUI
import requests


class Parser:
    GUI.theme('LightGreen5')
    GUI.set_options(font='Franklin 10')
    WINDOW_SIZE = 1100, 650
    WINDOW_TITLE = 'Product Parser'
    DEFAULT_URL = 'https://mi-shop.com/ru/catalog/smartphones/'
    PARAM_INPUT_SIZE = 16, 1
    PARAM_TITLE_SIZE = 11, 1
    BUTTON_SIZE = 9, 1
    OUTPUT_TEXTBOX_PAD = 5, 10
    DROPDOWN_MENU_SIZE = 14, 1
    CONTAINER_TYPES = ['div', 'span', 'section']
    SELECTOR_TYPES = ['class', 'text', 'name', 'id']
    USER_AGENT_HEADER = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  \
                        (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 \
                        Yowser/2.5 Safari/537.36'

    def __init__(self):
        # Input
        url_input = GUI.Input(default_text=self.DEFAULT_URL, expand_x=True, key='-URL-')
        request_btn = GUI.Button('Request', size=self.BUTTON_SIZE, key='-REQUEST-')
        open_btn = GUI.Button('Open', size=self.BUTTON_SIZE, key='-OPEN-')
        show_page_btn = GUI.Button('Show Page', size=self.BUTTON_SIZE, key='-PAGE-', disabled=True)
        
        # Find
        find_button = GUI.Button('Find', size=self.BUTTON_SIZE, key='-FIND-', disabled=True)
        find_container = GUI.Text(text='Container type:', size=self.PARAM_TITLE_SIZE)
        find_selector_type = GUI.Text(text='Selector type:', size=self.PARAM_TITLE_SIZE)
        find_selector_name = GUI.Text(text='Selector name:', size=self.PARAM_TITLE_SIZE)
        param_container = GUI.Combo(values=self.CONTAINER_TYPES, default_value=self.CONTAINER_TYPES[0], key='-CONTAINER-', size=self.DROPDOWN_MENU_SIZE)
        param_selector_type = GUI.Combo(values=self.SELECTOR_TYPES, default_value=self.SELECTOR_TYPES[0], key='-SELECTOR_TYPE-', size=self.DROPDOWN_MENU_SIZE)
        param_selector_name = GUI.Input(default_text='product-card__body', size=self.PARAM_INPUT_SIZE, key='-SELECTOR_NAME-')
        find_column = GUI.Column([
            [find_container, param_container],
            [find_selector_type, param_selector_type],
            [find_selector_name, param_selector_name],
            [find_button],
        ])
        # Parse
        parse_btn = GUI.Button('Parse', key='-PARSE-', size=self.BUTTON_SIZE, disabled=True)
        parse_title = GUI.Text(text='', size=self.PARAM_TITLE_SIZE)
        parse_container = GUI.Text(text='Container type:', size=self.PARAM_TITLE_SIZE)
        parse_selector_type = GUI.Text(text='Selector type:', size=self.PARAM_TITLE_SIZE)
        parse_selector_name = GUI.Text(text='Selector name:', size=self.PARAM_TITLE_SIZE)
        parse_names = GUI.Text(text='Save as:', size=self.PARAM_TITLE_SIZE)
        param_info_column = GUI.Column([
            [parse_title],
            [parse_container],
            [parse_selector_type],
            [parse_selector_name],
            [parse_names],
            [parse_btn],
        ])
        param_1_clear = GUI.Button('Clear', key='-CLEAR_PARAM_1-', size=self.BUTTON_SIZE)
        param_1_title = GUI.Text(text='Parameter 1', size=self.PARAM_TITLE_SIZE)
        param_1_container = GUI.Combo(values=self.CONTAINER_TYPES, default_value=self.CONTAINER_TYPES[0], key='-PARAM_CONTAINER_1-', size=self.DROPDOWN_MENU_SIZE)
        param_1_selector_type = GUI.Combo(values=self.SELECTOR_TYPES, default_value=self.SELECTOR_TYPES[0], key='-PARAM_SELECTOR_TYPE_1-', size=self.DROPDOWN_MENU_SIZE)
        param_1_selector_name = GUI.Input(default_text='product-card__type', key='-PARAM_SELECTOR_NAME_1-', size=self.PARAM_INPUT_SIZE)
        param_1_name = GUI.Input(default_text='Категория',key='-PARAM_NAME_1-', size=self.PARAM_INPUT_SIZE)
        param_1_column = GUI.Column([
            [param_1_title],
            [param_1_container],
            [param_1_selector_type],
            [param_1_selector_name],
            [param_1_name],
            [param_1_clear],
        ])
        param_2_clear = GUI.Button('Clear', key='-CLEAR_PARAM_2-', size=self.BUTTON_SIZE)
        param_2_title = GUI.Text(text='Parameter 2', size=self.PARAM_TITLE_SIZE)
        param_2_container = GUI.Combo(values=self.CONTAINER_TYPES, default_value=self.CONTAINER_TYPES[0], key='-PARAM_CONTAINER_2-', size=self.DROPDOWN_MENU_SIZE)
        param_2_selector_type = GUI.Combo(values=self.SELECTOR_TYPES, default_value=self.SELECTOR_TYPES[0], key='-PARAM_SELECTOR_TYPE_2-', size=self.DROPDOWN_MENU_SIZE)
        param_2_selector_name = GUI.Input(default_text='product-card__title', key='-PARAM_SELECTOR_NAME_2-', size=self.PARAM_INPUT_SIZE)
        param_2_name = GUI.Input(default_text='Наименование',key='-PARAM_NAME_2-', size=self.PARAM_INPUT_SIZE)
        param_2_column = GUI.Column([
            [param_2_title],
            [param_2_container],
            [param_2_selector_type],
            [param_2_selector_name],
            [param_2_name],
            [param_2_clear],
        ])
        param_3_clear = GUI.Button('Clear', key='-CLEAR_PARAM_3-', size=self.BUTTON_SIZE)
        param_3_title = GUI.Text(text='Parameter 3', size=self.PARAM_TITLE_SIZE)
        param_3_container = GUI.Combo(values=self.CONTAINER_TYPES, default_value=self.CONTAINER_TYPES[1], key='-PARAM_CONTAINER_3-', size=self.DROPDOWN_MENU_SIZE)
        param_3_selector_type = GUI.Combo(values=self.SELECTOR_TYPES, default_value=self.SELECTOR_TYPES[0], key='-PARAM_SELECTOR_TYPE_3-', size=self.DROPDOWN_MENU_SIZE)
        param_3_selector_name = GUI.Input(default_text='price__new', key='-PARAM_SELECTOR_NAME_3-', size=self.PARAM_INPUT_SIZE)
        param_3_name = GUI.Input(default_text='Цена',key='-PARAM_NAME_3-', size=self.PARAM_INPUT_SIZE)
        param_3_column = GUI.Column([
            [param_3_title],
            [param_3_container],
            [param_3_selector_type],
            [param_3_selector_name],
            [param_3_name],
            [param_3_clear],
        ])
        param_4_clear = GUI.Button('Clear', key='-CLEAR_PARAM_4-', size=self.BUTTON_SIZE)
        param_4_title = GUI.Text(text='Parameter 4', size=self.PARAM_TITLE_SIZE)
        param_4_container = GUI.Combo(values=self.CONTAINER_TYPES, default_value=self.CONTAINER_TYPES[0], key='-PARAM_CONTAINER_4-', size=self.DROPDOWN_MENU_SIZE)
        param_4_selector_type = GUI.Combo(values=self.SELECTOR_TYPES, default_value=self.SELECTOR_TYPES[0], key='-PARAM_SELECTOR_TYPE_4-', size=self.DROPDOWN_MENU_SIZE)
        param_4_selector_name = GUI.Input(default_text='product-card__reviews', key='-PARAM_SELECTOR_NAME_4-', size=self.PARAM_INPUT_SIZE)
        param_4_name = GUI.Input(default_text='Популярность',key='-PARAM_NAME_4-', size=self.PARAM_INPUT_SIZE)
        param_4_column = GUI.Column([
            [param_4_title],
            [param_4_container],
            [param_4_selector_type],
            [param_4_selector_name],
            [param_4_name],
            [param_4_clear],
        ])
        param_5_clear = GUI.Button('Clear', key='-CLEAR_PARAM_5-', size=self.BUTTON_SIZE)
        param_5_title = GUI.Text(text='Parameter 5', size=self.PARAM_TITLE_SIZE)
        param_5_container = GUI.Combo(values=self.CONTAINER_TYPES, default_value=self.CONTAINER_TYPES[0], key='-PARAM_CONTAINER_5-', size=self.DROPDOWN_MENU_SIZE)
        param_5_selector_type = GUI.Combo(values=self.SELECTOR_TYPES, default_value=self.SELECTOR_TYPES[0], key='-PARAM_SELECTOR_TYPE_5-', size=self.DROPDOWN_MENU_SIZE)
        param_5_selector_name = GUI.Input(default_text='product-card__evaluation', key='-PARAM_SELECTOR_NAME_5-', size=self.PARAM_INPUT_SIZE)
        param_5_name = GUI.Input(default_text='Оценка',key='-PARAM_NAME_5-', size=self.PARAM_INPUT_SIZE)
        param_5_column = GUI.Column([
            [param_5_title],
            [param_5_container],
            [param_5_selector_type],
            [param_5_selector_name],
            [param_5_name],
            [param_5_clear],
        ])
        #  Output
        event_msg = GUI.Text(text='', enable_events=True, key='-MESSAGE-')
        output_box = GUI.Multiline(key='-OUTPUT-', disabled=True, expand_x=True, expand_y=True, pad=self.OUTPUT_TEXTBOX_PAD)
        save_btn = GUI.Button('Save',  key='-SAVE-', size=self.BUTTON_SIZE, disabled=True)
        clear_btn = GUI.Button('Clear', key='-CLEAR-', size=self.BUTTON_SIZE)
        close_btn = GUI.Button('Close', key='-CLOSE-', size=self.BUTTON_SIZE)

        layout = [
            [open_btn, request_btn, url_input, show_page_btn],
            [GUI.HorizontalSeparator()],
            [find_column, GUI.Push(), param_info_column, param_1_column, param_2_column, param_3_column, param_4_column, param_5_column],
            [GUI.HorizontalSeparator()],
            [event_msg],
            [output_box],
            [save_btn, GUI.Push(), clear_btn, close_btn],
        ]
        
        # Data storage
        self.page = None
        self.data = []
        self.clean_data = []

        self.window = GUI.Window(
            title=self.WINDOW_TITLE,
            layout=layout,
            size=self.WINDOW_SIZE,
        )
        

    def run(self):
        while True:
            event, values = self.window.read()

            if event in ('-OPEN-', '-REQUEST-'):
                if event == '-OPEN-':
                    self.load_data(source=GUI.popup_get_file('Open', no_window=True))
                
                elif event == '-REQUEST-':
                    self.request_data(source=values['-URL-'])

                if self.page:
                    self.window['-FIND-'].update(disabled=False)
                    self.window['-PAGE-'].update(disabled=False)

            if event == '-FIND-':
                self.find_data(
                    container=values['-CONTAINER-'],
                    attrs={values['-SELECTOR_TYPE-']: values['-SELECTOR_NAME-']},
                )
                if self.data:
                    self.window['-PARSE-'].update(disabled=False)
            
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
                    if self.clean_data:
                        self.window['-SAVE-'].update(disabled=False)

            if event in [f'-CLEAR_PARAM_{i}-' for i in range(1, 6)]:
                param_number = event.split('_')[-1].replace('-','')
                self.clear_param(param_number)

            if event == '-SAVE-':
                self.save_data()

            if event == '-CLEAR-':
                self.clear_data()

            if event in (GUI.WIN_CLOSED, '-CLOSE-'):
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
        self.data = []
        self.window['-PARSE-'].update(disabled=True)
        self.clean_data = []
        self.window['-SAVE-'].update(disabled=True)
    
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
