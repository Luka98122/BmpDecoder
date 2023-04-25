import pygame
from PIL import Image
import time
import pygame


pygame.init()
fileToRead = "24bit.bmp"


byteL = []
hexL = []

with open(fileToRead, "rb") as f:

    header = f.read(14)
    print(header)
    data_offset = int.from_bytes(header[10:14], byteorder="little")
    f.seek(data_offset)

    byteL = list(f.read())


with Image.open(fileToRead) as img:
    width, height = img.size
    mode = img.mode
    decoder = 0
    if mode == "RGB":
        decoder = 24
    elif mode == "RGBA":
        decoder = 32
    print(mode)

with open(fileToRead, "rb") as f:
    # Read BMP file header (14 bytes)
    header = f.read(14)

    # Read DIB header (40 bytes)
    dib_header = f.read(40)
    print(dib_header)
    raw_decoder = str(dib_header).split("\\")[13]
    print("Raw", str(dib_header).split("\\"))
    raw_decoder = raw_decoder[1 : len(raw_decoder)]
    if decoder != 24 and decoder != 32:
        decoder = int(raw_decoder)
        if decoder != 24 or decoder != 32 or decoder != 8:
            raw_decoder = str(dib_header).split("\\")[12]
            raw_decoder = raw_decoder[1 : len(raw_decoder)]
            decoder = int(raw_decoder)
    print(decoder)
    # Read color palette (256*4 bytes)
    palette = []
    if decoder == 8:
        for i in range(256):
            color = list(f.read(4))
            palette.append(color)
    if decoder == 4:
        for i in range(16):
            color = list(f.read(4))
            palette.append(color)


window = pygame.display.set_mode((width, height))
window.fill(pygame.Color(255, 255, 255))
parity = 0
counter = 0
for i in range(height):

    for j in range(width):
        if decoder == 24:
            pixel_index = (i * width + j) * (3)
            b1 = byteL[pixel_index]
            b2 = byteL[pixel_index + 1]
            b3 = byteL[pixel_index + 2]
            pygame.draw.rect(
                window,
                pygame.Color(b3, b2, b1),
                pygame.Rect(j, height - i, 1, 1),
            )
        if decoder == 32:
            pixel_index = (i * width + j) * (4)
            b1 = byteL[pixel_index]
            b2 = byteL[pixel_index + 1]
            b3 = byteL[pixel_index + 2]
            b4 = byteL[pixel_index + 3]
            pygame.draw.rect(
                window,
                pygame.Color(b3, b2, b1, b4),
                pygame.Rect(j, height - i, 1, 1),
            )
        if decoder == 8:
            pixel_index = i * width + j
            b1 = byteL[pixel_index]
            c1 = palette[b1][0]
            c2 = palette[b1][1]
            c3 = palette[b1][2]
            pygame.draw.rect(
                window,
                pygame.Color(c3, c2, c1),
                pygame.Rect(j, height - i, 1, 1),
            )
        if decoder == 4:
            pixel_index = counter
            b1 = byteL[pixel_index]
            b1 = bin(b1)
            pre = b1[0:2]
            b1 = b1[2:].rjust(8, "0")
            finalNumber = int(
                pre
                + b1[0 + parity * 4]
                + b1[1 + parity * 4]
                + b1[2 + parity * 4]
                + b1[3 + parity * 4],
                0,
            )
            c1 = palette[finalNumber][0]
            c2 = palette[finalNumber][1]
            c3 = palette[finalNumber][2]
            c4 = palette[finalNumber][3]
            if parity == 0:
                parity = 1
            else:
                counter += 1
                parity = 0
            pygame.draw.rect(
                window,
                pygame.Color(c3, c2, c1, c4),
                pygame.Rect(j, height - i, 1, 1),
            )

    if i % 50 == 0:
        pygame.display.flip()

while True:
    evnt = pygame.event.get()
    print(evnt)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1] == True or keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    pygame.display.flip()
