import warnings
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from IPython.display import HTML, display
import ipywidgets as widgets
from ipywidgets import Layout
from functools import wraps
import markdown2

class CodeObject:
    def __init__(self, code: str):
        self.code = code

    def __repr__(self):
        return f"{self.__class__.__name__}(code={self.code!r})"

    def __str__(self):
        return f"CodeObject with code: {self.code}"
    
    def get_code(self):
        return self.code

class StickyNote:
    MESSAGE_HTML = """
    <div style="
        color: black; 
        background-color: {bcolor}; 
        border: 1px solid rgb(90 89 89); 
        padding: 10px; 
        width: 200px; 
        position: relative;
        margin-right: 10px;
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        z-index: 1;
        ">
        <h3 style="margin: 0">@ {note_type} Note</h3>
        <p style="word-break: break-word;">{message_html}</p>
        {warning_html}
    </div>
    """
    CODE_HTML = """
    <div style="
        flex: 1; 
        padding: 10px; 
        overflow: scroll; 
        border: 1px dotted darkgray; 
        border-radius: 5px;
        margin-right: 10px;
        ">
        <h3 style="margin: 0">Code</h3>
        <pre style="white-space: pre-wrap; word-wrap: break-word;">{highlighted_code}</pre>
    </div>
    """

    COLORS = {
        "completed": "rgb(76, 175, 80)",        # Green
        "working": "rgb(255, 235, 59)",         # Yellow
        "todo": "rgb(255, 152, 0)",             # Orange
        "failed": "rgb(244, 67, 54)",           # Red
        "error": "rgb(244, 67, 54)",            # Red
        "validation": "rgb(33, 150, 243)",      # Blue
        "warning": "rgb(255, 193, 7)"           # Amber
    }

    def __init__(self, interactive=None):
        if interactive is None:
            self.global_namespace = globals()
            self.interactive = False            
        elif isinstance(interactive, dict):
            self.global_namespace = interactive
            self.interactive = True
        else:
            raise ValueError("Interactive parameter must be a globals() dictionary or the globals function")

    @staticmethod
    def _get_todo_list(todo: list) -> widgets.VBox:
        if todo:
            checkboxes = []
            for bullet in todo:
                checkbox = widgets.Checkbox(
                    value=False,
                    description=bullet,
                    disabled=False,
                    indent=False
                )
                checkboxes.append(checkbox)
                header = widgets.HTML(value='<h3 style="margin: 0">Todo</h3>')
            return widgets.VBox([header] + checkboxes)
        else:
            return widgets.VBox()

    @staticmethod
    def normalize_indentation(code: str) -> str:
        lines = code.split('\n')
        if not lines:
            return code

        # Find the minimum indentation level (ignoring empty lines)
        min_indent = float('inf')
        for line in lines:
            stripped_line = line.lstrip()
            if stripped_line:
                indent = len(line) - len(stripped_line)
                min_indent = min(min_indent, indent)

        if min_indent == float('inf'):
            min_indent = 0

        # Remove the minimum indentation from all lines
        normalized_lines = [line[min_indent:] if len(line) >= min_indent else line for line in lines]
        return '\n'.join(normalized_lines)

    def _get_code_div(self, code: str) -> widgets.VBox:
        if code:
            code = StickyNote.normalize_indentation(code)
            highlighted_code = pygments.highlight(code, PythonLexer(), HtmlFormatter())
            output_area = widgets.Output()
            run_button = widgets.Button(description="Run")

            def on_run_button_clicked(b):
                output_area.clear_output()
                with output_area:
                    try:
                        exec(code, self.global_namespace)
                        display(HTML("<pre style='color: green;'>Code executed successfully.</pre>"))
                    except Exception as e:
                        display(HTML(f"<pre style='color: red;'>{str(e)}</pre>"))

            run_button.on_click(on_run_button_clicked)

            code_display = widgets.HTML(value=self.CODE_HTML.format(highlighted_code=highlighted_code))
            if self.interactive:
                return widgets.VBox([code_display, run_button, output_area])
            else:
                return widgets.VBox([code_display])
        else:
            return widgets.VBox()

    @staticmethod
    def _note_decorator(note_type: str):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # Check if positional arguments are provided
                message = ""
                code = ""
                todo = []

                if len(args) > 0:
                    message = args[0]
                    if len(args) > 1:
                        code = args[1]
                        if isinstance(code, list):
                            raise ValueError("The second unnamed argument is code, not a list")
                    if len(args) > 2:
                        todo = args[2]
                        if not isinstance(todo, list):
                            raise ValueError("The third unnamed argument is todo, not a string")

                # Override with keyword arguments if provided
                message = kwargs.pop('message', message)
                code = kwargs.pop('code', code)
                todo = kwargs.pop('todo', todo)

                if not message:
                    raise ValueError("Message is required")

                bcolor = StickyNote.COLORS.get(note_type)
                code_div = self._get_code_div(code)
                todo_list = StickyNote._get_todo_list(todo)

                warning_html = ""
                if func.__name__ == "validating":
                    warning_html = """
                    <div style='color: orange;'>
                        DeprecationWarning: The `validating` method is deprecated and will be removed in a future version.
                        Please use validation instead.
                    </div>
                    """

                # Convert Markdown to HTML
                message = self.normalize_indentation(message)
                message_html = markdown2.markdown(message)
                message_html = f"""
                <style>
                    blockquote {{
                        background-color: #333;
                        color: white;
                        border-left: 5px solid #444;
                        padding-left: 5px;
                    }}
                </style>
                {message_html}
                """

                bookmark_html = StickyNote.MESSAGE_HTML.format(
                    bcolor=bcolor, 
                    note_type=note_type.capitalize(), 
                    message_html=message_html, 
                    warning_html=warning_html,
                    bullet_div=""  # Remove the bullet div from the message HTML
                )

                bookmark_display = widgets.HTML(value=bookmark_html)
                hbox_layout = Layout(display='flex', flex_flow='row', padding='10px')
                display(widgets.HBox([bookmark_display, code_div, todo_list], layout=hbox_layout))

                return CodeObject(code)
            return wrapper
        return decorator

    @_note_decorator("completed")
    def completed(self, *args, **kwargs):
        pass

    @_note_decorator("working")
    def working(self, *args, **kwargs):
        pass

    @_note_decorator("todo")
    def todo(self, *args, **kwargs):
        pass

    @_note_decorator("failed")
    def failed(self, *args, **kwargs):
        pass

    @_note_decorator("error")
    def error(self, *args, **kwargs):
        pass

    @_note_decorator("validating")
    def validating(self, *args, **kwargs):
        pass

    @_note_decorator("validation")
    def validation(self, *args, **kwargs):
        pass

    @_note_decorator("warning")
    def warning(self, *args, **kwargs):
        pass
