import unittest

from crc import append_crc, verify_packet


class CRCTests(unittest.TestCase):
    def test_append_crc_returns_bytes_and_matches_request_vector(self):
        payload = bytes.fromhex("A1 03 00 0F 00 0F")
        packet = append_crc(payload)

        self.assertIsInstance(packet, bytes)
        self.assertEqual(packet, bytes.fromhex("A1 03 00 0F 00 0F 6D 2D"))

    def test_append_crc_accepts_integer_lists(self):
        packet = append_crc([0xA1, 0x03, 0x00, 0x0F, 0x00, 0x0F])

        self.assertEqual(packet[-2:], bytes.fromhex("6D 2D"))

    def test_verify_packet_accepts_a_valid_packet(self):
        packet = append_crc(bytes.fromhex("A1 03 00 0F 00 0F"))
        crch, crcl, is_valid = verify_packet(packet)

        self.assertEqual((crch, crcl), (0x6D, 0x2D))
        self.assertTrue(is_valid)

    def test_verify_packet_detects_payload_corruption(self):
        packet = bytearray(append_crc(bytes.fromhex("A1 03 00 0F 00 0F")))
        packet[3] ^= 0x01

        self.assertFalse(verify_packet(packet)[2])

    def test_verify_packet_rejects_packets_shorter_than_three_bytes(self):
        with self.assertRaises(ValueError):
            verify_packet(b"\\x01\\x02")

    def test_append_crc_rejects_empty_payload(self):
        with self.assertRaises(ValueError):
            append_crc(b"")


if __name__ == "__main__":
    unittest.main()
