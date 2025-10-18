#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import Pool, PoolMeta


class SaleLine(metaclass=PoolMeta):
    'Sale Line'
    __name__ = 'sale.line'

    def _get_invoice_comment_line(self):
        'Return if comment lines should be invoiced'
        return (
            self.sale.invoice_method == 'order'
            and not self.sale.invoices)

    def get_invoice_line(self):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')

        if self.type == 'comment' and self._get_invoice_comment_line():
            invoice_line = InvoiceLine()
            invoice_line.type = self.type
            invoice_line.currency = self.currency
            invoice_line.company = self.company
            invoice_line.description = self.description
            invoice_line.note = self.note
            invoice_line.origin = self
            return [invoice_line]
        return super().get_invoice_line()
