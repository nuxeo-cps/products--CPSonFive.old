from zope.app.form.browser import TextWidget
from zope.app.form.browser.widget import renderElement
from zope.app.datetimeutils import DateTimeError
from zope.app.form.interfaces import ConversionError, WidgetInputError
from zope.app.form.interfaces import InputErrors
from zope.schema.interfaces import ValidationError

class DocumentBrowserWidget(TextWidget):

    displayWidth = 30

    def __call__(self):
        value = self._getFormValue()
        res = renderElement(self.tag,
                            type=self.type,
                            name=self.name,
                            id=self.name,
                            value=value,
                            cssClass=self.cssClass,
                            style=self.style,
                            size=self.displayWidth,
                            extra=self.extra)
        style = "text-decoration:none;border:1px solid black;padding:0.2em 0.3em;"
        js = "window.open('../../documentnavigation_popup?input_id=" + \
                          self.name + "', 'DirectoryMultiEntryFinder', " \
                          "'toolbar=0, scrollbars=1, location=0, " \
                          "statusbar=0, menubar=0, resizable=1, dependent=1, " \
                          "width=500, height=480')"
        btn = renderElement("button", style=style, onClick=js, contents="Pressme!" )
        return res + btn
        