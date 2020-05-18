from bs4 import BeautifulSoup
import requests
import pprint as pp
import json
import pandas as pd

SERVICE_JSON_PATH = '../service-setting.json'


class FakeDataGenerator(object):
    def __init__(self, isDebug=False):

        self.version = "0.0.1"
        self.isDebug = isDebug

        self.fakeBody = None
        self.fakeStatus = 0

        self.isError = False
        self.reqTimeout = 20

        if self.isDebug is True:
            print("FakeDataGenerator Loaded")

        self.__loading_service_json()

    def __loading_service_json(self):
        if self.isDebug:
            print("Loading Service Json")
        try:
            __setting_configs = None
            with open(SERVICE_JSON_PATH, 'r', encoding='utf-8') as __f:
                __setting_configs = json.load(__f)

            if __setting_configs is not None:
                self.setting_configs = __setting_configs

            if self.isDebug:
                print((self.setting_configs['info'])['version'])
                print(self.setting_configs.keys())

            self.__json_load_check()
        except Exception as E:
            self.isError = True
            print(str(E))

    def loading_fake_data(self, get_data_source):
        if self.isDebug:
            print("Loading Fake Data")

        try:

            __req = requests.get(get_data_source, timeout=self.reqTimeout)

            __is_ok = __req.ok
            __status_code = __req.status_code

            if __is_ok is True and __status_code == 200:
                __dummy_body = __req.text
                self.fakeBody = __dummy_body
            else:
                self.isError = True

            self.__status_code = __status_code

            if self.isDebug:
                print("HTML request : " + str(__is_ok))
                print("Request Status : " + str(__status_code))

        except Exception as e:
            self.isError = True
            print(str(e))

    def __json_load_check(self):
        __check_lists = ['emptys', 'anchors', 'keyNames', 'keyConventions']
        __match_cnt = len(__check_lists)
        for __check in __check_lists:
            if __check in self.setting_configs:
                __match_cnt -= 1

        print(__match_cnt)
        if __match_cnt == 0:
            if self.isDebug:
                print("OK")
        else:
            if self.isDebug:
                print("json Load Error")
            self.isError = True

    def generate_fake_body(self):
        if self.isError == True:
            print("There is Error, please Check")
            return None

        __check_lists = ['emptys', 'anchors', 'keyNames', 'keyConventions']

        __emptys = self.setting_configs.get('emptys', None)
        __anchors = self.setting_configs.get('anchors', None)
        __keyNames = self.setting_configs.get('keyNames', None)
        __keyConventions = self.setting_configs.get('keyConventions', None)
        __fakeBody = self.fakeBody

        __soup = BeautifulSoup(__fakeBody, 'html.parser')
        __fake_data_list = __soup.findAll('li', {'class': 'li_box'})

        if __fake_data_list is None or len(__fake_data_list) == 0:
            print("There is not data")
            return None

        if self.isDebug:
            __dummy_item = __fake_data_list[4]
            __debug_data_list = __fake_data_list[:10]
            pp.pprint(__fake_data_list[0])
            __fake_data_list = __debug_data_list

        __gen_data_list = list()

        for __single_data in __fake_data_list:
            __gen_dict = dict()

            __B_Name = self.__gen_type_A(
                __single_data, 'B_Name', __emptys, __anchors)

            __I_Name = self.__gen_type_A(
                __single_data, 'I_Name', __emptys, __anchors)

            __P_Value = self.__gen_type_B(
                __single_data, 'P_Value', __emptys, __anchors)

            __R_Value = self.__gen_type_B(
                __single_data, 'R_Value', __emptys, __anchors)

            __L_Value = self.__gen_type_C(
                __single_data, 'L_Value', __emptys, __anchors)

            __gen_dict[str(__keyNames['B_Name'])] = __B_Name
            __gen_dict[str(__keyNames['I_Name'])] = __I_Name
            __gen_dict[str(__keyNames['P_Value'])] = self.__gen_type_B_conv(
                __P_Value, 'P_Value', __keyConventions)
            __gen_dict[str(__keyNames['R_Value'])] = self.__gen_type_B_conv(
                __R_Value, 'R_Value', __keyConventions)
            __gen_dict[str(__keyNames['L_Value'])] = __L_Value

            if self.isDebug:
                pp.pprint(__gen_dict)

            __gen_data_list.append(__gen_dict)

        self.generated_list = __gen_data_list
        return __gen_data_list

    def __gen_type_A(self, single_data, gen_val, emptys, anchors):
        __name_anchor = anchors.get(gen_val, None)
        __name_text = str(emptys.get(gen_val, None))

        if __name_anchor is None:
            if self.isDebug:
                print("No "+str(gen_val)+" Anchor")
            return __name_text

        __cache_1 = single_data.find('p', {'class', str(__name_anchor)})

        if __cache_1 is not None:
            __cache_2 = __cache_1.find('a')
            if __cache_2 is not None:
                __name_text = str(__cache_2.get_text()).strip()
        return __name_text

    def __gen_type_B(self, single_data, gen_val, emptys, anchors):
        __name_anchor = anchors.get(gen_val, None)
        __name_text = str(emptys.get(gen_val, None))

        if __name_anchor is None:
            if self.isDebug:
                print("No "+str(gen_val)+" Anchor")
            return __name_text

        __cache_1 = single_data.find('p', {'class', str(__name_anchor)})
        if __cache_1 is not None:
            __name_text = str(__cache_1.get_text()).strip()
        return __name_text

    def __gen_type_C(self, single_data, gen_val, emptys, anchors):
        __name_anchor = anchors.get(gen_val, None)
        __name_text = str(emptys.get(gen_val, None))

        if __name_anchor is None:
            if self.isDebug:
                print("No "+str(gen_val)+" Anchor")
            return __name_text

        __cache_1 = single_data.find('a', {'class', str(__name_anchor)})
        if __cache_1 is not None:
            __name_text = str(__cache_1['href']).strip()
        return __name_text

    def __gen_type_B_conv(self, gen_Data, gen_val, convs):
        __var = convs.get(gen_val, None)
        if __var is None:
            return gen_Data
        __cahce_1 = gen_Data.split(__var)
        __dump_1 = __cahce_1[0]
        return __dump_1

    def save_to_pandas(self, save_path=None):
        if self.isDebug:
            print("Save to Pandas")

        generated_data = self.generated_list
        df_generated = pd.DataFrame(generated_data)

        if self.isDebug:
            pp.pprint(df_generated)

        df_generated.to_excel("output.xlsx",sheet_name='Gathering')