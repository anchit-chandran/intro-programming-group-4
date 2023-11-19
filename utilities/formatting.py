def add_border(widget)->None:
    """Takes in a tk widget and adds border style"""
    widget.configure(relief="solid", borderwidth=2)

def calculate_max_col_width(data:list[list])->int:
    """For [row][cols], returns the max width // 2."""
    res = 1
    
    for row in data:
        for col in row:
            res = max(res, len(str(col)))
            
    return res // 2