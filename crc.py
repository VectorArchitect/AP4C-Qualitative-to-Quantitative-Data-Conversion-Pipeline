#this particular file acts as a library not just a program used by other 2 programs
# CRC-16 | Polynomial = 0xA001

def calcrc(data, ldata):      #calculating CRC and returning ch, cl
    ch = 0xFF                 #setting ch & cl as 255/0xFF
    cl = 0xFF

    for i in range(ldata + 1):        #first loop takes bytes in the list of data
        cl = cl ^ data[i]                #now xor each byte
        for ctrc in range(8):         #second loop takes bits in the bytes
            #if ch have '1' at last then we will add last 1 to
            carryh = ch % 2
            #if cl have '1' at last then we will do shift and xor
            carryl = cl % 2
            ch = ch // 2
            cl = (carryh * 128) + (cl // 2)
            if carryl != 0:      #last me 1 hoga to xor hoga
                ch = ch ^ 0xA0
                cl = cl ^ 0x01
    return ch, cl  # returns (CRCH, CRCL)      #this will return Cl first then Ch
    


def verify_packet(packet_bytes):
    """
    Recalculate the CRC for a complete packet (payload + two CRC bytes).

    Returns (expected_crch, expected_crcl, is_valid). The existing AP4C
    protocol uses CRCH followed by CRCL in the packet.
    """
    packet = bytes(packet_bytes)
    if len(packet) < 3:
        raise ValueError("A CRC packet must contain at least one data byte and two CRC bytes.")

    data = packet[:-2]
    expected_crch, expected_crcl = calcrc(data, len(data) - 1)
    received_crch, received_crcl = packet[-2:]
    is_valid = (
        expected_crch == received_crch
        and expected_crcl == received_crcl
    )
    return expected_crch, expected_crcl, is_valid


def append_crc(data_bytes):
    """
    Compute and append the AP4C CRC bytes.

    Returns bytes so the result can be passed directly to pySerial.write().
    """
    payload = bytes(data_bytes)
    if not payload:
        raise ValueError("Cannot append a CRC to an empty payload.")

    crch, crcl = calcrc(payload, len(payload) - 1)
    return payload + bytes((crch, crcl))


if __name__ == "__main__":      #use to run above code in this file but is ignored when pther files import it
    packet = input("Enter hex values (space separated): ").split()
    packet_int = [int(x, 16) for x in packet]    #converting from hex to int
    print(f"Data: {packet_int}")

    # new=append_crc(packet_int)
    # print(F"new: {new}")

    if len(packet_int) > 6:
        data = packet_int[:6]
        crc = packet_int[6:8]   #puts 7 & 8 th value counting form 1 not 0
        ldata = len(data) - 1
        crcl, crch = calcrc(data, ldata)
        print(f"Calculated → CRCH: {crch:02X}  CRCL: {crcl:02X}")
        if crc[0] == crch and crc[1] == crcl:
            print("✅ Data is Intact")
        else:
            print("❌ Data is Varied!")
    else:
        ldata = len(packet_int) - 1
        crcl, crch = calcrc(packet_int, ldata)
        print(f"Calculated → CRCH: {crch:02X} CRCL: {crcl:02X}  ")

