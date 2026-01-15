import re
from PIL import Image, ImageDraw, ImageFont

# ----------------------------
# Unicode subscript mapping
# ----------------------------
SUBSCRIPT_MAP = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

def to_subscript(text):
    """Convert digits in a string to Unicode subscripts."""
    return text.translate(SUBSCRIPT_MAP)

# ----------------------------
# Chemical formula formatting
# ----------------------------
def format_formula(formula):
    """
    Converts chemical formulas to use Unicode subscripts.
    Preserves leading coefficients.
    Example: 2H2O -> 2H₂O
    """
    match = re.match(r"^(\d*)(.*)$", formula)
    coeff, body = match.groups()
    body = to_subscript(body)
    return f"{coeff}{body}"

# ----------------------------
# Equation formatting
# ----------------------------
def format_equation(equation):
    """
    Formats a full chemical equation:
    - Converts subscripts
    - Adds space before state symbols
    - Normalizes arrows
    """
    equation = equation.replace("-->", "→").replace("->", "→")

    parts = re.split(r"(\+|→)", equation)

    formatted_parts = []
    for part in parts:
        part = part.strip()

        if part in {"+", "→"}:
            formatted_parts.append(f" {part} ")
            continue

        # Separate state of matter
        state_match = re.search(r"\((aq|s|l|g)\)", part)
        state = ""
        if state_match:
            state = f" ({state_match.group(1)})"
            part = re.sub(r"\((aq|s|l|g)\)", "", part)

        formatted_parts.append(format_formula(part) + state)

    return "".join(formatted_parts)

# ----------------------------
# Image generation
# ----------------------------
def save_as_image(text, filename="chemical_equation.png"):
    """
    Saves formatted chemical text as an image.
    """
    font_size = 48
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    padding = 20
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    text_width, text_height = draw.textsize(text, font=font)

    img = Image.new(
        "RGB",
        (text_width + padding * 2, text_height + padding * 2),
        "white",
    )
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, fill="black", font=font)

    img.save(filename)
    return filename

# ----------------------------
# Main interaction loop
# ----------------------------
if __name__ == "__main__":
    user_input = input(
        "Enter a chemical formula or equation:\n"
        "Examples:\n"
        "  H2O\n"
        "  2H2(g) + O2(g) --> 2H2O(g)\n\n> "
    )

    if "→" in user_input or "+" in user_input or "-->" in user_input or "->" in user_input:
        formatted = format_equation(user_input)
    else:
        formatted = format_formula(user_input)

    print("\nFormatted output (copy/paste ready):")
    print(formatted)

    save = input("\nSave as image? (y/n): ").lower()
    if save == "y":
        filename = save_as_image(formatted)
        print(f"Image saved as: {filename}")
