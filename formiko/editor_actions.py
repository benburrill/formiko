from gi.repository.Gio import SimpleActionGroup, SimpleAction
from gi.repository.GLib import VariantType, Variant


class EditorActionGroup(SimpleActionGroup):
    def __init__(self, editor, renderer, preferences):
        super(EditorActionGroup, self).__init__()
        self.editor = editor
        self.renderer = renderer
        self.preferences = preferences

        self.create_stateful_action(
            "period-save-toggle", 'b', preferences.period_save,
            self.on_period_save)
        self.create_stateful_action(
            "use-spaces-toggle", 'b', preferences.spaces_instead_of_tabs,
            self.on_use_spaces)
        self.create_stateful_action(
            "tab-width", 'i', preferences.tab_width, self.on_tab_width)
        self.create_stateful_action(
            "auto-indent-toggle", 'b', preferences.auto_indent,
            self.on_auto_indent)
        self.create_stateful_action(
            "line-numbers-toggle", 'b', preferences.line_numbers,
            self.on_line_numbers)

    def create_stateful_action(self, name, _type, variable, method):
        action = SimpleAction.new_stateful(
            name, VariantType.new(_type),
            Variant(_type, variable))
        action.connect("change-state", method)
        self.add_action(action)

    def on_period_save(self, action, param):
        period_save = not self.preferences.period_save
        self.preferences.period_save = period_save
        self.editor.set_period_save(period_save)
        self.preferences.save()

    def on_use_spaces(self, action, param):
        use_spaces = not self.preferences.spaces_instead_of_tabs
        self.preferences.spaces_instead_of_tabs = use_spaces
        self.editor.set_spaces_instead_of_tabs(use_spaces)
        self.preferences.save()

    def on_tab_width(self, action, param):
        width = param.get_int32()
        self.preferences.tab_width = width
        self.editor.set_tab_width(width)
        self.renderer.set_tab_width(width)
        self.preferences.save()

    def on_auto_indent(self, action, param):
        auto_indent = not self.preferences.auto_indent
        self.preferences.auto_indent = auto_indent
        self.editor.set_auto_indent(auto_indent)
        self.preferences.save()

    def on_line_numbers(self, action, param):
        line_numbers = not self.preferences.line_numbers
        self.preferences.line_numbers = line_numbers
        self.editor.set_line_numbers(line_numbers)
        self.preferences.save()