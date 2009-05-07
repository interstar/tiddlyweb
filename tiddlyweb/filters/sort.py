"""
Sort routines.
"""


def date_to_canonical(x):
    gap = 14 - len(x)
    if gap > 0:
        x = x + '0' * gap
    return x

ATTRIBUTE_ALTER = {
        'modified': date_to_canonical
        }

def sort_by_attribute(attribute, tiddlers, reverse=False):

    func = ATTRIBUTE_ALTER.get(attribute, lambda x : x.lower())

    def key_gen(x):
        try:
            return func(getattr(x, attribute))
        except AttributeError:
            try:
                return func(x.fields[attribute])
            except KeyError, exc:
                raise AttributeError('no attribute: %s, %s' % (attribute, exc))

    return sorted(tiddlers, key=key_gen, reverse=reverse)
