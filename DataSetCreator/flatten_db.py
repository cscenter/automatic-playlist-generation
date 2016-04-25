from dataproviders import HardDriveProvider


def id3_tabbed(j):
    pass


def echonest_tabbed(j):
    pass


def lastfm_tabbed(j):
    pass


NAME = 'music'
data = HardDriveProvider(NAME)
with open(NAME + '.tsv') as w:
    for d in data.get_all():
        w.write('{}\n'.format('\t'.join((id3_tabbed(d),
                                         lastfm_tabbed(d),
                                         echonest_tabbed(d)))))
