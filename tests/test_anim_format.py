"""Check the wire layout against the firmware's bicycle1 structures."""
import struct
import unittest
import animgen

class AnimationFormatTest(unittest.TestCase):
    def test_bicycle1_header_full_frame_and_unchanged_mask(self):
        pixel = b'\x10\x20\x30\xff'
        blob = animgen.encode_anim([pixel, pixel], fps=25, w=1, h=1)
        header = struct.unpack('<8sBBBBHHBBIIII', blob[:34])
        self.assertEqual((b'bicycle1', 0, 1, 1, 2, 0, 4, 25, 0, 20, 14, 1, 2), header)
        self.assertEqual(struct.pack('<III', 0, 1, 54) + b'default\0', blob[34:54])
        self.assertEqual(struct.pack('<BHH', 0x10, 0, 4) + pixel + struct.pack('<BHH', 0, 0, 0), blob[54:])
        animgen.decode_check(blob, [pixel, pixel], w=1, h=1)

    def test_rle_alpha_changes_and_legacy_option(self):
        frames = [b'\0\0\0\0' * 16, b'\x10\x20\x30\xff' * 16] * 2
        for version in (0, 1):
            blob = animgen.encode_anim(frames, w=4, h=4, format_version=version)
            animgen.decode_check(blob, frames, w=4, h=4)
        with self.assertRaises(ValueError):
            animgen.encode_anim([], format_version=1)
