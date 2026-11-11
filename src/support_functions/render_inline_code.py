# Renders inline code in HTML using <code> tags. It handles multiple inline code blocks in a single string and ensures that unclosed backticks are preserved in the output.
def render_inline_code(text):
    result = ""
    code_text = ""
    inside_code = False

    for char in text:
        if char == "`":
            # jesli znak zamykajacy to wpisz dotychczasowy kod
            if inside_code:
                result = result + "<code>" + code_text + "</code>"
                code_text = ""
                inside_code = False
            # jesli znak otwierajacy to ustaw inside_code na True i ustaw code_text na pusty
            else:
                inside_code = True
                code_text = ""
        # jesli inny znak niz "`"
        else:
            if inside_code:
                code_text = code_text + char
            else:
                result = result + char
    # jesli po zakonczeniu petli brak zamykajacego "`" to dodaj znak i text z tymczasowego code_text
    if inside_code:
        result = result + "`" + code_text

    return result


print(
    render_inline_code(
        "This is a `code block` and this is another `code block` and this is an unclosed `code block"
    )
)
