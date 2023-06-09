import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from IPython.display import HTML

class StickyNote:
    BOOKMARK_TEMPLATE = """
    <div style="display: flex;">
      <div style="color: {tcolor}; background-color: {bcolor}; border: 1px solid {border}; padding: 10px; width: 200px; position: sticky; top: 10px; z-index: 1; overflow: auto;">
        <h3>@ {header}</h3>
        <p style="word-break: break-word;">{message}</p>
      </div>{code_div}
    </div>
    """
    COLORS = {
        "completed": "rgb(50, 200, 100)",
        "working": "rgb(255, 255, 153)",
        "todo": "rgb(239, 133, 0)",
        "failed": "rgb(300, 25, 0)",
        "validating": "rgb(173, 216, 230)",
        "warning": {
            "border": "#ff9800",
            "background": "#fff3e0",
            "color": "#ff5722"
        }
    }

    @staticmethod
    def _get_code_div(code: str) -> str:
        if code:
            highlighted_code = pygments.highlight(code, PythonLexer(), HtmlFormatter())
            return f"""
                <div style="flex: 1; padding: 10px;">
                    <h3>Code</h3>
                    <pre>{highlighted_code}</pre>
                </div>
            """
        else:
            return ""

    @staticmethod
    def completed(message: str, code: str = "") -> HTML:
        bcolor = StickyNote.COLORS.get("completed")
        code_div = StickyNote._get_code_div(code)
        return HTML(StickyNote.BOOKMARK_TEMPLATE.format(
            header="Completed Note", 
            tcolor="black",
            bcolor=bcolor, 
            message=message, 
            border="black",
            code_div=code_div))

    @staticmethod
    def working(message: str, code: str = "") -> HTML:
        bcolor = StickyNote.COLORS.get("working")
        code_div = StickyNote._get_code_div(code)
        return HTML(StickyNote.BOOKMARK_TEMPLATE.format(
            header="Working Note", 
            tcolor="black",
            bcolor=bcolor, 
            message=message, 
            border="black",
            code_div=code_div))

    @staticmethod
    def todo(message: str, code: str = "") -> HTML:
        bcolor = StickyNote.COLORS.get("todo")
        code_div = StickyNote._get_code_div(code)
        return HTML(StickyNote.BOOKMARK_TEMPLATE.format(
            header="Todo Note", 
            tcolor="black",
            bcolor=bcolor, 
            message=message, 
            border="black",
            code_div=code_div))

    @staticmethod
    def failed(message: str, code: str = "") -> HTML:
        bcolor = StickyNote.COLORS.get("failed")
        code_div = StickyNote._get_code_div(code)
        return HTML(StickyNote.BOOKMARK_TEMPLATE.format(
            header="Debugging Note", 
            tcolor="black",
            bcolor=bcolor, 
            message=message, 
            border="black",
            code_div=code_div))

    @staticmethod
    def validating(message: str, code: str = "") -> HTML:
        bcolor = StickyNote.COLORS.get("validating")
        code_div = StickyNote._get_code_div(code)
        return HTML(StickyNote.BOOKMARK_TEMPLATE.format(
            header="Validating Note", 
            tcolor="black",
            bcolor=bcolor, 
            message=message, 
            border="black",
            code_div=code_div))

    @staticmethod
    def warning(message: str, code: str = "") -> HTML:
        tcolor = StickyNote.COLORS.get("warning")["color"]
        bcolor = StickyNote.COLORS.get("warning")["background"]
        border = StickyNote.COLORS.get("warning")["border"]
        code_div = StickyNote._get_code_div(code)
        return HTML(StickyNote.BOOKMARK_TEMPLATE.format(
            header="Warning Note", 
            tcolor=tcolor,
            bcolor=bcolor, 
            message=message, 
            border=border, 
            code_div=code_div))

