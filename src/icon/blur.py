from PIL import Image
import math

def _(ksize, sigma):
    if ksize % 2 == 0:
        raise ValueError("Kernel size must be an odd number.")
    if sigma <= 0:
        raise ValueError("Sigma must be greater than 0.")
    
    radius = ksize // 2
    kernel = []
    sum_val = 0.0
    
    for i in range(ksize):
        row = []
        for j in range(ksize):
            x = i - radius
            y = j - radius
            exponent = -(x**2 + y**2) / (2 * sigma**2)
            value = math.exp(exponent) / (2 * math.pi * sigma**2)
            row.append(value)
            sum_val += value
        kernel.append(row)
    
    # Normalize the kernel
    for i in range(ksize):
        for j in range(ksize):
            kernel[i][j] /= sum_val
    
    return kernel

def makePhotoBlur(img, ksize=5, sigma=1.0):
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    
    new_img = Image.new('RGB', (width, height))
    new_pixels = new_img.load()
    
    kernel = _(ksize, sigma)
    radius = ksize // 2
    
    for x in range(width):
        for y in range(height):
            r_total = 0.0
            g_total = 0.0
            b_total = 0.0
            
            for i in range(ksize):
                for j in range(ksize):
                    px = x + (i - radius)
                    py = y + (j - radius)
                    
                    # Handle boundary conditions
                    px = max(0, min(width - 1, px))
                    py = max(0, min(height - 1, py))
                    
                    r, g, b = pixels[px, py]
                    weight = kernel[i][j]
                    
                    r_total += r * weight
                    g_total += g * weight
                    b_total += b * weight
            
            # Clamp values to [0, 255]
            new_r = int(round(r_total))
            new_g = int(round(g_total))
            new_b = int(round(b_total))
            
            new_r = max(0, min(255, new_r))
            new_g = max(0, min(255, new_g))
            new_b = max(0, min(255, new_b))
            
            new_pixels[x, y] = (new_r, new_g, new_b)
    
    return new_img
