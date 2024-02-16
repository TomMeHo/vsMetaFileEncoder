from datetime import date   # , datetime,  timezone
import hashlib
import base64


class VsMetaCode(bytes):
    def __init__(self, encoded_data: bytes = b''):
        self._data = encoded_data
        self._pos = 0

    def __len__(self) -> int:
        return len(self._data)

    def data(self) -> bytes:
        return self._data

    def hashMd5Hex(self) -> str:
        return hashlib.md5(self._data).hexdigest()

    def writeToFile(self, file_path: str):
        if len(self._data) > 0:
            with open(file_path, "wb") as f_vsmeta:
                f_vsmeta.write(self._data)

    def readFromFile(self, file_path: str):
        with open(file_path, "rb") as f_vsmeta:
            self._data = f_vsmeta.read()

    # ====================== read from code methods() as of here =======================================
    # ---------------------- methods which access self._data direct ------------------------------------
    def _readData(self, num_bytes: int) -> bytes:
        beg = self._pos
        self._pos += num_bytes
        return self._data[beg:self._pos]

    def pos(self) -> int:
        return self._pos

    def dataAhead(self, byte_cnt: int) -> bytes:
        end = len(self._data) if self._pos + byte_cnt > len(self._data) else self._pos + byte_cnt
        return self._data[self._pos:end]

    def byteCountAhead(self) -> int:
        return len(self._data) - self._pos

    # ---------------------- methods which access self._data only in-direct ---------------------------------
    def readHeader(self) -> bytes:
        return self._readData(2)

    def readTag(self) -> bytes:
        return self._readData(1)

    def readSpecialInt(self) -> int:
        mask, shift, length = 0x80, 0, 0        # 0x80 = 0b10000000
        while mask:
            byte = self.readInt(1)
            mask &= byte
            length |= (byte & ~mask) << shift   # ~0x80 = 0b01111111
            shift += 7
        return length

    def readBool(self) -> bool:
        return bool(self._readData(1))

    def readInt(self, byte_cnt: int) -> int:
        return int.from_bytes(self._readData(byte_cnt), "little")

    def readFloat(self) -> float:
        value = self.readSpecialInt()
        return value / 10.0 if value < 1e12 else -1.0

    def readString(self) -> str:
        return self._readData(self.readSpecialInt()).decode()

    def readTimeStamp(self) -> float:
        return float(self.readSpecialInt())

    def readVsData(self) -> 'VsMetaCode':
        return VsMetaCode(self._readData(self.readSpecialInt()))

    def readImage(self) -> (bytes, bool):
        image_str = self._readData(self.readSpecialInt())
        last_char_is_newline = (image_str[-1] == b'\n')
        return base64.decodebytes(image_str), last_char_is_newline

    def dumpData(self, num_bytes: int) -> None:
        print("Next... : {0}".format("".join(["{0:02x} ".format(value) for value in self.dataAhead(num_bytes)])))

    # ====================== write to code methods() as of here ================================================
    # ---------------------- methods which access self._data direct ------------------------------------

    def writeTag(self, tag: bytes, value=None):  # , int_bytes: int = 0, signed: bool = True):
        # write tag
        self._data += tag
        if value is None:
            return
        # write content
        if type(value) is int:
            self._data += self.calcSpecialInt(value)
        elif type(value) is str:
            self.writeStr(value)
        elif type(value) is date:
            self._writeDate(value)
        elif type(value) is bool:
            self._writeBool(value)
        elif type(value) is bytes:
            self._writeBytes(value)
        elif type(value) is dict:
            self.writeStr(str(value))
        elif type(value) is VsMetaCode:
            self._writeContent(value)

    def writeStr(self, text: str, with_bom: bool = False):
        # byteOrderMark \xEF\xBB\xBF is written automatically when using utf-8-sig.
        encoding = 'utf-8-sig' if with_bom else 'utf-8'
        text_bytes = bytes(text, encoding)
        self._data += self.calcSpecialInt(len(text_bytes)) + text_bytes

    def _writeDate(self, date_value: date):
        # length of date string: x0a = 10
        self._data += b'\x0a' + bytes(date_value.isoformat(), 'utf-8')

    def _writeBool(self, byte_value: bool):
        self._data += b'\x01' if byte_value else b'\x00'

    def _writeBytes(self, byte_value: bytes):
        self._data += byte_value

    def _writeContent(self, value):
        self._data += self.calcSpecialInt(len(value)) + value.data()

    # --------------- public methods which don't access self._data as of here ----------------
    @staticmethod
    def calcSpecialInt(num: int) -> bytes:
        if num < 0:
            return b'\x00'          # may be better to raise an exception here ?!
        return_value = b''
        has_more = 0x80
        while has_more:
            value = num & 0x7F
            num >>= 7
            has_more = 0x80 if num != 0 else 0x00
            return_value += (value | has_more).to_bytes(1, 'little')
        return return_value
