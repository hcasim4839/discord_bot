'''
File is for various tables that can be used to display information
'''
from table2ascii import table2ascii
from PIL import Image, ImageDraw, ImageFont

def create_single_col_ascii_table(amt_of_rows:int, row_list:list, column_width = None, cell_alignment_list = None, header_list = None):
    table = None
    table_body = []
    print(f'{amt_of_rows=}')
    print(f'{row_list=}')
    for index in range(amt_of_rows):
        new_row_data = [row_list[index]]
        table_body.append(new_row_data)
    
    print(f'{table_body=}')
    ascii_table = table2ascii(body=table_body,header=header_list)
    ascii_table = f"```{ascii_table}```"
    font = ImageFont.load_default()  # Built-in font

    # Calculate image size
    lines = ascii_table.split("\n")
    max_line_length = max(len(line) for line in lines)
    font_size = 14
    line_height = font_size + 4
    image_width = max_line_length * font_size // 2
    image_height = len(lines) * line_height

    # Create a blank white image
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Render the ASCII table onto the image
    for i, line in enumerate(lines):
        draw.text((5, i * line_height), line, font=font, fill="black")

    # Save the image
    image.save("output_file.png")
    return ascii_table


