from dataproviders import HardDriveProvider


def id3_tabbed(j):
    return '\t'.join(())


def echonest_tabbed(j):
    return '\t'.join(())


def lastfm_tabbed(j):
    return '\t'.join(())


NAME = 'music'
data = HardDriveProvider(NAME)
with open(NAME + '.tsv', 'w') as w:
    for d in data.get_all():
        w.write('{}\n'.format('\t'.join((id3_tabbed(d),
                                         lastfm_tabbed(d),
                                         echonest_tabbed(d)))))
