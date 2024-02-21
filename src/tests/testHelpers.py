import unittest


def __prettyPrintByteComparison(bytes1: bytes, bytes2: bytes, marker_position: int = -1):
    """
    docstring
    """

    # shortened
    print("\nMixed representation:")
    print("Expected: . . . %s" % bytes1)
    print("Test result:. . %s" % bytes2)

    if marker_position > -1:
        marker = ''
        len_byte_str = len('%s' % bytes2[:marker_position - 1])
        for j in range(0, len_byte_str):
            marker += ' '
        for j in range(0, max(len('%s' % hex(bytes1[marker_position])), len('%s' % hex(bytes2[marker_position])))):
            marker += '^'
        print("                %s" % marker)

    # extended
    print("Alternative representation:")
    print("Expected: . . . %s" % __prettyPrintBytesExtended(bytes1))
    print("Test result:. . %s" % __prettyPrintBytesExtended(bytes2))

    if marker_position > -1:
        marker = ''
        for j in range(0, marker_position):
            marker += '   '
        marker += ' ^^'
        print("                %s" % marker)


def __prettyPrintBytesExtended(bytes_param: bytes) -> str:
    print_str = ''
    for j in range(0, len(bytes_param)):
        print_str_element = hex(bytes_param[j])[2:]
        if len(print_str_element) == 1:
            print_str_element = '0%s' % print_str_element
        print_str += ' %s' % print_str_element
    return print_str


def compareBytesLength(test_class: unittest.TestCase, bytes_expected: bytes, bytes_is: bytes):
    bytes_e_length = len(bytes_expected)
    bytes_i_length = len(bytes_is)

    if bytes_e_length != bytes_i_length:
        print("Expected: . . . %s" % __prettyPrintBytesExtended(bytes_expected))
        print("Test result:. . %s" % __prettyPrintBytesExtended(bytes_is))

    test_class.assertEqual(bytes_e_length, bytes_i_length,
                           msg="Bytes length is not equal. Expected: %s bytes, is: %s bytes."
                               % (bytes_e_length, bytes_i_length))


def compareBytesBitByBit(test_class: unittest.TestCase, bytes_expected: bytes, bytes_is: bytes):
    # bytesExpected: Expected
    # bytesIs: Result of class-under-test
    if len(bytes_is) > 0:

        for i in range(0, min(len(bytes_expected) - 1, len(bytes_is) - 1)):
            if bytes_expected[i] != bytes_is[i]:
                __prettyPrintByteComparison(bytes_expected, bytes_is, i)
            msg_text = ("Deviation at offset %s. Expected: %s, is: %s."
                        % (i + 1, hex(bytes_expected[i]), hex(bytes_is[i])))
            test_class.assertEqual(bytes_expected[i], bytes_is[i], msg=msg_text)


def readTemplateFile(filename: str) -> bytes:
    # file_content = b'\x00'
    with open(filename, 'rb') as readFile:
        file_content = readFile.read()
        readFile.close()
    return file_content


def writeVsMetaFile(filename: str, content: bytes):
    with open(filename, 'wb') as writeFile:
        writeFile.write(content)
        writeFile.close()
