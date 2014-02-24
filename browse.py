from IPython import display
from IPython.html import widgets
from pandas import DataFrame

class Browse(object):

    instance = None  # why? I think this is to limit to just 1.

    def __init__(self, df):

        Browse.instance = self
        self.closed = False

        self._popout = widgets.PopupWidget()
        self._popout.description = getattr(df, 'name', 'df')
        self._popout.button_text = self._popout.description
        self._modal_body = widgets.ContainerWidget()
        self._modal_body.set_css('overflow-y', 'scroll')

        self._modal_body_label = widgets.HTMLWidget(value = 'Not hooked')
        self._modal_body.children = [self._modal_body_label]

        self._popout.children = [
            self._modal_body,
        ]

        self._df = df
        self._ipython = get_ipython()
        self._ipython.register_post_execute(self._fill)

        self.ncols = len(df._info_axis)
        self.nrows = len(df)

    def close(self):
        """Close and remove hooks."""
        if not self.closed:
            del self._ipython._post_execute[self._fill]
            self._popout.close()
            self.closed = True
            Browse.instance = None

    def _fill(self):
        df = self._df
        values = self._df.values
        idx = self._df.index
        idx_values = idx.values

        idx_name = getattr(idx, 'name', 'Index') or 'Index'

        header = [idx_name] + df.columns.tolist()

        ncols = len(self._df.columns)  # TODO: Series
        nrows = len(self._df)

        f = lambda x, row: ''.join('<td>{}</td>'.format(v) for v in [x] + row.values.tolist())

        self._modal_body_label.value = '<table class="table table-bordered table-striped"' +\
            '<tr>' + ''.join('<th>{}</th>'.format(x) for x in header) + '</tr>' + \
            '<tr>' + ''.join('<tr>{}</tr>'.format(f(x, row)) for x, row in df.iterrows()) + '</tr>' + \
            '</table>'

    def _ipython_display_(self):
        """Called when display() or pyout is used to display the Variable
        Inspector."""
        self._popout._ipython_display_()
        self._popout.add_class('vbox')
        self._modal_body.add_class('box-flex1')

