#!/usr/bin/env python
# Copyright (C) 2014 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script to take a set of frames (PNG files) for a recovery animation
and turn it into a single output image which contains the input frames
interlaced by row.  Run with the names of all the input frames on the
command line, in order, followed by the name of the output file.
"""

from __future__ import print_function

import argparse
import os.path
import sys
try:
  import PIL.Image
  import PIL.PngImagePlugin
except ImportError:
  print("This script requires the Python Imaging Library to be installed.")
  sys.exit(1)


def interlace(output, inputs):
  frames = [PIL.Image.open(fn).convert("RGB") for fn in inputs]
  assert len(frames) > 0, "Must have at least one input frame."
  sizes = set()
  for fr in frames:
    sizes.add(fr.size)

  assert len(sizes) == 1, "All input images must have the same size."
  w, h = sizes.pop()
  N = len(frames)

  out = PIL.Image.new("RGB", (w, h*N))
  for j in range(h):
    for i in range(w):
      for fn, f in enumerate(frames):
        out.putpixel((i, j*N+fn), f.getpixel((i, j)))

  # When loading this image, the graphics library expects to find a text
  # chunk that specifies how many frames this animation represents.  If
  # you post-process the output of this script with some kind of
  # optimizer tool (eg pngcrush or zopflipng) make sure that your
  # optimizer preserves this text chunk.

  meta = PIL.PngImagePlugin.PngInfo()
  meta.add_text("Frames", str(N))

  out.save(output, pnginfo=meta)


def deinterlace(output, input):
  # Truncate the output filename extension if it's '.png'.
  if os.path.splitext(output)[1].lower() == '.png':
    output = output[:-4]

  img2 = PIL.Image.open(input)
  print(img2.mode)
  palette = img2.getpalette()
  img = img2.convert("RGB")
  num_frames = int(img.info.get('Frames', 1))
  print('Found %d frames in %s.' % (num_frames, input))
  assert num_frames > 0, 'Invalid Frames meta.'

  # palette = img.getpalette()
  print(palette)

  width, height = img.size
  height /= num_frames
  for k in range(num_frames):
    out = PIL.Image.new('RGB', (width, height))
    out.info = img.info
    for i in range(width):
      for j in range(height):
        out.putpixel((i, j), img.getpixel((i, j * num_frames + k)))
    # out.putpalette(img.getpalette(), rawmode='RGB')
    out2 = out.convert(mode='P', palette=palette)
    #out2 = out
    print(out2.mode)
    # out2.putpalette(palette)
    filename = '%s%02d.png' % (output, k)
    out2.save(filename)
    print('Frame %d written to %s.' % (k, filename))


def main(argv):
  parser = argparse.ArgumentParser(description='Parse')
  parser.add_argument('--deinterlace', '-d', action='store_true')
  parser.add_argument('--output', '-o', required=True)
  parser.add_argument('input', nargs='+')
  args = parser.parse_args(argv)

  if args.deinterlace:
    # args.input is a list, and we only process the first when deinterlacing.
    deinterlace(args.output, args.input[0])
  else:
    interlace(args.output, args.input)


if __name__ == '__main__':
  main(sys.argv[1:])
