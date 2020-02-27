class NotAvailable:
    def __str__(self):
        return "NA"

    def __repr__(self):
        return repr_(self)


NA = NotAvailable()
