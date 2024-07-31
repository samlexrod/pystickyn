import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from IPython.display import HTML
from functools import wraps


class StickyNote:
    BOOKMARK_TEMPLATE = """
    <div style="display: flex;">
      <div style="color: {tcolor}; background-color: {bcolor}; border: 1px solid {border}; padding: 10px; width: 200px; position: sticky; top: 10px; z-index: 1; overflow: auto;">
        <h3>@ {header}</h3>
        <p style="word-break: break-word;">{message}</p>
        {bullet_div}
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
    def _get_bullet_div(bullets: list) -> str:
        if bullets:
            bullet_html = "<ul>"
            for bullet in bullets:
                bullet_html += f"<li>{bullet}</li>"
            bullet_html += "</ul>"
            return bullet_html
        else:
            return ""
        
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
    def note_decorator(note_type: str):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs) -> HTML:
                # Check if positional arguments are provided
                message = ""
                code = ""
                bullets = []

                if args:
                    message = args[0]
                    if len(args) > 1:
                        code = args[1]
                        if isinstance(code, list):
                            raise ValueError("The second unnamed argument is code, not a list")
                    if len(args) > 2:
                        bullets = args[2]
                        if not isinstance(bullets, list):
                            raise ValueError("The third unnamed argument is bullets, not a string")
                
                # Override with keyword arguments if provided
                message = kwargs.pop('message', message)
                code = kwargs.pop('code', code)
                bullets = kwargs.pop('bullets', bullets)

                if not message:
                    raise ValueError("Message is required")

                bcolor = StickyNote.COLORS.get(note_type)
                code_div = StickyNote._get_code_div(code)
                bullet_div = StickyNote._get_bullet_div(bullets)
                html = StickyNote.BOOKMARK_TEMPLATE.format(
                    header=f"{note_type.capitalize()} Note", 
                    tcolor="black",
                    bcolor=bcolor, 
                    message=message, 
                    border="black",
                    code_div=code_div,
                    bullet_div=bullet_div
                )
                return HTML(html)
            return wrapper
        return decorator
        
    @note_decorator("completed")
    def completed(self, *args, **kwargs) -> HTML:
        pass

    @note_decorator("working")
    def working(self, *args, **kwargs) -> HTML:
        pass

    @note_decorator("todo")
    def todo(self, *args, **kwargs) -> HTML:
        pass

    @note_decorator("failed")
    def failed(self, *args, **kwargs) -> HTML:
        pass
    
    @note_decorator("validating")
    def validating(self, *args, **kwargs) -> HTML:
        pass

    @note_decorator("warning")
    def warning(self, *args, **kwargs) -> HTML:
        pass
