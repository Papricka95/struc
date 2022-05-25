from typing import Any
from struc2 import Struct, Tag, LittleEndian, DV, DTR, BigEndian
from struc2.Serialized import Serialized
from struc2.SerializedImpl import u16, u8, f32, i64, i32, i16, i8


class Protocol(Struct):
    '''
        class Protocol have two subclasses: TypeOne and TypeTwo
        which intended for parsing input bytes-data of different types.

        staticmethod parse return dict in format: 
        type0 {
            'imei': b'...',
            'type': '0x..'
            'lat'
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

        # latitude: Tag[Any, DV[lambda v: v / 2], DTR[from_type_dtr]]
        # longitude: Tag[Any, DV[lambda v: v / 2], DTR[from_type_dtr]]

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
        current_type = data[15]
        return current_type

    @staticmethod
    def parse(data: bytes) -> dict:
        if Protocol.check_type(data):
            parsed_dict = Protocol.TypeTwo.parse(data)
            return parsed_dict
        else:
            parsed_dict = Protocol.TypeOne.parse(data)
            return parsed_dict


inp1 = b'634982147811851\x01\x9dapproach allow\x00'
inp2 = b'744367240316316\x00k;\x83@\xa9L\rA'
inp3 = b'492220775190111\x00L\xc5\x14\xc2\xa7\xb2;\xc2'
inp4 = b'276837711961258\x00\xfa\x83|@\xad\xf5\x1b\xc1'
inp5 = b'681051685877949\x00QR5\xc2R\xb27\xc2'


print(Protocol.parse(inp1))
print(Protocol.parse(inp2))
print(Protocol.parse(inp3))
print(Protocol.parse(inp4))
print(Protocol.parse(inp5))
