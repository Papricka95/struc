from typing import Any
from struc2 import Struct, Tag, LittleEndian, DV, DTR, BigEndian
from struc2.Serialized import Serialized
from struc2.SerializedImpl import u16, u8, f32, i64, i32, i16, i8
import csv
import ast


class Protocol(Struct):
    '''
        class Protocol have two subclasses: TypeOne and TypeTwo
        which intended for parsing input bytes-data of different types.

        staticmethod parse return dict in format:
        type0 {
            'imei': b'...',
            'type': '0x...'
            'latitude': ...,
            'longitude': ...
        }
        type1 {
            'imei': b'...',
            'type': '0x...'
            'code': '0x...',
            'message': ...
        }
    '''
    class TypeOne(Struct):
        '''
            class TypeOne contains method parse that can to parse bytes of data
            This method return dict of data which fit to type0
        '''
        def from_type_dtr(d: 'DataBlock') -> list[Any]:
            return [LittleEndian, 'f32']

        imei: Tag[bytes, 15, "cstring"]
        message_type: Tag[int, "u8"]

        latitude: Tag[Any, DV[lambda v: v*2], DTR[from_type_dtr]]
        longitude: Tag[Any, DV[lambda v: v*2], DTR[from_type_dtr]]

        @staticmethod
        def parse(data: bytes) -> dict:
            p = Protocol.TypeOne.unpack_b(data)
            return {'imei': p.imei, 'type': hex(p.message_type), 'latitude': p.latitude, 'longitude': p.longitude}

    class TypeTwo(Struct):
        '''
            class TypeTwo contains method parse that can to parse bytes of data
            This method return dict of data which fit to type1
        '''

        def cstring_from_size(self) -> list[Any]:
            return [self.code, "cstring"]

        imei: Tag[bytes, 15, "cstring"]
        message_type: Tag[int, "u8"]
        code: Tag[bytes, "u8"]
        message: Tag[Any, DTR[cstring_from_size]]

        @staticmethod
        def parse(data: bytes) -> dict:
            p = Protocol.TypeTwo.unpack_b(data)
            return {'imei': p.imei, 'type': hex(p.message_type), 'code': hex(p.code), 'message': p.message.decode('utf-8')[:-1]}

    def check_type(data: bytes):
        '''
            This function intended for check type of input data.
            The check intends for create valid returned data in format of dict.
        '''
        position_byte_type = 15
        current_type = data[position_byte_type]
        return current_type

    @staticmethod
    def parse(data: bytes) -> dict:
        if Protocol.check_type(data):
            parsed_dict = Protocol.TypeTwo.parse(data)
            return parsed_dict
        else:
            parsed_dict = Protocol.TypeOne.parse(data)
            return parsed_dict


imei_arr = []
with open('examples.csv', 'r', encoding='utf-8') as file:
    all_data = csv.reader(file)
    for data in all_data:
        imei_arr.append(data[0])


for inp in imei_arr:
    inp = ast.literal_eval(inp)
    print(Protocol.parse(inp))
