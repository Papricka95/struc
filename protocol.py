from typing import Any
from struc2 import Struct, Tag, LittleEndian, DV, DTR
from struc2.Serialized import Serialized
from struc2.SerializedImpl import u16, u8, f32


# import csv


class Protocol(Struct):
    def from_type_dtr(d: 'DataBlock') -> list[Any]:
        return [LittleEndian, 'f64']

    imei: Tag[bytes, 15, "cstring"]
    message_type: Tag[int, "u8"]
    # field_1: Tag[Any, DV[lambda v: v], DTR[from_type_dtr]]
    # field_2: Tag[Any, DV[lambda v: v], DTR[from_type_dtr]]
    field_1: Tag[int, "u8"]
    field_2: Tag[int, "u8"]

    def pars_func_type0(data: bytes) -> dict:

        print(data)
        p = Protocol.unpack_b(data)
        print(p.imei)
        print(p.message_type)
        print(p.field_1)
        print(p.field_2)
        return {'type': 'zero'}

    def pars_func_type1(data: bytes) -> dict:

        print(data)
        p = Protocol.unpack_b(data)
        print(data)
        print(p.imei)
        print(p.message_type)
        print(p.field_1)
        print(p.field_2)
        return {'type': 'one'}

    def check_type(data: bytes):
        current_type = data[15]
        return current_type

    @ staticmethod
    def parse(data: bytes) -> dict:

        # imei: Tag[bytes, 15, "cstring"]
        # message_type: Tag[int, "u8"]
        # code: Tag[int, "u8"]
        # message: Tag[bytes, "cstring"]
        # field_1: Tag[Any, DV[lambda v: v], DTR[from_type_dtr]]
        # field_2: Tag[Any, DV[lambda v: v], DTR[from_type_dtr]]

        if Protocol.check_type(data):
            print('type1')
            return Protocol.pars_func_type1(data)
        else:
            print('type0')
            return Protocol.pars_func_type0(data)

            # p = Protocol.unpack_b(data)
            # if (p.message_type):
            #     print(
            #         f"\'imei\': {p.imei}, \'type\': {p.message_type}, \'code\': {p.code}, \'message\': \'{p.message.decode('utf-8')}\'")
            #     return {'imei': p.imei, 'type': p.message_type, 'code': p.code, 'message': p.message.decode('utf-8')}
            # else:
            #     imei: Tag[bytes, 15, "cstring"]
            #     message_type: Tag[int, "u8"]
            #     lat: Tag
            #     lon: Tag
            #     p = Protocol.unpack_b(data)
            #     # print(
            #     #     f"\'imei\': {p.imei}, \'type\': {p.message_type}, \'code\': {p.lat}, \'message\': \'{p.lon}\'")
            # return p


inp1 = b'634982147811851\x01\x9dapproach allow\x00'
inp2 = b'276837711961258\x00\xfa\x83|@\xad\xf5\x1b\xc1'
inp3 = b'492220775190111\x00L\xc5\x14\xc2\xa7\xb2;\xc2'

# pars_func(inp1)
# pars_func2(inp3)
Protocol.parse(inp1)
# Protocol.parse(inp2)


# with open('examples.csv', 'r', encoding='utf-8') as file:
#     all_data = csv.reader(file)
#     print(all_data)
#     # for data in all_data:
#     #     print(data[0])
